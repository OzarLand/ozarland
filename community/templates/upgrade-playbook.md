---
title: <e.g. "Upgrading from 2024.2 to 2025.1 with Kolla-Ansible">
kind: playbook
status: draft
openstack_releases: [<from>, <to>]
components: [<all>]
deployment_methods: [<kolla-ansible>]
environment:
  topology: <...>
  network: <...>
  storage: <...>
  os: <before -> after, if the OS changes too>
risk: destructive
confirmed_by: []
upstream_refs:
  - <release notes of the target release>
  - <deployment tool upgrade guide>
last_verified: <YYYY-MM-DD>
---

# <Title>

> 🛑 An upgrade is a destructive operation on the whole platform. This playbook describes what one team did on one
> platform. Check the upstream release notes and your deployment tool's upgrade guide for your own path before
> following any step.

## Upgrade path

<!-- From which release to which, in how many steps. State explicitly whether the path is documented upstream as supported, with the link, or whether it is something you did without that guarantee. Never present a path as supported without a reference. -->

## Preparation

<!-- Timeline, communication, maintenance window, team, rollback decision points. -->

## Prerequisites and pre-checks

<!-- What must be true before starting: versions, OS, backups, free space, healthy clusters (Galera, RabbitMQ, Ceph), no pending migrations, deprecated options removed from config. Commands to check each. -->

## Differences between the releases that mattered

<!-- Configuration options renamed or removed, defaults changed, services added or dropped, database migrations of note, image or driver changes. -->

## Procedure

<!-- The steps as run, with the commands, where they run, and the expected duration. Mark every destructive step. -->

### Step 1: <...>

## Health checks

### Before

### During

### After

## Problems met and how they were resolved

<!-- One subsection per problem. Link to runbooks where they exist. -->

## Rollback

<!-- What could be rolled back and how, what could not (database migrations, data format changes), and the recovery plan beyond that point. Be honest about the limits. -->

## Outcome

<!-- Duration, downtime, what broke, what surprised you. -->

## Validity and limits

<!-- This platform's specifics; what someone with a different setup should expect to differ. -->

## Related
