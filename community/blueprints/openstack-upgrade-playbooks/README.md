[← OzarLand home](https://github.com/OzarLand/ozarland)

# openstack-upgrade-playbooks

**Upgrade experiences and procedures for OpenStack platforms, per release and per deployment method.**

Part of [OzarLand](https://github.com/OzarLand/ozarland), a collaborative knowledge-sharing space for OpenStack
operators. Share experiences, document solutions, learn from each other. No imposed tools, no single way of
operating OpenStack.

> **Repository metadata to apply:** description "Upgrade experiences and procedures for OpenStack, per release and
> deployment method: preparation, pre-checks, health checks, common problems, rollback limits, real reports."
> Topics: `openstack`, `upgrade`, `kolla-ansible`, `openstack-operations`, `sre`, `release-management`.

> 🛑 **Upgrades are destructive operations on a whole platform.** Everything here describes what one team did on
> one platform. Nothing here is an officially supported upgrade path unless it links to the upstream documentation
> that says so. Always check the release notes and your deployment tool's upgrade guide for your own path.

## Scope

**In scope:**

- Preparing an upgrade: planning, communication, maintenance windows, decision points.
- Prerequisites and pre-checks: versions, OS, backups, cluster health (Galera, RabbitMQ, Ceph), deprecated options,
  pending migrations.
- Upgrade paths: which were done, and whether upstream documents them as supported (with the link).
- Differences between releases that affected an upgrade: renamed or removed options, changed defaults, new or
  dropped services, notable database migrations.
- Strategies by deployment method: Kolla-Ansible first (because its operators are here), others as they arrive.
- Health checks before, during and after.
- Problems met and how they were resolved.
- Rollback: what could be rolled back, what could not, recovery plans beyond that point.
- Real upgrade reports, told first-hand.

**Out of scope:** instance troubleshooting unrelated to an upgrade (see `openstack-vm-runbooks`), initial
deployment (see `kolla-ansible-deployment-patterns`).

## How content is organised

```text
playbooks/<deployment-method>/<from>-to-<to>/   step-by-step playbooks, e.g. playbooks/kolla-ansible/2024.2-to-2025.1/
pre-checks/                                     reusable prerequisite and health check lists
release-differences/<release>/                   what changed in a release that affects upgrading to it
problems/                                       problems met during upgrades, as runbooks
rollback/                                       rollback strategies and their limits
reports/                                        first-hand upgrade experience reports
templates/                                      upgrade-playbook and experience-report templates
```

Playbooks follow the shared [upgrade playbook template](https://github.com/OzarLand/ozarland/blob/main/community/templates/upgrade-playbook.md).
Every page states its release pair, deployment method and environment; `status` says whether anyone else has
confirmed it.

## Index

| Page | From → To | Deployment method | Status |
|---|---|---|---|
| | | | |

## First pages to write

1. One real upgrade report, whatever the release pair.
2. The pre-check list that report's team used, generalised.
3. Release differences for the most recent release the community has upgraded to.
4. Rollback: what a Kolla-Ansible upgrade can and cannot roll back, from experience.

## Contributing

- **Tell what happened during an upgrade:** start an *Experience reports* discussion, or submit a report page.
- **Share a playbook:** copy `templates/upgrade-playbook.md`, open a pull request. State the release pair and the
  deployment method in the title.
- **Confirm a playbook on your platform:** open a *Documentation proposal* issue with your result.
- **Report an upgrade problem you solved:** open an issue with the *Problem solved* template.

Rules that are not optional: no secrets, hostnames, addresses or unredacted logs; flag destructive steps; never
present a path as supported without an upstream reference. Full guide: [CONTRIBUTING.md](CONTRIBUTING.md).

## License

All content, documentation and code alike, is licensed under the Apache License 2.0 ([LICENSE](LICENSE)). Reuse it
freely with attribution. See [licensing](https://github.com/OzarLand/ozarland/blob/main/docs/conventions/licensing.md).

OpenStack is a project of the OpenInfra Foundation community. OzarLand is an independent community initiative.
