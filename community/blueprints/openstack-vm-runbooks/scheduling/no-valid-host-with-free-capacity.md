---
title: No valid host was found, although capacity exists
kind: runbook
status: draft
openstack_releases: [unrecorded]
components: [nova, placement]
deployment_methods: [any]
environment:
  topology: any multinode
  network: any
  storage: any
  os: any
risk: state-changing
confirmed_by: []
upstream_refs:
  - https://docs.openstack.org/nova/latest/admin/cells.html
  - https://docs.openstack.org/nova/latest/cli/nova-manage.html
  - https://docs.openstack.org/osc-placement/latest/
last_verified: 2026-10-18
---

# No valid host was found, although capacity exists

Instances fail to schedule while hypervisors show free CPU, memory and disk. The classic cause on a platform that
just added hosts is a compute node that exists but is not mapped to a cell; the others are Placement inventory,
disabled services and filters.

## Symptom

```text
$ openstack server show <server-id> -c status -c fault
status | ERROR
fault  | {'code': 500, 'message': 'No valid host was found. There are not enough hosts available.', ...}
```

`OS-EXT-SRV-ATTR:host` is empty: no host was ever selected. Meanwhile `openstack hypervisor list` shows hosts with
room.

## Impact

Provisioning fails for some or all flavors, projects or availability zones. Running instances are unaffected.
Operators waste capacity they paid for; users see random failures if only some hosts are affected.

## Quick checks

```bash
# 1. Are all compute services up and enabled?
openstack compute service list --service nova-compute -c Host -c Zone -c Status -c State

# 2. Are all compute hosts mapped to a cell? (run where nova-manage and nova.conf are available)
nova-manage cell_v2 list_hosts
# Compare with the hosts in step 1. A host present in step 1 and absent here is unmapped.

# 3. Does Placement have candidates for the flavor's resources? (needs the osc-placement plugin)
openstack allocation candidate list --resource VCPU=<vcpus> --resource MEMORY_MB=<ram> --resource DISK_GB=<disk>

# 4. What did the scheduler say?
#    nova-scheduler.log for the request id of the failed boot (openstack server event list <server-id>)
```

**Kolla-Ansible:** `nova-manage` runs inside the `nova_api` container (`docker exec -it nova_api nova-manage ...`).

## Diagnosis

### Unmapped host

`nova-scheduler.log` or `nova-conductor.log` for the request id shows the host being selected, then the conductor
failing with:

```text
Host '<host>' is not mapped to any cell
```

The scheduler picked the host (it exists in Placement) but the conductor could not find which cell database holds
it. This happens when `nova-manage cell_v2 discover_hosts` was not run after adding the host and
`[scheduler] discover_hosts_in_cells_interval` is at its default of `-1` (disabled).

### Placement has no candidates

If step 3 returns nothing, look at the providers:

```bash
openstack resource provider list
openstack resource provider inventory list <rp-uuid>      # capacity, reserved, allocation_ratio
openstack resource provider usage show <rp-uuid>           # what Placement believes is used
```

Usual findings: `allocation_ratio` lower than you think (for example `cpu_allocation_ratio` left at 1.0 on new
hosts), `reserved` too high, usage inflated by allocations of instances that no longer exist (see
[Stale records](../lifecycle/stale-records-stuck-instances-orphan-ports-attachments.md)), or the flavor asks for a
trait or a resource class (PCPU, a custom class) the hosts do not expose.

### Filters rejected every candidate

The scheduler log line `Filter <Name> returned 0 hosts` names the filter. Common ones: `AggregateInstanceExtraSpecsFilter`
(flavor extra specs versus aggregate metadata), `AvailabilityZoneFilter` (the requested zone has no enabled host),
`NUMATopologyFilter` (pinned or hugepage flavor with no matching host), `ComputeFilter` (service disabled or down),
`ImagePropertiesFilter` (image requires a property the hosts lack).

### Service disabled or down

Step 1 shows `disabled` (someone disabled it, read the reason) or `down` (the service stopped reporting: host
problem, or the service lost its message bus connection).

## Possible causes

| Cause | How to tell |
|---|---|
| Host not mapped to a cell | Conductor log: `is not mapped to any cell`; host missing from `cell_v2 list_hosts` |
| Placement inventory or ratios | `allocation candidate list` empty; inventory shows low ratio or high reserved |
| Stale allocations inflating usage | `usage show` higher than instances actually on the host; `nova-manage placement audit` reports orphans |
| Filter rejects everything | Scheduler log names the filter returning 0 hosts |
| Compute service disabled or down | `compute service list` |
| Flavor asks for a resource class or trait no host has | Candidate list empty for that flavor only; `resource provider trait list` |

## Resolution

### Map the host

> ⚠️ **State-changing.** Writes the host mapping to the Nova API database. Reversible (`delete_host`). No impact on
> running instances.

```bash
nova-manage cell_v2 discover_hosts --verbose
nova-manage cell_v2 list_hosts
```

Consider setting `[scheduler] discover_hosts_in_cells_interval = 300` on `nova-scheduler` so that new hosts are
mapped automatically. Verify how your deployment tool handles this before changing the file by hand.

### Fix inventory or ratios

Set `cpu_allocation_ratio`, `ram_allocation_ratio`, `disk_allocation_ratio` and `reserved_host_*` in the
`[DEFAULT]` or `[compute]` section of `nova.conf` on the compute host, restart `nova-compute`, and check the
inventory again. Changing a ratio directly in Placement is overridden by the compute on its next update unless the
`initial_*_allocation_ratio` logic applies; prefer the Nova configuration.

### Heal stale allocations

See [Stale records](../lifecycle/stale-records-stuck-instances-orphan-ports-attachments.md); in short,
`nova-manage placement audit` to list, `nova-manage placement heal_allocations` to repair, with the warnings there.

### Re-enable a service

> ⚠️ **State-changing.** Instances will be scheduled on the host again. Make sure the reason it was disabled no
> longer applies.

```bash
openstack compute service set --enable <compute-host> nova-compute
```

## Verification

```bash
openstack allocation candidate list --resource VCPU=<vcpus> --resource MEMORY_MB=<ram> --resource DISK_GB=<disk> | head
openstack server create --flavor <flavor> --image <image> --network <network> sched-test
openstack server show sched-test -c status -c OS-EXT-SRV-ATTR:host
openstack server delete sched-test
```

## Validity and limits

Derived from an operator's account of "capacity exists but nothing lands on it"; release not recorded. Cells v2
and Placement have been mandatory since Pike (16.0), so the mapping mechanism applies to every current release.
The `osc-placement` plugin is required for the `openstack resource provider` and `allocation candidate` commands.
Not covered: scheduling failures specific to Ironic bare-metal nodes.

## Related

- [Instance stuck in BUILD waiting for vif-plugged](../lifecycle/instance-stuck-in-build-waiting-for-vif-plugged.md): the failure that happens after a host was selected.
- [Stale records](../lifecycle/stale-records-stuck-instances-orphan-ports-attachments.md).
- Source: *OpenStack, the Day After Tomorrow* (S. Zaouam), chapter 5.
