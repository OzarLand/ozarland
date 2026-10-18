---
title: Compute host unreachable, instances down. Fence before you evacuate
kind: runbook
status: draft
openstack_releases: [unrecorded]
components: [nova, libvirt, cinder, ceph]
deployment_methods: [any]
environment:
  topology: any multinode
  network: any
  storage: shared instance storage or boot-from-volume for evacuation to preserve disks
  os: any
risk: destructive
confirmed_by: []
upstream_refs:
  - https://docs.openstack.org/nova/latest/admin/evacuate.html
  - https://docs.openstack.org/nova/latest/admin/node-down.html
last_verified: 2026-10-18
---

# Compute host unreachable, instances down. Fence before you evacuate

`nova evacuate` rebuilds an instance on another host and reuses its volumes. Nova requires the source compute
service to be reported `down` first, but Nova cannot know whether the host is really dead or merely unreachable
from the control plane. Evacuating from a host that is still running the instances produces two copies of each
server writing to the same volume. The precondition is fencing, not the missing heartbeat.

## Symptom

```text
$ openstack compute service list --service nova-compute -c Host -c State
| compute-07 | down |

$ openstack server list --all-projects --host compute-07 -c ID -c Status
| ...        | ACTIVE |      <- Nova still believes they run; users say they are unreachable
```

Monitoring shows the host unreachable (no ping, no SSH, no agent). Users report their instances on that host are
not responding.

## Impact

Every instance on the host is down or unreachable. Nothing else is affected unless the host also ran a network
node role. The risk during recovery is worse than the outage: a wrong evacuation corrupts volumes.

## Quick checks

```bash
# 1. Nova's view of the host and when it last reported
openstack compute service list --service nova-compute --host <host> --long

# 2. Which instances and which volumes are involved
openstack server list --all-projects --host <host> --long -c ID -c Name -c Status -c Networks
openstack volume list --all-projects --status in-use -c ID -c "Attached to" | grep -F "<instance-id>"

# 3. Can the control plane reach the host at all?
ping -c 3 <host>             # management network
ssh <host> uptime            # if it answers, the host is NOT dead; stop here and diagnose the service instead
```

If the host answers on the management network, this is a `nova-compute` or message-bus problem, not a dead host.
Do not evacuate. Restart `nova-compute` and investigate its connection to RabbitMQ.

## Diagnosis

The question to answer is "is the host powered off or isolated?", and the platform cannot answer it. Use a channel
that does not depend on the host's network stack:

- **Out-of-band management** (IPMI, iDRAC, iLO, BMC): power state, console. This is the authoritative source.
- **Switch side**: is the host's port up, is traffic flowing? A host that is up with a dead management NIC may still
  be running instances and serving them on the data-plane network.
- **Storage side**: with Ceph, `ceph osd blocklist ls` and client sessions can show whether the host's libvirt
  clients still hold RBD images open (`rbd status <pool>/<image>` lists watchers).

A host that is "up" by any of these channels is isolated, not dead. Instances may still be running on it.

## Possible causes

| Cause | How to tell |
|---|---|
| Hardware failure, host powered off | Out-of-band interface shows powered off or a hardware fault |
| Kernel panic or hang | Console shows a panic; power state is on |
| Management network isolation | Host reachable from out-of-band console; instances still running; data plane may be fine |
| `nova-compute` crashed or lost its bus connection | Host reachable over SSH; only the service is down |

## Resolution

### Step 1: fence

> 🛑 **Destructive.** Powering off the host ends every instance still running on it, if any. It is the only way to
> make evacuation safe. Affects all instances on this host. Precondition: you have decided the host must be taken
> out; the instances are already unavailable to users or the risk of split-brain outweighs the remaining service.
> Cannot be undone, but the instances will be rebuilt on other hosts in step 3.

Power off through the out-of-band interface and confirm the power state:

```bash
ipmitool -I lanplus -H <bmc-address> -U <user> -P '<password>' chassis power off
ipmitool -I lanplus -H <bmc-address> -U <user> -P '<password>' chassis power status
```

If out-of-band management is unavailable, isolate the host at the switch (shut its ports) so it cannot write to
storage or serve traffic. Isolation at the switch is weaker than power-off (the host may still write to local
disks) but prevents the double-writer problem on shared storage.

### Step 2: keep the scheduler away from the host

> ⚠️ **State-changing.** Prevents new instances from being placed on the host when it returns.

```bash
openstack compute service set --disable --disable-reason "fenced <date>, hardware failure" <host> nova-compute
```

### Step 3: evacuate

> 🛑 **Destructive.** Evacuation rebuilds the instance on another host. With shared instance storage or
> boot-from-volume, the disk is preserved. With local ephemeral storage, the instance is rebuilt from its image and
> **the ephemeral disk content is lost**. Check each instance's storage before evacuating. Precondition: step 1
> done; Nova reports the compute service `down`.

```bash
# One instance; omit --host to let the scheduler choose
openstack server evacuate --host <destination-host> <server-id>
# Older clients: nova evacuate [--on-shared-storage] <server-id> [<destination-host>]
```

To evacuate every instance of the host in one go, check whether your deployment provides `nova host-evacuate`
(legacy client) or script a loop over the list from the quick checks. Evacuate in batches on a large host: each
rebuild loads the destination's storage and network.

Automation that evacuates on a lost heartbeat (Masakari, Pacemaker fence agents, home-made scripts) must perform
step 1 itself, or it will one day destroy the workload it was meant to save.

### Step 4: when the host comes back

Nova handles a returning evacuated host: on startup, `nova-compute` finds the evacuation migration records and
destroys the local copies of the evacuated instances. Do not start `nova-compute` on the host before confirming the
evacuations completed, and keep the service disabled until the host is diagnosed.

## Verification

```bash
# Every instance has a new host and is ACTIVE
openstack server list --all-projects --long -c ID -c Status -c Host | grep -F "<previous-host>"   # should be empty
openstack server show <server-id> -c status -c OS-EXT-SRV-ATTR:host

# Volumes are attached to the rebuilt instances, once
openstack volume show <volume-id> -c status -c attachments

# Migration records
openstack server migration list --type evacuation --status done

# The source host is still disabled
openstack compute service list --host <previous-host>
```

Reach a sample of the evacuated instances from the network and check their application state; a rebuilt instance
boots from scratch and may need its services started.

## Validity and limits

Derived from a real incident described by an operator: the team refused to evacuate on the strength of a missing
heartbeat, confirmed the host's state through its out-of-band interface, shut it down, and only then evacuated.
Release not recorded. The commands assume the libvirt driver. Evacuation semantics for local storage, and the
behaviour of a returning host, should be checked against the Nova documentation of your release.

## Related

- [Moving instances off a host for planned maintenance](../migration/moving-instances-off-a-host-for-maintenance.md): the planned counterpart, where the host is healthy.
- [Stale records](../lifecycle/stale-records-stuck-instances-orphan-ports-attachments.md): what an interrupted evacuation leaves behind.
- Source: *OpenStack, the Day After Tomorrow* (S. Zaouam), chapter 10, "Unplanned host failure".
