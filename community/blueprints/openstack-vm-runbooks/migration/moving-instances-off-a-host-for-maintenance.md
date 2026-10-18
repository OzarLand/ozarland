---
title: Moving instances off a compute host for planned maintenance (patching, reboot, hardware)
kind: runbook
status: draft
openstack_releases: [unrecorded]
components: [nova, libvirt, qemu]
deployment_methods: [any]
environment:
  topology: any multinode
  network: any
  storage: shared or local; determines live migration mode
  os: any
risk: destructive
confirmed_by: []
upstream_refs:
  - https://docs.openstack.org/nova/latest/admin/live-migration-usage.html
  - https://docs.openstack.org/nova/latest/admin/configuring-migrations.html
  - https://docs.openstack.org/nova/latest/admin/migration.html
last_verified: 2026-10-18
---

# Moving instances off a compute host for planned maintenance

Which operation applies to which instance, what must be true before each, and the capacity trap of a patching
campaign: once some hosts are patched, instances can move onto them but not back.

## Symptom

Not a failure: a planned need. "Host X must be rebooted for an OS, kernel, libvirt or QEMU patch, or for hardware
work, and it runs N instances."

## Impact

Live migration keeps instances running (brief pause); cold migration and restarts stop them. The real impact is
decided per workload, and Nova cannot tell you which workload tolerates what. Collect that from the owning teams
before the campaign, as a table: instance or project, business criticality, acceptable downtime, contact.

## Quick checks

```bash
# 1. What runs on the host
openstack server list --all-projects --host <host> --long -c ID -c Name -c Status -c Flavor -c Project

# 2. Which instances cannot be live-migrated (PCI passthrough, SR-IOV direct ports, vGPU, special flavors)
for s in $(openstack server list --all-projects --host <host> -f value -c ID); do
  echo "== $s"; openstack server show $s -c flavor -c OS-EXT-SRV-ATTR:instance_name -f value
  openstack port list --server $s -c ID -c "VNIC Type" -f value | grep -v normal
done
# On the host: virsh dumpxml <instance-name> | grep -E 'hostdev|mdev'   -> passthrough or vGPU present

# 3. Capacity: where could they go?
openstack hypervisor list --long          # vCPUs and memory used/total per host
openstack allocation candidate list --resource VCPU=<largest flavor vcpus> --resource MEMORY_MB=<largest flavor ram>

# 4. Version compatibility between source and destination
#    on each host: virsh version ; qemu-system-x86_64 --version ; the CPU model in nova.conf [libvirt] cpu_mode/cpu_models
```

## Diagnosis: choosing the operation per instance

| Instance | Operation | Why |
|---|---|---|
| Normal instance, shared storage or boot-from-volume | Live migration | Keeps it running; disks are not copied |
| Normal instance, local disk | Live block migration (`--block-migration`) | Copies the disk over the network: load on network and storage, longer |
| Memory-intensive, pages change faster than they copy | Live migration with auto-converge or post-copy enabled, else cold migration | Without them the migration never converges |
| PCI passthrough, SR-IOV direct port | Cold migration or restart | Live migration of these is unsupported or version-dependent |
| vGPU | Cold migration or restart on releases without mediated-device migration | Check your release |
| Workload the owner says may restart | Stop, patch, start, or cold migrate | Cheapest; needs no spare capacity |

**Direction matters.** Migration from a newer libvirt/QEMU to an older one is not supported. Once a host is
patched, instances can move onto it but not back off it to an unpatched host. The order of patching therefore
decides where instances can go: plan the sequence so that patched capacity is available to receive from the next
host. The destination's CPU model must also be compatible with the source's (`cpu_mode`, `cpu_models`).

**Patching protects only restarted or migrated instances.** An instance that keeps running on the old QEMU binary
is not patched, even if the host package is. A live migration (which starts a new QEMU process on the destination)
or a restart is required for the fix to apply to the instance.

## Resolution

### Step 1: stop new placements on the host

> ⚠️ **State-changing.** No new instances land on the host; existing ones unaffected.

```bash
openstack compute service set --disable --disable-reason "maintenance <ticket> <date>" <host> nova-compute
```

### Step 2: live-migrate what can be live-migrated

> ⚠️ **State-changing, production impact.** The instance pauses briefly at switchover; network and storage carry
> the memory (and disk, for block migration) copy. Migrate a few at once, not the whole host, and watch the
> destination. Memory-heavy instances may never converge: set a timeout and be ready to abort.

```bash
# Let the scheduler pick a destination
openstack server migrate --live-migration <server-id>
# Or choose it (checked by the scheduler since Rocky unless --os-compute-api-version < 2.30)
openstack server migrate --live-migration --host <destination-host> <server-id>
# Local disks
openstack server migrate --live-migration --block-migration <server-id>

# Watch
openstack server migration list --server <server-id>
openstack server show <server-id> -c status -c OS-EXT-STS:task_state -c OS-EXT-SRV-ATTR:host
# Abort one that does not converge (migration id from the list above)
openstack server migration abort <server-id> <migration-id>
# Force completion with post-copy if enabled ([libvirt] live_migration_permit_post_copy = true)
openstack server migration force complete <server-id> <migration-id>
```

### Step 3: cold-migrate or restart the rest, as agreed with the owners

> 🛑 **Destructive for the workload's availability.** Cold migration stops the instance, moves it, and leaves it
> in `VERIFY_RESIZE` until confirmed; a restart interrupts the service. Precondition: the owner agreed to the
> downtime window. Undo: `openstack server resize revert` before confirming.

```bash
openstack server migrate <server-id>                 # cold migration
openstack server show <server-id> -c status          # VERIFY_RESIZE
openstack server resize confirm <server-id>          # newer clients: openstack server migration confirm
# or simply
openstack server stop <server-id>   # patch the host ... openstack server start <server-id>
```

### Step 4: patch and reboot the host, then re-enable

> ⚠️ **State-changing.** Re-enabling makes the host a destination again, which is exactly what the next host in the
> sequence needs.

```bash
openstack compute service set --enable <host> nova-compute
```

## Verification

```bash
openstack server list --all-projects --host <host>                      # empty before reboot
openstack compute service list --host <host>                            # up and enabled after
openstack server show <server-id> -c status -c OS-EXT-SRV-ATTR:host    # ACTIVE on the new host
openstack server migration list --server <server-id>                    # completed, none stuck in running
# On the destination: the instance's QEMU process is the new binary
ps -o pid,lstart,cmd -C qemu-system-x86_64 | grep <instance-name>
```

Check with the owner that the application is healthy after a cold migration or restart. For the campaign as a
whole: every host rebooted, every instance either migrated after its host was patched or restarted.

## Validity and limits

Derived from an operator's patching campaign on a platform of up to several hundred hosts, where spare capacity
did not allow live-migrating everything and the owning teams supplied the criticality that Nova cannot know.
Release not recorded. Command names for cold-migration confirmation changed across python-openstackclient
versions. Live migration constraints (PCI, SR-IOV, vGPU, CPU model, version direction) are release-dependent:
check the Nova documentation of your release. Capacity rule of thumb from the same source: spare capacity must
exist per failure domain (rack, availability zone), not once for the whole platform.

## Related

- [Compute host failure: fence before evacuate](../recovery/compute-host-failure-fence-before-evacuate.md): never use evacuation on a host that may still be running its instances.
- [CPU steal on pinned instances](cpu-steal-on-pinned-instances.md): pinned instances need extra care when moved.
- Source: *OpenStack, the Day After Tomorrow* (S. Zaouam), chapter 20.
