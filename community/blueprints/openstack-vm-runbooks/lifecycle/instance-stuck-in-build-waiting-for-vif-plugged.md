---
title: Instance stuck in BUILD, then ERROR after vif_plugging_timeout
kind: runbook
status: draft
openstack_releases: [unrecorded]
components: [nova, neutron, ovn, ovs]
deployment_methods: [any]
environment:
  topology: any
  network: ovn or ml2/ovs (agent-based)
  storage: any
  os: any
risk: state-changing
confirmed_by: []
upstream_refs:
  - https://docs.openstack.org/nova/latest/admin/architecture.html
  - https://docs.openstack.org/nova/latest/configuration/config.html#DEFAULT.vif_plugging_timeout
  - https://docs.openstack.org/neutron/latest/admin/ovn/
last_verified: 2026-10-18
---

# Instance stuck in BUILD, then ERROR after vif_plugging_timeout

A networking problem wearing a compute symptom. The instance sits in `BUILD` with task state `spawning` for about
five minutes, then goes to `ERROR`. Nova is waiting for Neutron to tell it the port is wired, and the message never
comes.

## Symptom

```text
$ openstack server show <server-id> -c status -c OS-EXT-STS:task_state -c OS-EXT-STS:vm_state
status      | BUILD
task_state  | spawning
vm_state    | building
```

After `vif_plugging_timeout` seconds (default 300), the instance goes to `ERROR` with a fault like:

```text
Virtual Interface creation failed
```

or, in `nova-compute.log` on the selected host:

```text
Timeout waiting for [('network-vif-plugged', '<port-id>')] for instance with vm_state building and task_state spawning
```

Scheduling itself succeeded: the instance has a host (`OS-EXT-SRV-ATTR:host`) and an allocation in Placement.

## Impact

New instances fail on one host, a set of hosts, or everywhere, depending on the cause. Running instances are not
affected. Each failed build leaves an `ERROR` instance that holds quota and a Placement allocation until deleted.

## Quick checks

Run on a controller with admin credentials, unless stated otherwise.

```bash
# 1. Which host was selected, and the fault
openstack server show <server-id> -c OS-EXT-SRV-ATTR:host -c fault

# 2. Is the port bound, and to what?
openstack port list --server <server-id> -c ID -c Status -c "Binding Host"
openstack port show <port-id> -c binding_vif_type -c binding_host_id -c status
#    binding_vif_type = binding_failed  -> Neutron could not bind the port on that host
#    status = DOWN with a valid vif_type -> bound, but never came up: agent/controller side

# 3. Is the networking agent or OVN controller alive on that host?
openstack network agent list --host <compute-host>

# 4. Is it one host or all of them?
openstack server list --all-projects --status ERROR --long -c ID -c Host -c Created | head
```

## Diagnosis

### Nova (compute host)

`nova-compute.log` for the instance UUID shows the wait: `Preparing to wait for external event network-vif-plugged`,
then the timeout. If instead you see `network-vif-plugged` received and the boot still fails, this is a different
runbook.

**Kolla-Ansible:** `docker logs nova_compute 2>&1 | grep <server-id>` or `/var/log/kolla/nova/nova-compute.log`.
**Any:** `journalctl -u nova-compute | grep <server-id>` or the configured log file.

### Neutron server

Search `neutron-server.log` for the port UUID. Look for the binding attempt and its result:

- `Failed to bind port <port-id> on host <host>`: no mechanism driver accepted the binding. Usual causes: the agent
  on that host is dead or not reporting, the network's segmentation type (VLAN, VXLAN, Geneve) is not configured on
  that host's bridge mappings, or the physical network name does not match.
- Binding succeeded but no `network-vif-plugged` was sent: the agent or OVN controller never reported the port up,
  or Neutron could not reach the Nova API to deliver the event (check `[nova]` section credentials and endpoint in
  `neutron.conf`, and `neutron-server.log` for `Failed to notify nova on events`).

### Agent or OVN controller (compute host)

**ML2/OVS:** `openstack network agent list --host <host>` must show `Open vSwitch agent` alive. On the host,
`ovs-vsctl show` should list the tap device of the port under `br-int`; `neutron-openvswitch-agent.log` shows the
port being processed. An agent that is alive but has a stale or stuck RPC connection (after a RabbitMQ incident, for
example) processes nothing: look for `AMQP server unreachable` or long gaps in the log.

**OVN:** on the host, `docker logs ovn_controller` (Kolla-Ansible) or `journalctl -u ovn-controller`. Check that
the chassis is registered and claims the port:

