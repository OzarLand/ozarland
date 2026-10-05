# Vision and principles

## Mission

> Give the operators of OpenStack platforms deployed with Kolla Ansible an open-source toolkit to deploy, operate,
> upgrade and maintain them safely over many years — using Kolla Ansible as it is, without depending on a new platform.

## The operator first

OzarLand starts from the operator's work, not from a list of features. Every project answers one question:

> **What does an operator need to run Kolla Ansible in production?**

Typical operator tasks:

- keep several environments (lab, pre-production, production) under control and comparable;
- prepare a change, see its effect before applying it, and keep a trace of it;
- upgrade to a new OpenStack series with prerequisites checked and backups in place;
- carry local patches and rebuild images without losing track of them;
- maintain hosts (patching, reboots, evacuations) knowing what will be affected;
- check the platform before acting, and collect evidence during an incident;
- make knowledge survive the people who hold it.

## Why Kolla Ansible

Kolla Ansible is an official OpenStack project. It deploys OpenStack services in containers, covers the deployment
lifecycle and, together with Kolla, offers mature configuration and image customisation. It is plain Ansible and
containers: operators can read it, debug it and reason about it.

OzarLand uses it **as it is**. This commits the ecosystem to:

1. never forking Kolla Ansible, and never redoing what it already does;
2. keeping the upstream vocabulary, so that a Kolla Ansible operator understands OzarLand immediately;
3. keeping Kolla Ansible's behaviour and output visible to the operator;
4. following the OpenStack release rhythm.

## What the ecosystem covers

Deployment · configuration · lifecycle management · upgrades · local patches · image rebuilds ·
environment management · Day-2 administration · configuration validation · operation preparation ·
documentation · observability · operational governance · reproducibility · change management.

Each of these will be scoped project by project. Some needs are best served by documentation and conventions
rather than by new code.

## What OzarLand is not

- a fork or a replacement of Kolla Ansible;
- a new OpenStack distribution;
- a bare-metal provisioning tool;
- a monitoring stack;
- a Horizon alternative;
- a SaaS or a control plane that users must run.

## Principles

1. **Operator first.** A function exists because an operator needs it in production.
2. **Kolla Ansible as it is.** Use it; never fork it or duplicate it.
3. **Simple → coherent → maintainable → evolvable.** Few projects, each with a clear responsibility.
4. **Eject path.** Removing OzarLand leaves a plain, working Kolla Ansible setup.
5. **Observe before acting; evidence before assumption.** "Unknown" is never "OK".
6. **Automation with control.** Risky actions are explicit, reviewed and recorded; humans stay in the loop.
7. **Stability before feature velocity.**
8. **Knowledge must survive people.** Decisions are ADRs; procedures are runbooks.
9. **No new lock-in.** Prefer OpenStack, Kolla Ansible, Docker, Ansible, Git and standard Linux tooling over any new dependency.

## Who it is for

- Platform and operations engineers who run Kolla Ansible-based OpenStack in production.
- Technical leads who need changes to be reviewable, reproducible and auditable.
- Contributors who share these operator needs.

## An ecosystem, built with its users

OzarLand is meant to become a community project. Until it is public, it is developed by its founding maintainer
with the same discipline an open community requires: public-ready content, documented decisions, issues and pull
requests, and no dependency on any single company's environment.
