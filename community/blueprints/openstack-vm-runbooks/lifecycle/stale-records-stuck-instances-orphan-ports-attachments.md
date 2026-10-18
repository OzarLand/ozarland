---
title: Stale records. Instances stuck in BUILD, ERROR or deleting, orphan ports and attachments, phantom allocations
kind: runbook
status: draft
openstack_releases: [unrecorded]
components: [nova, placement, neutron, cinder, mariadb]
deployment_methods: [any]
environment:
  topology: any
  network: any
  storage: any
  os: any
risk: destructive
confirmed_by: []
upstream_refs:
  - https://docs.openstack.org/nova/latest/cli/nova-manage.html
  - https://docs.openstack.org/cinder/latest/cli/cinder-manage.html
last_verified: 2026-10-18
---

# Stale records. Instances stuck in BUILD, ERROR or deleting, orphan ports and attachments, phantom allocations

A long-lived platform accumulates records that describe nothing real: every host failure, interrupted operation and
recovery adds some. They hold quota, distort capacity, and make every investigation start with "is this record
true?". This runbook is the periodic clean-up, using project tools first and the database last.

## Symptom

One or more of:

```text
$ openstack server list --all-projects --status BUILD --long     # instances in BUILD for days
$ openstack server list --all-projects --status ERROR --long
$ openstack server list --all-projects --long | grep deleting     # task_state deleting that never completes
$ openstack port list --device-owner compute:nova --long          # ports whose device_id is a deleted instance
$ openstack volume list --all-projects --status in-use            # attached to instances that no longer exist
$ nova-manage placement audit --verbose                           # allocations for consumers that do not exist
```

Also: quota "in use" higher than what the project actually runs; `openstack hypervisor stats show` disagreeing with
the sum of running instances.

## Impact

No direct service impact, which is why it is neglected. Indirect: scheduling failures from inflated usage, users
blocked by quota, capacity planning on wrong numbers, slower incident response.

## Quick checks

```bash
# Instances in a transitional state for longer than any operation should take
openstack server list --all-projects --long -c ID -c Status -c "Task State" -c Host -c Updated \
  | awk '$4=="BUILD" || $4=="ERROR" || $6!="None"'

# Placement allocations without a matching instance
nova-manage placement audit --verbose              # read-only without --delete

# Ports whose device no longer exists (compare device_id with server list)
openstack port list --long -c ID -c "Device Owner" -c device_id -f value | awk '$2=="compute:nova"{print $3}' \
  | sort -u | while read id; do openstack server show "$id" -c id -f value >/dev/null 2>&1 || echo "orphan device_id $id"; done

# Volumes attached to a missing instance
openstack volume list --all-projects --status in-use -c ID -c "Attached to" -f value
```

**Kolla-Ansible:** `nova-manage` runs in the `nova_api` container, `cinder-manage` in `cinder_api`.

## Diagnosis

For each stale record, establish what is real before touching it:

- **Instance stuck in `BUILD`/`spawning`**: is there a libvirt domain on the host (`virsh list --all` on the host)?
  Did the build time out? Check `nova-compute.log` for the UUID. Usually safe to delete via the API.
- **Instance stuck in `deleting`**: the compute received the delete and never finished (host died, storage hung).
  Check the host and the domain. If the host is gone, a deletion will complete once Nova considers it `down`
  (local delete), or needs `reset-state` first.
- **Instance in `ERROR`**: read `fault`. Many are simply failed builds (delete them). Some are real instances whose
  last operation failed (resize, migration): the domain may be running and healthy; reset the state instead of
  deleting.
- **Orphan port**: `device_id` points to a deleted server. Confirm the server is really deleted
  (`openstack server show <id>` returns not found; `nova-manage` shows it archived) before deleting the port.
- **Volume attached to a missing instance**: Cinder has an attachment the instance does not. Compare
  `openstack volume attachment list` with `openstack server show` on the instance, if it exists.
