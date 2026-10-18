---
title: Reopening provisioning after a control-plane incident. Stop the APIs, recover, verify, reopen
kind: runbook
status: draft
openstack_releases: [unrecorded]
components: [nova, neutron, rabbitmq, mariadb, haproxy]
deployment_methods: [any]
environment:
  topology: HA control plane (clustered RabbitMQ, Galera)
  network: any
  storage: any
  os: any
risk: destructive
confirmed_by: []
upstream_refs:
  - https://www.rabbitmq.com/docs/partitions
  - https://galeracluster.com/library/documentation/crash-recovery.html
  - https://docs.openstack.org/kolla-ansible/latest/user/operating-kolla.html
last_verified: 2026-10-18
---

# Reopening provisioning after a control-plane incident. Stop the APIs, recover, verify, reopen

Controlled degradation applied to a real incident: users could not create VMs, running instances were fine, the
message bus and the database were unhealthy, and the cause was unknown at the time. The team chose to stop
accepting requests, recover the shared infrastructure on a platform whose state was no longer changing, verify end
to end, and only then reopen. The alternative, repairing the bus and the database while the APIs kept accepting
operations, would have produced broader and less predictable damage.

## Symptom

See [VM creation fails platform-wide](../diagnostics/vm-creation-fails-platform-wide-check-shared-dependencies.md):
provisioning lost, workloads running, RabbitMQ unable to complete RPC exchanges reliably (partition, alarms, or
queues with no consumers), Galera affected (nodes out of `Primary`, flow control stalled).

## Impact

Deliberate and explicit: provisioning and resource changes unavailable for the duration of the recovery. Running
instances keep running, keep their storage and keep exchanging traffic. New ports, security-group rule changes and
floating IP associations will not take effect until the control plane returns; an instance that boots during the
stop may fail to reach the metadata service.

## Quick checks: decide whether to stop

Stop the APIs when **both** are true:

1. The shared infrastructure is unhealthy and you do not yet know why or which requests were partially applied.
2. The business impact of "no new VMs for N minutes" is bounded and can be communicated.

Do **not** use this runbook for a single RabbitMQ node that left a cluster that still has a majority; rejoin that
node instead. The two situations start from the same alert and need different procedures.

Before stopping, record who authorised the stop and communicate it as a protection decision: what is restricted,
why continuing would create greater risk, what remains protected, and what condition will allow reopening.

## Resolution

### Step 1: stop accepting requests

> ⚠️ **State-changing, production impact.** Every API becomes unavailable to users. Running instances are not
> affected. Stopping the APIs does not silence the platform: conductors, schedulers and agents keep their own work
> going.

Preferred: disable the API backends at the load balancer, so that the VIP answers with an error rather than
timing out, and the action is reversible in one place. Alternative: stop the API services or containers.

**Kolla-Ansible:** on each controller, `docker stop nova_api neutron_server cinder_api glance_api placement_api
keystone` (adapt to the services you run); or set the backends to `MAINT` in HAProxy.
**Any:** `systemctl stop <api services>` or the equivalent HAProxy change.

Keep Keystone up if you can: you need tokens to verify later, and nothing user-facing works without it anyway.

### Step 2: recover the message bus

> 🛑 **Destructive.** Purging or resetting RabbitMQ discards every in-flight RPC message: operations in progress
> (builds, deletes, migrations) are lost and their instances will need [stale-record clean-up](../lifecycle/stale-records-stuck-instances-orphan-ports-attachments.md).
> Affects every service. Precondition: the APIs are stopped (step 1), so no new requests accumulate; you have
> established the cluster is partitioned or its state is unrecoverable by rejoining nodes. Cannot be undone.

First, establish the state on every node (`rabbitmqctl cluster_status`, `check_alarms`, which store the cluster
uses, which queue types). If a clean rejoin of one side is possible, prefer it. Otherwise, the incident path:

1. Stop the RabbitMQ application on every node (`rabbitmqctl stop_app`), the last node stopped first on restart.
2. Reset or purge according to your deployment tool's procedure. **Kolla-Ansible:** `kolla-ansible rabbitmq-reset-state`
   resets the cluster and recreates it. **Any:** `rabbitmqctl force_reset` on the nodes, then rejoin, or purge the
   queues one by one (`rabbitmqctl purge_queue <queue>`) if the cluster itself is healthy.
