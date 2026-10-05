# OzarLand

**The open-source operator toolkit for running OpenStack in production with Kolla Ansible.**

OzarLand is an **open-source ecosystem** for the people who operate OpenStack platforms deployed with
[Kolla Ansible](https://docs.openstack.org/kolla-ansible/latest/). Kolla Ansible is used as it is; OzarLand adds
what an operator needs around it to deploy, operate, upgrade and maintain a production platform over the years.

> **Kolla Ansible stays the deployment engine. OzarLand is built for the operator who runs it in production.**

```text
                    OzarLand
          (open-source operator toolkit)
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   Deployment       Lifecycle      Day 2
   ecosystem        management      operations
        │              │              │
        └──────────────┼──────────────┘
                       │
                 Kolla Ansible
                       │
                   OpenStack
```

## Why

Deploying OpenStack is the beginning of the operational journey, not the end. Once a platform is in production,
the operator's daily work is to keep environments under control, prepare and trace changes, upgrade safely, carry
local patches, maintain hosts, and know before acting what an operation will affect. Teams usually build their own
scripts and habits for this, differently each time.

OzarLand's goal is to provide these operator functions **once, in the open, with the people who run these platforms**.

## Open source from day one

- **Apache License 2.0** for every project — the same licence as OpenStack, Kolla and Kolla Ansible.
- **Developer Certificate of Origin** (sign-off) rather than a CLA.
- **Kolla Ansible as it is:** OzarLand never forks it or redoes what it already does.
- **No new lock-in:** removing OzarLand must leave a working Kolla Ansible setup; no SaaS, no mandatory central service.
- **Decisions in the open:** architecture decisions are written as ADRs, so the reasoning is public along with the code.

## Status

**Private — foundation phase (October 2026).** The repositories are private while the projects are being scoped
and stabilised. They are written as if they were already public, and will be opened progressively:

```text
Private → Internal development → Early adopters → Open source → Community → Production ecosystem
```

No code exists yet. Technical design comes next and will be documented here.

## Projects

All OzarLand products are prefixed `ozar-`.

| Repository | For the operator who… | Status |
|---|---|---|
| [`ozarland`](https://github.com/OzarLand/ozarland) | wants to understand the ecosystem: vision, governance, cross-project decisions | Active |
| [`ozar-deploy`](https://github.com/OzarLand/ozar-deploy) | prepares, deploys and changes the platform with Kolla Ansible | Scoping |
| [`ozar-ops`](https://github.com/OzarLand/ozar-ops) | operates the running platform day to day — "know before you act" | Scoping |

## Learn more

- [Vision and principles](docs/vision.md)
- [Governance](docs/governance.md)
- [Architecture decision records](docs/adr/README.md)
- [GitHub conventions](docs/github-conventions.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md), the [code of conduct](CODE_OF_CONDUCT.md) and the
[security policy](SECURITY.md).

## License

Apache License 2.0 — see [LICENSE](LICENSE).
OpenStack, Kolla and Kolla Ansible are projects of the OpenInfra Foundation community. OzarLand is an
independent project and is not affiliated with or endorsed by the OpenInfra Foundation.
