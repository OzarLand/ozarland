# Risk warnings

Readers follow runbooks in a hurry, often in production. Every command must tell them, before they run it, what it
can do to the platform.

## Three levels

| Level | Meaning | Marker |
|---|---|---|
| **Read-only** | Observes state. Safe to run at any time. (`openstack server show`, `docker logs`, `ovs-vsctl show`) | No marker needed; the section heading "Quick checks" or "Diagnosis" implies it |
| **State-changing** | Changes the platform in a reversible or bounded way. (restarting a service, disabling a compute service, resetting an instance state) | `> ⚠️ **State-changing.**` followed by what changes and what is affected |
| **Destructive** | Can lose data, end workloads or affect many users; not reversible by simply undoing the command. (deleting a volume, `nova-manage db` operations, evacuating a host, resetting RabbitMQ state, anything touching the database directly) | `> 🛑 **Destructive.**` followed by what can be lost, who is affected, the precondition to check, and the backup or snapshot to take first |

## How to write a warning

Put it immediately above the command, in a blockquote, and answer four questions: what changes, who is affected,
what must be true before running it, how to undo it or why it cannot be undone.

```markdown
> 🛑 **Destructive.** Deletes the block device mapping record from the Nova database. Affects this instance only.
> Run only after confirming with `openstack volume show <volume-id>` that the attachment no longer exists on
> the Cinder side, and after a database backup. Cannot be undone without restoring the backup.

```sql
DELETE FROM block_device_mapping WHERE instance_uuid = '<instance-uuid>' AND volume_id = '<volume-id>';
```
```

## Rules

- The **front matter `risk` field** carries the highest level present in the page, so that a page that contains one
  destructive step is marked destructive as a whole.
- **Production impact is called out even when reversible.** Restarting `neutron-openvswitch-agent` is state-changing
  and briefly interrupts data-plane changes; say so.
- **Direct database edits are always destructive**, however small. Prefer the API or the project's `*-manage`
  tools, and say when none exists.
- **Never hide a destructive step inside a script.** If a runbook provides a script, the destructive commands are
  listed and warned about in the page as well.
- Reviewers may **refuse to merge** a page whose destructive commands are not flagged. This is one of the few hard
  rules the community has.
