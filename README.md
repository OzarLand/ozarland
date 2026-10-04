# OzarLand

**An open-source ecosystem for running OpenStack in production with Kolla Ansible.**

OzarLand is being built as an **open-source ecosystem**: a small set of coherent, openly licensed projects
that help teams deploy, operate and evolve production OpenStack platforms with
[Kolla Ansible](https://docs.openstack.org/kolla-ansible/latest/) over the long term.

> **Kolla Ansible stays the deployment engine. OzarLand builds what is missing around it — it never replaces it.**

```text
                    OzarLand
             (open-source ecosystem)
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

## Why an ecosystem

Deploying OpenStack is the beginning of the operational journey, not the end. Teams that run Kolla Ansible in
production for years keep rebuilding the same things around it — reproducibility, change traceability, safe
upgrades, local patches, multiple environments, Day-2 procedures, documentation that survives people —
usually by hand and differently each time.

OzarLand's goal is to build that missing layer **once, in the open, with the people who operate these platforms**:
as shared conventions, focused tools and documentation, rather than as one more platform to depend on.

## Open source from day one

- **Apache License 2.0** for every project — the same licence as OpenStack, Kolla and Kolla Ansible, so work can
  move upstream without friction.
- **Developer Certificate of Origin** (sign-off) rather than a CLA.
- **Upstream first:** when a gap is generic to every Kolla Ansible user, it is contributed to Kolla Ansible,
  not kept in OzarLand.
- **No new lock-in:** everything OzarLand ships must work with upstream Kolla Ansible and standard tooling;
  removing OzarLand must leave a working Kolla Ansible setup.
- **On-premise and self-contained:** no SaaS dependency, no mandatory central service.
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

| Repository | Purpose | Status |
|---|---|---|
| [`ozarland`](https://github.com/OzarLand/ozarland) | This repository: vision, governance, cross-project decisions | Active |
| [`ozar-deploy`](https://github.com/OzarLand/ozar-deploy) | Deployment lifecycle around Kolla Ansible | Scoping |
| [`ozar-ops`](https://github.com/OzarLand/ozar-ops) | Day-2 operations — "know before you act" | Scoping |

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
