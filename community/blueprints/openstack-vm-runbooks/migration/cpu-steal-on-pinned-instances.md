---
title: CPU steal time on instances with dedicated (pinned) CPUs. Live migration moves the symptom, not the cause
kind: runbook
status: draft
openstack_releases: [unrecorded]
components: [nova, libvirt, qemu]
deployment_methods: [any]
environment:
  topology: compute hosts with cpu_dedicated_set
  network: any
  storage: any
  os: any
risk: state-changing
confirmed_by: []
upstream_refs:
  - https://docs.openstack.org/nova/latest/admin/cpu-topologies.html
  - https://docs.openstack.org/releasenotes/nova/train.html
last_verified: 2026-10-18
---

# CPU steal time on instances with dedicated (pinned) CPUs. Live migration moves the symptom, not the cause

Instances created with `hw:cpu_policy=dedicated` should not see steal time: each guest vCPU owns a host CPU. When
they do, live-migrating them makes the symptom disappear for a while, which turns live migration into the
response. The symptom comes back, the same workloads get migrated again and again, each migration carrying its own
risk. The cause is on the host, and it travels with the configuration.

## Symptom

Inside the guest, `top` or `/proc/stat` shows non-zero steal (`st`) on a pinned instance:

```text
%Cpu(s): 71.2 us,  3.1 sy,  0.0 ni, 18.0 id,  0.0 wa,  0.0 hi,  0.4 si,  7.3 st
```

Latency-sensitive workloads (telco, trading, real-time) report jitter. The instance's flavor has
`hw:cpu_policy=dedicated`. After a live migration, steal drops to zero, then returns days or weeks later on the new
host.

## Impact

Performance degradation of exactly the workloads that paid for isolation. Repeated live migrations add risk: each
one pauses the instance briefly and, on older releases, could itself produce an invalid pinning on the destination
(see Validity).

## Quick checks

On the compute host running the instance:

```bash
# 1. Which host CPUs the guest vCPUs are pinned to, and where the emulator threads run
virsh vcpupin <instance-name>              # instance-name is OS-EXT-SRV-ATTR:instance_name, e.g. instance-0000abcd
virsh emulatorpin <instance-name>
virsh dumpxml <instance-name> | sed -n '/<cputune>/,/<\/cputune>/p'

# 2. What else runs on those CPUs
ps -eLo pid,tid,psr,comm | awk '$3==<host-cpu>'      # for each pinned host CPU
cat /proc/interrupts | awk '{print $1, $<host-cpu+2>}' | sort -k2 -n | tail

# 3. Nova's view of the dedicated set
grep -E 'cpu_dedicated_set|cpu_shared_set|vcpu_pin_set' /etc/nova/nova.conf     # Kolla-Ansible: /etc/kolla/nova-compute/nova.conf
```

## Diagnosis

Nova pins **the guest's vCPUs**, nothing else. Two things routinely share "dedicated" CPUs:

1. **Host processes.** Nova does not keep the kernel's own threads, interrupt handlers, KSM, or daemons off the
   CPUs in `cpu_dedicated_set`. That isolation must be arranged on the host: `isolcpus`, `nohz_full`,
   `rcu_nocbs` kernel parameters, a tuned profile (`cpu-partitioning`, `realtime-virtual-host`), IRQ affinity.
   Check `cat /sys/devices/system/cpu/isolated` and `/proc/cmdline`.
2. **The instance's own emulator threads.** By default QEMU's emulator (I/O) thread may run on the instance's
   pinned CPUs. `hw:emulator_threads_policy=share` moves it to `cpu_shared_set`; `isolate` gives it an extra
   dedicated CPU. Without either, the emulator thread steals from the vCPUs it serves.

Only after those two: **overlapping pinning** between instances (two domains pinned to the same host CPU, visible by
comparing `virsh vcpupin` across all domains), and a **mismatch between Nova's belief and the host** (for example
`cpu_dedicated_set` changed on a host that already runs pinned instances, or a migration performed by a release
that did not recalculate the mapping).

Why migration "fixes" it: the destination host may happen to have less background activity on the chosen CPUs, or a
different interrupt distribution. The configuration gap is identical, so the symptom returns.

## Possible causes

| Cause | How to tell |
|---|---|
| Host threads and IRQs not isolated from the dedicated set | `/sys/devices/system/cpu/isolated` empty; `ps -eLo psr` shows kernel threads or daemons on pinned CPUs; interrupts counted on them |
| Emulator threads sharing the pinned CPUs | `virsh emulatorpin` equals the vCPU set; flavor lacks `hw:emulator_threads_policy` |
| Overlapping pinning between instances | Two domains' `vcpupin` share a host CPU |
| Nova/host mismatch | `cpu_dedicated_set` differs from what the domains use; history of migrations on pre-Train releases |

## Resolution

Stop migrating first. The book's team did exactly that: accepted a bounded amount of steal while investigating,
rather than relocating the symptom.

### Isolate the host CPUs

> ⚠️ **State-changing.** Kernel parameters and tuned profiles need a host reboot, hence moving or stopping its
> instances (see [Moving instances off a host](moving-instances-off-a-host-for-maintenance.md)). Do one host,
> measure, then roll out.

Configure the isolation the hardware vendor and your OS document for virtualisation hosts (`isolcpus=`, `nohz_full=`,
`rcu_nocbs=` matching `cpu_dedicated_set`, or a tuned profile), pin IRQs away from the set, and keep housekeeping
CPUs for the host in `cpu_shared_set`.

### Move the emulator threads

> ⚠️ **State-changing.** Changing flavor extra specs affects new instances and resized ones only. Existing instances
> need a resize (to the same flavor is not enough; use a new flavor) or a rebuild to pick up the new policy.

```bash
openstack flavor set --property hw:emulator_threads_policy=share <flavor>
# and make sure every host has a [compute] cpu_shared_set for them to land on
```

### Fix overlapping pinning or mismatches

> ⚠️ **State-changing.** Moving an instance changes its pinning. Live-migrate or cold-migrate one instance per
> overlap to a host with free dedicated CPUs, then verify with `virsh vcpupin` on the destination.

## Verification

```bash
# Inside the guest, over a representative period
vmstat 5 12            # st column stays at 0
# On the host
virsh vcpupin <instance-name>; virsh emulatorpin <instance-name>
ps -eLo psr,comm | awk '$1==<pinned-cpu>' | sort | uniq -c    # only the instance's vCPU threads
```

Verify over days, not minutes: the symptom was intermittent.

## Validity and limits

Derived from an operator's incident on a platform with dedicated-CPU workloads; release not recorded. Two release
facts matter: live migration of instances with a NUMA topology (including pinned CPUs) only became NUMA-aware in
Train (Nova 20.0); on Stein with the `enable_numa_live_migration` workaround, and earlier, the instance moved
without recalculating the guest-to-host mapping and could itself create overlapping pinning. `hw:emulator_threads_policy=share`
with `cpu_shared_set` dates from Stein. The host-isolation steps depend on the OS and hardware; check your vendor's
guidance for real-time or NFV hosts.

## Related

- [Moving instances off a host for planned maintenance](moving-instances-off-a-host-for-maintenance.md).
- Source: *OpenStack, the Day After Tomorrow* (S. Zaouam), chapter 15, "From the field" and technical note on pinned CPUs.
