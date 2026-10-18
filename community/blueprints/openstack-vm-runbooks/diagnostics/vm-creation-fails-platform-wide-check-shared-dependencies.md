---
title: VM creation fails platform-wide while instances keep running. Check the shared dependencies first
kind: diagnostic
status: draft
openstack_releases: [unrecorded]
components: [nova, neutron, rabbitmq, mariadb, memcached, haproxy, keystone]
deployment_methods: [any]
environment:
  topology: HA control plane (clustered RabbitMQ, Galera)
  network: any
  storage: any
  os: any
risk: read-only
confirmed_by: []
upstream_refs:
  - https://galeracluster.com/library/documentation/monitoring-cluster.html
  - https://www.rabbitmq.com/docs/partitions
  - https://docs.openstack.org/oslo.messaging/latest/admin/rabbit.html
last_verified: 2026-10-18
---

# VM creation fails platform-wide while instances keep running. Check the shared dependencies first

When every provisioning request fails or hangs at once, the cause is rarely in Nova. The control plane (APIs,
schedulers, conductors, message bus, databases) fails separately from the data plane (hypervisors, instance disks,
network paths). Running instances survive a control-plane failure; what is lost is the ability to create, change,
migrate or delete resources. This page is the read-only triage of the shared dependencies that every capability
rests on.

## Symptom

- Users cannot create instances; some requests time out, some go to `ERROR`, some stay in `BUILD`/`scheduling`.
- Existing instances run and are reachable.
- The failures are not confined to one host, project or network.
- Often: other operations (volume attach, floating IP associate, port create) also hang or fail.

## Impact

Loss of one capability (provisioning and changes), platform-wide. Workloads are not at risk from the condition
itself. They are at risk from an uncontrolled attempt to fix it: an unstable control plane that keeps accepting
requests creates orphaned allocations, half-built instances and records that disagree between Nova, Placement and
Neutron, and every such record makes recovery slower.

## Quick checks

```bash
# 1. Service liveness as the services report it
openstack compute service list                   # any 'down'? all of them down = bus or database, not hosts
openstack network agent list                     # same question (agent-based backends)

# 2. Transitional-state instances piling up
openstack server list --all-projects --long -c ID -c Status -c "Task State" -c Created | grep -E 'BUILD|scheduling|networking|spawning'

# 3. API health at the load balancer: are the APIs answering, and how slowly?
time openstack token issue -f value -c id >/dev/null
time openstack server list --limit 1 >/dev/null

# 4. What changed? Deployments, config changes, certificate rotations, host maintenance, network changes in the
#    last hours. This question resolves more incidents than any metric.
```

## Diagnosis, in dependency order

Follow the chain a VM creation traverses: Keystone and memcached (authentication), the API (HAProxy and the VIP),
the database (Galera), the message bus (RabbitMQ), then Placement, Glance, Neutron, Cinder.

### Keystone and memcached

Slow or failing token validation makes every API call slow or failing. Check memcached is reachable from the API
hosts and not full; check Keystone logs for Fernet key errors (keys must be identical on every Keystone node; a
rotation that removed a key still validating tokens breaks the whole platform at once). Check TLS certificate
expiry on every endpoint: expired certificates are one of the most common causes of a complete control-plane
outage on long-lived platforms.

```bash
openssl s_client -connect <internal-api-vip>:5000 </dev/null 2>/dev/null | openssl x509 -noout -enddate
```

### Load balancer and VIP

Is the VIP on exactly one node (`ip addr` on the controllers)? Are the backends up in HAProxy's stats? A flapping VIP
or backends marked down explains intermittent API failures.

### Galera (MariaDB)

```sql
SHOW STATUS LIKE 'wsrep_cluster_size';           -- expected: number of nodes
SHOW STATUS LIKE 'wsrep_cluster_status';         -- anything but Primary: the node refuses writes
SHOW STATUS LIKE 'wsrep_local_state_comment';    -- Synced expected; Donor/Desynced, Joining = recovering
SHOW STATUS LIKE 'wsrep_flow_control_paused';    -- fraction of time replication stalled the node; near 1 = stuck
```

**Kolla-Ansible:** `docker exec -it mariadb mysql -uroot -p -e "SHOW STATUS LIKE 'wsrep%'"` on a controller. Run it
on every node: a node in `non-Primary` while the others are `Primary` is a node that lost quorum.

