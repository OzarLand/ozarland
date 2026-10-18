---
title: <Symptom, as the operator sees it, e.g. "Instance stuck in deleting state">
kind: runbook
status: draft
openstack_releases: [<2025.1>]
components: [<nova>, <neutron>]
deployment_methods: [<kolla-ansible>]
environment:
  topology: <e.g. multinode, 3 controllers>
  network: <ovn | ovs | linuxbridge | other>
  storage: <ceph-rbd | lvm | nfs | other>
  os: <e.g. ubuntu-24.04>
risk: <read-only | state-changing | destructive>
confirmed_by: []
upstream_refs: []
last_verified: <YYYY-MM-DD>
---

# <Title>

## Symptom

<!-- What you see. Exact messages, states, CLI output. Redacted. -->

```text
$ openstack server show <server-id> -c status -c task_state
...
```

## Impact

<!-- Who and what is affected. One instance? All instances on a host? The whole platform? Data at risk? -->

## Quick checks

<!-- 3 to 5 read-only commands that confirm this is the problem described here. Say where each runs. -->

```bash
openstack server show <server-id>
```

## Diagnosis

<!-- How to narrow down the cause. Commands, logs, what to look for. Group by component. -->

### <Component, e.g. Nova>

### <Component, e.g. Neutron>

## Possible causes

<!-- One subsection per cause, with how to tell it apart from the others. -->

### Cause 1: <name>

### Cause 2: <name>

## Resolution

<!-- One subsection per cause. Every state-changing or destructive command carries its warning. -->

### For cause 1

> ⚠️ **State-changing.** <What changes, what is affected, how to undo.>

```bash
<command>
```

### For cause 2

> 🛑 **Destructive.** <What can be lost, who is affected, what must be checked first, backup to take, why it cannot be undone.>

```bash
<command>
```

## Verification

<!-- Commands and expected output proving the problem is gone and nothing else broke. -->

## Validity and limits

<!-- Where observed, what was not tested, what is uncertain. Be concrete. -->

## Related

<!-- Other runbooks, upstream bugs and docs, the discussion where this was investigated. -->