3. Start the application on every node and confirm `cluster_status` shows one cluster, no partitions, no alarms.

When RabbitMQ returns, every agent on every host reconnects at once; on a large platform that reconnection storm is
itself a load to expect, and consumers may take minutes to reappear on queues.

### Step 3: recover the database

> 🛑 **Destructive if done wrong.** Bootstrapping Galera from the wrong node discards the transactions the others
> had committed. Precondition: identify the most advanced node (`grastate.dat`: `seqno` and `safe_to_bootstrap`;
> after an unclean stop, run `mysqld --wsrep-recover` on each node to find the highest seqno). Backup first if the
> data directories allow it.

If the cluster is merely degraded (one node non-Primary), restart that node and let it SST/IST from the others. If
the whole cluster is non-Primary, follow the Galera crash-recovery procedure or your tool's:
**Kolla-Ansible:** `kolla-ansible mariadb-recovery`.
Confirm on every node: `wsrep_cluster_size` is full, `wsrep_cluster_status` is `Primary`,
`wsrep_local_state_comment` is `Synced`.

### Step 4: restart the OpenStack services that hold bus connections

> ⚠️ **State-changing.** Restarting conductors, schedulers, `nova-compute` and Neutron agents re-establishes
> clean RPC connections. Agent restarts can briefly interrupt data-plane changes on the host; `nova-compute`
> restarts do not affect running instances.

Restart conductors and schedulers on the controllers, then `nova-compute` and network agents (or `ovn-controller`
is unaffected by RabbitMQ; OVN deployments skip the Neutron agents) in batches.

## Verification, before reopening

All three must hold:

```bash
# 1. Shared infrastructure whole
rabbitmqctl cluster_status                                   # one cluster, no partitions, no alarms
rabbitmqctl list_queues name messages consumers | awk '$3==0 && $2>0'   # empty: every queue has consumers
mysql -e "SHOW STATUS LIKE 'wsrep_cluster_size'; SHOW STATUS LIKE 'wsrep_cluster_status';"

# 2. Every compute service and network agent reporting again
openstack compute service list --service nova-compute | grep -c down     # 0
openstack network agent list | grep -c -w False                          # 0 alive=False (agent-based backends)

# 3. End-to-end: create, reach, delete a test instance (with the APIs reopened internally, or from a controller)
openstack server create --flavor <flavor> --image <image> --network <network> --wait reopen-test
openstack server add floating ip reopen-test <fip>   # or test from a host on the network
ping -c 3 <address>
openstack server delete --wait reopen-test
```

Only then re-enable the API backends and announce the reopening. Expect a burst of retried requests from users and
automation.

## Afterwards

- Establish the cause. In the source incident it was a network partition within the RabbitMQ cluster; a known
  failure mode with known mitigations, from the partition-handling setting on the versions that still have one to
  the network design that prevents the split. An incident review that stops at "we restarted RabbitMQ" guarantees
  a repeat.
- Clean up what the purge interrupted: [stale records](../lifecycle/stale-records-stuck-instances-orphan-ports-attachments.md).
- Record the decision: who stopped, why, what was protected, what condition reopened. Next time the authority
  question is already answered.

## Validity and limits

Derived from one real incident on an HA control plane; release, RabbitMQ and Galera versions not recorded. The
RabbitMQ steps depend heavily on version (Mnesia versus Khepri, quorum versus classic queues): read the RabbitMQ
documentation for your version before resetting anything. Deployment-tool commands are given for Kolla-Ansible;
other tools have their own recovery commands. This is the heaviest option; use it when lighter ones (rejoin one
node, restart one service) do not apply.

## Related

- [VM creation fails platform-wide: check the shared dependencies first](../diagnostics/vm-creation-fails-platform-wide-check-shared-dependencies.md).
- [Stale records](../lifecycle/stale-records-stuck-instances-orphan-ports-attachments.md).
- Source: *OpenStack, the Day After Tomorrow* (S. Zaouam), chapters 1, 10, 11 and 19.