- **Phantom allocation**: `placement audit` lists allocations whose consumer (instance) no longer exists, or exists
  on a different host than the allocation says (left over from a failed migration or evacuation).

## Possible causes

Interrupted operations (host failure during build, delete, resize or migration), control-plane outages mid-request,
message-bus incidents that lost RPC calls, manual interventions that bypassed the API. There is rarely a single
cause; the clean-up is routine maintenance.

## Resolution

Work with project tools in this order. Take a database backup before anything that touches the database directly.

### Instances: reset state, then delete through the API

> ⚠️ **State-changing.** `reset-state` only changes Nova's record; it does not touch the hypervisor. Setting
> `--state active` on an instance whose domain does not run gives users a false picture; setting `--state error`
> then deleting is the usual path for a truly dead instance.

```bash
openstack server set --state error <server-id>      # make it deletable
openstack server delete <server-id>
# Instance whose domain is actually running fine after a failed operation:
openstack server set --state active <server-id>
```

If the delete hangs because the host is gone, Nova performs a local delete once the compute service is `down`; if
the service still reports `up` from a host that lost its storage, fix or fence the host first.

### Placement: audit, then heal or delete

> ⚠️ **State-changing.** `heal_allocations` creates or corrects allocations for existing instances; `audit --delete`
> removes allocations whose consumer does not exist. Both change what the scheduler sees. Run `audit` without
> `--delete` first and read the list.

```bash
nova-manage placement audit --verbose
nova-manage placement audit --verbose --delete
nova-manage placement heal_allocations --verbose
```

### Ports and volumes

> ⚠️ **State-changing.** Deleting a port frees its IP; detaching or resetting a volume attachment changes its
> status. Confirm the owning instance is gone first.

```bash
openstack port delete <port-id>

# Volume still "in-use" for an instance that no longer exists
openstack volume attachment list --volume <volume-id>
openstack volume attachment delete <attachment-id>
# Older Cinder APIs: openstack volume set --state available --detached <volume-id>   (check the data is not in use!)
```

### Archive and purge soft-deleted rows

> ⚠️ **State-changing.** Moves soft-deleted rows to the shadow tables, then purges them. Reduces database size and
> query time. Irreversible once purged; it only touches rows already marked deleted.

```bash
nova-manage db archive_deleted_rows --until-complete --verbose
nova-manage db purge --all --verbose          # or --before <date>
cinder-manage db purge <days>
```

### Direct database surgery, last resort

> 🛑 **Destructive.** Direct edits bypass every consistency check the services perform. Use only when no API or
> `*-manage` command covers the case (for example a `block_device_mapping` row for a volume Cinder does not know).
> Precondition: full database backup, the exact row identified by UUID, one record at a time, verification after
> each. Cannot be undone without the backup.

Prefer an upstream bug report and a project tool over a repeatable SQL fix. If you must, write down the query, the
row before and after, and the reason, in the change record.

## Verification

```bash
openstack server list --all-projects --long | awk '$4=="BUILD" || $6!="None"'   # empty or explainable
nova-manage placement audit --verbose                                         # no orphan allocations
openstack quota show --usage <project>                                        # matches reality
openstack hypervisor stats show                                               # consistent with instance counts
```

## Validity and limits

Derived from an operator's clean-up of a long-lived platform; release not recorded. `nova-manage placement audit`
exists since Train (20.0); `heal_allocations` since Rocky (18.0). Command flags change between releases: check
`nova-manage --help` on your platform. Not covered: Octavia, Heat and Magnum resources that hold Nova and Neutron
objects, which have their own clean-up logic.

## Related

- [No valid host with free capacity](../scheduling/no-valid-host-with-free-capacity.md): where phantom allocations show up first.
- [Compute host failure: fence before evacuate](../recovery/compute-host-failure-fence-before-evacuate.md): the main producer of stale records.
- Source: *OpenStack, the Day After Tomorrow* (S. Zaouam), chapter 10, "The state that lies".