### RabbitMQ

```bash
rabbitmqctl cluster_status                       # every node running? any "partitions" listed? alarms?
rabbitmq-diagnostics check_alarms                # memory or disk alarm blocks publishers
rabbitmqctl list_queues name messages consumers | awk '$2>0 && $3==0'    # queues piling up with no consumer
rabbitmqctl list_unresponsive_queues
```

**Kolla-Ansible:** prefix with `docker exec -it rabbitmq`. A partition means the bus is split into sides the services
cannot agree on; services connected to different sides exchange nothing. Two facts decide what you may do next:
whether the cluster uses the Mnesia metadata store (every version before 3.13, and clusters upgraded in place),
where `cluster_partition_handling` (`pause_minority` is the usual OpenStack choice) governs behaviour, or the Khepri
store (default for new clusters in recent 4.x), where that setting no longer applies; and whether the queues are
quorum queues (recommended by oslo.messaging, `rabbit_quorum_queue`), which need a majority of their members and
are lost when two nodes of three are down.

A queue whose messages accumulate while its consumers vanish is a service that has stopped processing, whatever
its process list says. A `nova-compute` that reports `up` but has a stale bus connection does nothing.

### The OpenStack services

Only now read `nova-api.log`, `nova-conductor.log`, `nova-scheduler.log`, `neutron-server.log`, for the request id
of a failed boot. Typical confirmations: `AMQP server on ... is unreachable`, `MessagingTimeout`,
`Lost connection to MySQL server`, `WSREP has not yet prepared node for application use`.

## Possible causes

| Cause | How to tell |
|---|---|
| RabbitMQ network partition | `cluster_status` lists partitions; RPC timeouts in every service; agents report up but nothing moves |
| RabbitMQ memory or disk alarm | `check_alarms`; publishers block, APIs hang rather than fail |
| Galera node out of Primary, or whole cluster non-Primary | `wsrep_cluster_status`; services log WSREP errors |
| Galera flow control stalled | `wsrep_flow_control_paused` near 1; everything slow, nothing failing outright |
| Certificate expired, Fernet keys inconsistent | Every API call fails authentication; dated exactly |
| memcached down or full | Token validation slow; Keystone logs cache errors |
| VIP or HAProxy problem | Intermittent failures depending on which backend answers |

## What to do next

This page is read-only on purpose. Two situations lead to different runbooks, and they start from the same alert:

- **A RabbitMQ node has left the cluster** while the others still form a majority: rejoin or reset that one node,
  watch consumers reconnect. Bounded and routine.
- **The RabbitMQ cluster has partitioned**: do not touch the nodes yet. Establish which side the services talk to,
  decide whether to stop the APIs first, and escalate before any node is reset, because the wrong reset discards
  the queues the services are still using. See
  [Reopening provisioning after a control-plane incident](../recovery/reopening-provisioning-after-control-plane-incident.md)
  for the controlled-degradation path: stop the APIs, recover the bus and the database on a platform whose state is
  no longer changing, verify, reopen.

For Galera recovery after a full outage (`safe_to_bootstrap`, `--wsrep-recover`, bootstrapping from the most
advanced node), follow the Galera documentation and your deployment tool's procedure (Kolla-Ansible:
`kolla-ansible mariadb-recovery`). Bootstrapping the wrong node discards committed transactions; it is the step to
rehearse before you need it.

## Validity and limits

Derived from an operator's incident (users could not create VMs, instances ran, cause later established as a
RabbitMQ partition) and from the shared-component signals they recommend watching; release not recorded.
RabbitMQ facts (Khepri, quorum queues, removal of classic mirroring in 4.0) are version-dependent: check which
store and queue types your cluster uses before applying partition guidance. OVN deployments do not carry Neutron
agent RPC on RabbitMQ (OVN uses its own databases), so the "agents stale" symptom does not apply to them.

## Related

- [What a VM creation traverses, and tracing it by request id](what-a-vm-creation-traverses-and-tracing-by-request-id.md).
- [Reopening provisioning after a control-plane incident](../recovery/reopening-provisioning-after-control-plane-incident.md).
- Source: *OpenStack, the Day After Tomorrow* (S. Zaouam), chapters 1, 8, 10, 11, 17 and 19.
