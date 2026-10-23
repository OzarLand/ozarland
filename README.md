# OzarLand

**A collaborative knowledge-sharing space for OpenStack operators.**

> Share experiences, document solutions, learn from each other.
> No imposed tools, no single way of operating OpenStack.

OzarLand is where people who run OpenStack platforms meet to compare how they deploy, operate, upgrade and
troubleshoot them, and to turn what they learn in production into knowledge that others can reuse and improve.

## Where to start?

- 🌱 **I'm new to OpenStack.** Follow the [newcomer path](newcomers/README.md): five short pages, read in order, from
  what the services are to your first contribution. Keep the [glossary](newcomers/glossary.md) open as you go.
- 🔧 **I have a problem with a VM.** Go to [openstack-vm-runbooks](https://github.com/OzarLand/openstack-vm-runbooks#index) and find your symptom: stuck states,
  scheduling, migration, networking, recovery. Every runbook starts with read-only checks. Nothing matches?
  [Ask in the Q&A discussions](newcomers/start-a-discussion.md), with your release and deployment method.
- 🏗️ **I'm deploying a platform.** Go to [kolla-ansible-deployment-patterns](https://github.com/OzarLand/kolla-ansible-deployment-patterns#index): topologies, network and
  storage choices, errors met during real deployments, each with its context and limits. Using another deployment
  tool? Your patterns are welcome too: start an [*Ideas* discussion](https://github.com/OzarLand/ozarland/discussions/new?category=ideas).
- 🤝 **I want to contribute.** Read [your first contribution](newcomers/first-contribution.md), then pick a task
  labelled [`good first contribution`](https://github.com/search?q=org%3AOzarLand+label%3A%22good+first+contribution%22+state%3Aopen&type=issues).
  The full rules are in [CONTRIBUTING.md](CONTRIBUTING.md).

Whichever door you take, questions are welcome: [start a discussion](newcomers/start-a-discussion.md) explains which
category to pick, what to include and what never to post.

## What can you find here?

Content is organised in thematic repositories (see the [repository directory](#repository-directory)). Across them,
you will find:

| Kind of content | What it is |
|---|---|
| **Runbooks** | Symptom-driven procedures: what you see, what to check, what it usually means, what to do, how to confirm it is fixed. |
| **Deployment patterns** | How operators actually deploy OpenStack: topologies, network and storage choices, inventory layouts, and the consequences of those choices. |
| **Upgrade experiences** | Preparation, prerequisite checks, what went wrong, what worked, and how to roll back, per release and per deployment method. |
| **Diagnostics** | Command sequences and log-reading guides for Nova, Neutron, Cinder, Glance, Keystone and the infrastructure services around them. |
| **Experience reports** | First-hand accounts of an incident, a migration, a capacity problem or an architectural decision, with the context that makes them useful. |
| **Open questions** | Problems the community has not solved yet, where several operators compare their observations. |

Every piece of content states the OpenStack release, the components involved, the deployment method and the
conditions under which it was observed. A solution that worked in one environment is documented as exactly that,
not as a universal truth. See [knowledge lifecycle](docs/knowledge-lifecycle.md) for how content matures from an
open question to a procedure validated by several operators.

## Repository directory

OzarLand starts small and grows with the community. Repositories are created when there is content to put in them,
not before. The full reasoning, including the trade-offs between separate repositories and grouped documentation,
is in [docs/repositories.md](docs/repositories.md).

| Repository | Role | Status |
|---|---|---|
| [`ozarland`](https://github.com/OzarLand/ozarland) | Community home: mission, principles, contribution model, shared templates, repository blueprints, open questions | **Active** |
| [`kolla-ansible-deployment-patterns`](https://github.com/OzarLand/kolla-ansible-deployment-patterns) | How operators deploy OpenStack with Kolla-Ansible: topologies, network and storage choices, inventories, configuration layout, common deployment errors, version differences | **Active**, awaiting first patterns |
| [`openstack-vm-runbooks`](https://github.com/OzarLand/openstack-vm-runbooks) | Diagnosing and resolving instance problems: stuck states, scheduling, boot, migration, networking, volume attachment, with Nova, Neutron, Glance and Cinder diagnostics | **Active**, seed runbooks under review |
| `openstack-upgrade-playbooks` | Upgrade preparation, prerequisites, health checks, common problems, rollback limits and real upgrade reports, per release and per deployment method | Planned, priority 2 |
| `openstack-operations-runbooks` | Candidate umbrella for incident, networking, storage and performance runbooks once the first contributions show how they should be grouped | Under evaluation |

Open questions and discussions live in this repository until a dedicated space proves necessary. Initial READMEs
and structures for the planned repositories are kept under [`community/blueprints/`](community/blueprints/) so they
can be created as soon as the first content is ready.

Earlier OzarLand repositories that developed operator tooling (`ozar-deploy`, `ozar-ops`, `ozar-kb`, `ozar-lab`)
are archived. They are not part of the community's scope and are kept read-only for reference. The reasoning
behind the repositioning is recorded in [ADR-0008](docs/adr/0008-community-knowledge-sharing-space.md).

## How to contribute?

Any real experience is worth sharing. You can:

- **Ask a question.** Open a discussion or an issue using the *Question* template. Give the release, the deployment
  method and what you have already checked.
- **Share a problem you solved.** Use the *Problem solved* template. Once the fix is confirmed by someone else, it
  becomes a runbook.
- **Add or improve a procedure.** Open a pull request with the runbook or pattern template. Small improvements to
  existing content are as welcome as new pages.
- **Share an experience report.** Upgrades, incidents, architecture choices: tell what happened, what you learned,
  and what you would do differently.
- **Review other people's contributions.** Confirming that a procedure also works in your environment, or does not,
  is one of the most valuable contributions there is.

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the practical rules. They are short on purpose. The non-negotiable
ones: never publish secrets, real hostnames, IP addresses, unredacted logs or anything that identifies an
infrastructure, and clearly flag commands that can affect production.

## What is OzarLand? Mission and vision

Running OpenStack is a craft learned mostly on the job. Every operations team builds its own runbooks, its own
checklists and its own hard-won understanding of why a platform behaves the way it does. Most of that knowledge
never leaves the team.

OzarLand exists to change that. It is a community, not a product. Its purpose is to:

- share deployment and operations practices for OpenStack;
- document problems met in production and the solutions that were applied;
- pool runbooks and operational procedures;
- compare different technical approaches without declaring a single winner;
- share experience reports on upgrades, incidents, performance, availability and maintenance;
- help experienced operators and newcomers learn from each other;
- turn individual knowledge into collective knowledge that anyone can reuse and improve.

OzarLand does not tell operators how they must run OpenStack. It gives them a place to learn from one another and
to build a common body of operational knowledge, one real experience at a time.

## Who is it for?

- **OpenStack operators** who run platforms day to day, whatever their distribution or deployment method.
- **Cloud and platform engineers** who design, build and change OpenStack environments.
- **SREs and on-call engineers** who diagnose and resolve incidents on OpenStack services.
- **Anyone responsible for an OpenStack platform** who wants to compare notes with peers, from a one-node lab
  to a multi-region production cloud.

You do not need to use a particular deployment tool, distribution, storage backend or network plugin to take part.
Kolla-Ansible, OpenStack-Ansible, Charmed OpenStack, TripleO heritage platforms, vendor distributions, hand-built
clouds: every real-world setup is a valid source of experience.

## Community principles

1. **Collaboration over authority.** Knowledge is built by comparing experiences, not by handing down rules.
2. **Openness.** Discussions, decisions and content are public and reviewable. Anyone can contribute.
3. **Tool neutrality.** No deployment tool, distribution or vendor is promoted as the right one. Each approach
   is documented with its context, its benefits, its limits and its lessons.
4. **Respect for different approaches.** Two operators can make opposite choices for good reasons. The goal is to
   understand why, not to decide who is right.
5. **Real experience first.** Content comes from things that actually happened on real platforms. Theory is
   welcome when it explains an observation.
6. **Honesty about validity.** Every procedure states where and when it was verified, and what is still uncertain.
7. **Safety.** Risky and destructive commands are flagged. Sensitive data never reaches a public repository.
8. **Lightweight governance.** Just enough structure to keep content findable and trustworthy, and nothing more.

The [code of conduct](CODE_OF_CONDUCT.md) applies everywhere in the organisation.

## Learn more

- [Newcomer path](newcomers/README.md) and [glossary](newcomers/glossary.md)
- [Mission and principles](docs/vision.md)
- [Knowledge lifecycle: from question to validated procedure](docs/knowledge-lifecycle.md)
- [Repository architecture and priorities](docs/repositories.md)
- [Content conventions](docs/conventions/README.md): metadata, runbook structure, risk warnings, sensitive data
- [Shared templates for every community repository](community/README.md)
- [Agents](docs/agents.md) and the [review and merge policy](docs/review-policy.md)
- [Governance](docs/governance.md)
- [Decision records](docs/adr/README.md)
- [GitHub conventions](docs/github-conventions.md)
- [Launch plan](docs/launch-plan.md)

## Go further

- [openstack-vm-runbooks](https://github.com/OzarLand/openstack-vm-runbooks): diagnosing and resolving instance problems.
- [kolla-ansible-deployment-patterns](https://github.com/OzarLand/kolla-ansible-deployment-patterns): how operators deploy OpenStack with Kolla-Ansible.
- [Newcomer path](newcomers/README.md) and [glossary](newcomers/glossary.md).

## License

All content, documentation and code alike, is licensed under the Apache License 2.0, see [LICENSE](LICENSE).
Reuse it freely with attribution. See [docs/conventions/licensing.md](docs/conventions/licensing.md).

OpenStack and Kolla are projects of the OpenInfra Foundation community. OzarLand is an independent community
initiative and is not affiliated with or endorsed by the OpenInfra Foundation or any vendor.