```bash
ovn-sbctl show                              # run where ovn-sbctl can reach the southbound DB
ovn-sbctl --columns=logical_port,chassis find Port_Binding logical_port=<port-id>
ovn-nbctl lsp-get-up <port-id>              # true once the port is up
```

An empty `chassis` means the controller on that host never claimed the port: the host's `ovn-bridge-mappings` or
`ovn-encap-ip` external_ids may be wrong, or `ovn-controller` cannot reach the southbound database (check the
`ovn-remote` setting and TLS).

### Message bus (agent-based backends only)

If every host is affected at once after a RabbitMQ or network event, the agents may be connected to a partitioned
or stale bus. See [VM creation fails platform-wide: check the shared dependencies](../diagnostics/vm-creation-fails-platform-wide-check-shared-dependencies.md).

## Possible causes

| Cause | How to tell |
|---|---|
| Agent or OVN controller down or not reporting on the host | `network agent list` shows it dead, or `ovn-sbctl show` has no chassis for the host |
| Bridge mappings or physical network mismatch on the host | `binding_vif_type = binding_failed`; `neutron-server.log` says no mechanism driver bound the port; only networks of one type fail |
| Agents alive but RPC stale after a bus incident | Agents report alive (heartbeat is on a separate connection) but process nothing; recovers on restart |
| Neutron cannot notify Nova | Port is `ACTIVE`, `neutron-server.log` shows notification errors; every host affected |
| Host simply slow (storage, many ports at once) | Event arrives just after the timeout; raising `vif_plugging_timeout` is a workaround, not a fix |

## Resolution

### Agent or controller down, or RPC stale

> ⚠️ **State-changing.** Restarting `neutron-openvswitch-agent` can briefly disrupt data-plane changes on the host
> and, on some versions and configurations, existing flows; restarting `ovn-controller` is usually transparent
> but re-syncs every port on the host. Do it on one host first.

**Kolla-Ansible:** `docker restart neutron_openvswitch_agent` or `docker restart ovn_controller` on the host.
**Any:** `systemctl restart neutron-openvswitch-agent` or `systemctl restart ovn-controller`.

### Bridge mappings or physical network mismatch

Fix the host's configuration (`bridge_mappings` in the OVS agent config, or `ovn-bridge-mappings` in
`ovs-vsctl get open . external_ids`) so that it matches the other hosts and the network's `provider:physical_network`,
then restart the agent or controller as above. Until it is fixed, keep the scheduler away from the host:

> ⚠️ **State-changing.** Disabling the compute service stops new instances landing on the host. Running instances
> are not affected.

```bash
openstack compute service set --disable --disable-reason "binding_failed on <network>" <compute-host> nova-compute
```

### Neutron cannot notify Nova

Fix the `[nova]` section of `neutron.conf` (auth URL, credentials, region, endpoint type) and restart
`neutron-server`. Verify with a test boot.

### Clean up the failed instances

> ⚠️ **State-changing.** Deleting the `ERROR` instances frees quota and Placement allocations. Confirm with the
> owner first if the instance may hold data on an attached volume (the volume itself is not deleted unless it was
> created with `delete_on_termination`).

```bash
openstack server delete <server-id>
```

## Verification

```bash
# A test boot on the affected host reaches ACTIVE within the normal time
openstack server create --flavor <flavor> --image <image> --network <network> \
  --availability-zone nova:<compute-host> vif-test
openstack server show vif-test -c status -c OS-EXT-SRV-ATTR:host
openstack port list --server vif-test -c Status      # ACTIVE
openstack server delete vif-test

# No agent or chassis missing
openstack network agent list
```

## Validity and limits

Derived from an operator's description of the provisioning path; the OpenStack release on which the incidents were
observed is not recorded. The mechanism (Nova waiting for `network-vif-plugged`, bounded by `vif_plugging_timeout`)
is stable across recent releases. OVN commands assume the Neutron OVN driver; ML2/OVS commands assume the OVS
agent. Not tested with Linux Bridge or SR-IOV ports, where binding failures have additional causes.

## Related

- [No valid host with free capacity](../scheduling/no-valid-host-with-free-capacity.md): the other common build failure, which happens before a host is selected.
- [What a VM creation traverses, and tracing it by request id](../diagnostics/what-a-vm-creation-traverses-and-tracing-by-request-id.md).
- Source: *OpenStack, the Day After Tomorrow* (S. Zaouam), chapter 5, technical note on the provisioning path.
