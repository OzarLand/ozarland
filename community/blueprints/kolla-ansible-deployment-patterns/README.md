# kolla-ansible-deployment-patterns

**How operators actually deploy OpenStack with Kolla-Ansible, compared side by side.**

Part of [OzarLand](https://github.com/OzarLand/ozarland), a collaborative knowledge-sharing space for OpenStack
operators. Share experiences, document solutions, learn from each other. No imposed tools, no single way of
operating OpenStack.

> **Repository metadata to apply:** description "Deployment patterns for OpenStack with Kolla-Ansible, from real
> platforms: topologies, network and storage choices, inventories, configuration layout, common errors, version
> notes. Compared, not prescribed." Topics: `openstack`, `kolla-ansible`, `kolla`, `deployment`,
> `reference-architecture`, `openstack-operations`, `ansible`.

## Scope

This repository documents the many ways operators deploy OpenStack with [Kolla-Ansible](https://docs.openstack.org/kolla-ansible/latest/),
so that someone planning or changing a deployment can compare approaches and learn from others' experience.

**It does not promote one architecture as correct.** Every pattern states its context, its benefits, its limits
and the lessons its operators learned. Two patterns can contradict each other and both be right in their context.

**In scope:**

- Reference topologies and node roles, from all-in-one labs to multi-controller, multi-network-node production.
- Lab, pre-production and production environments: how they differ and how they are kept comparable.
- Network design: interfaces, management/API/tunnel/external/storage networks, OVN versus OVS, provider networks,
  MTU, bonding.
- Storage choices: Ceph, LVM, NFS and others for Glance, Cinder and Nova; what is shared and what is local.
- Inventories, `globals.yml`, group and host variables, configuration overrides: how they are organised and
  versioned across environments.
- Secrets and configuration files: how `passwords.yml` and certificates are handled (never their content).
- Architectural choices and their operational consequences.
- Errors met during deployment and reconfiguration, with their causes and fixes.
- Differences between Kolla-Ansible and OpenStack releases that affect a pattern, and the precautions they require.

**Out of scope:** running instances (see `openstack-vm-runbooks`), upgrading (see `openstack-upgrade-playbooks`),
other deployment tools (welcome as separate pattern repositories when their operators show up), and anything
that reproduces the upstream documentation instead of adding operational experience to it.

## How content is organised

```text
topologies/        one pattern per topology, from all-in-one to large multinode
networking/        network designs and their trade-offs
storage/           storage designs and their trade-offs
configuration/     inventory layouts, variable organisation, environment separation, secrets handling
deployment-errors/ errors met during deploy/reconfigure/upgrade-prepare, cause and fix
version-notes/     per Kolla-Ansible / OpenStack release: what changed that affects deployments
comparisons/       side-by-side comparisons of patterns on one dimension (e.g. OVN vs OVS, Ceph vs LVM)
templates/         deployment-pattern template
```

Each pattern follows the shared [deployment pattern template](https://github.com/OzarLand/ozarland/blob/main/community/templates/deployment-pattern.md):
context, topology, network, storage, inventory and configuration layout, key choices and consequences, what went
wrong, version notes, lessons learned, validity and limits.

## Index

| Pattern | Purpose | Scale | Network | Storage | Releases |
|---|---|---|---|---|---|
| | | | | | |

## First pages to write

1. All-in-one lab for learning and testing changes before production.
2. Three controllers, OVN, Ceph RBD: a common production baseline, with its consequences.
3. Separated storage and storage-replication networks: why, and what it costs.
4. Keeping lab, pre-production and production inventories aligned: one layout that worked.
5. Comparison: OVN versus OVS as seen from operations (not from features).
6. Deployment errors: the five most common `kolla-ansible deploy` failures and what they meant.

## Contributing

- **Compare approaches:** start a *Show and compare* discussion.
- **Share your pattern:** copy `templates/deployment-pattern.md`, open a pull request. Describe your context first.
- **Add a variant or a consequence to an existing pattern:** open a pull request or a *Documentation proposal* issue.
- **Report a deployment error you solved:** open an issue with the *Problem solved* template.

Rules that are not optional: no secrets (never `passwords.yml` content), no real hostnames, addresses or
unredacted logs; say where your pattern runs and for how long. Full guide: [CONTRIBUTING.md](CONTRIBUTING.md).

## License

All content, documentation and code alike, is licensed under the Apache License 2.0 ([LICENSE](LICENSE)). Reuse it
freely with attribution. See [licensing](https://github.com/OzarLand/ozarland/blob/main/docs/conventions/licensing.md).

OpenStack, Kolla and Kolla-Ansible are projects of the OpenInfra Foundation community. OzarLand is an independent
community initiative and is not affiliated with or endorsed by the OpenInfra Foundation.
