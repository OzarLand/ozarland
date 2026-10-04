# Vision and principles

## Mission

> Build, in the open, the missing production layer around Kolla Ansible — conventions, focused tools and
> documentation — so that teams can deploy, operate and evolve OpenStack platforms safely over many years,
> without replacing Kolla Ansible and without depending on a new platform.

## Why Kolla Ansible

Kolla Ansible is an official OpenStack project. It deploys OpenStack services in containers, covers the
deployment lifecycle (bootstrap, deploy, reconfigure, upgrade, backup and recovery helpers) and, together with
Kolla, offers mature configuration and image customisation mechanisms. It is plain Ansible and containers:
operators can read it, debug it and reason about it.

OzarLand therefore builds **around** Kolla Ansible. This commits the ecosystem to:

1. never re-implementing what Kolla Ansible already does well;
2. keeping the upstream vocabulary, so that a Kolla Ansible operator understands OzarLand immediately;
3. contributing generic improvements upstream first;
4. following the OpenStack release rhythm.

## What the ecosystem covers

Deployment · configuration · lifecycle management · upgrades · local patches · image rebuilds ·
environment management · Day-2 administration · configuration validation · operation preparation ·
documentation · observability · operational governance · reproducibility · change management.

Each of these will be scoped project by project. Many needs are best served by documentation and conventions
rather than by new code.

## What OzarLand is not

- a fork or a replacement of Kolla Ansible;
- a new OpenStack distribution;
- a bare-metal provisioning tool;
- a monitoring stack;
- a Horizon alternative;
- a SaaS or a control plane that users must run.

## Principles

1. **Kolla Ansible first.** Before any feature: *"must this live in OzarLand, or in Kolla Ansible?"*
2. **Simple → coherent → maintainable → evolvable.** Few projects, each with a clear responsibility.
3. **Eject path.** Removing OzarLand leaves a plain, working Kolla Ansible setup.
4. **Observe before acting; evidence before assumption.** "Unknown" is never "OK".
5. **Automation with control.** Risky actions are explicit, reviewed and recorded; humans stay in the loop.
6. **Stability before feature velocity.**
7. **Knowledge must survive people.** Decisions are ADRs; procedures are runbooks.
8. **No new lock-in.** Prefer OpenStack, Kolla Ansible, Docker, Ansible, Git and standard Linux tooling over any
   new dependency.

## Who it is for

- Platform and operations engineers who run Kolla Ansible-based OpenStack in production.
- Technical leads who need changes to be reviewable, reproducible and auditable.
- Contributors who want to improve the production story of Kolla Ansible — inside OzarLand or upstream.

## An ecosystem, built with its users

OzarLand is meant to become a community project. Until it is public, it is developed by its founding maintainer
with the same discipline an open community requires: public-ready content, documented decisions, issues and pull
requests, and no dependency on any single company's environment.
