# Repository architecture and priorities

How the community's content is split across repositories, why, and in what order repositories are created.

## What you will find

Content is organised in thematic repositories (see [current repositories](#current-repositories)). Across them,
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
not as a universal truth. See [knowledge lifecycle](knowledge-lifecycle.md) for how content matures from an
open question to a procedure validated by a human operator other than its author.

## Current repositories

OzarLand starts small and grows with the community. Repositories are created when there is content to put in them,
not before. The reasoning, including the trade-offs between separate repositories and grouped documentation, is in
the rest of this page.

| Repository | Role | Status |
|---|---|---|
| [`ozarland`](https://github.com/OzarLand/ozarland) | Community home: mission, principles, contribution model, shared templates, repository blueprints, open questions | **Active**: see the [Discussions](https://github.com/OzarLand/ozarland/discussions) and the [newcomer path](../newcomers/README.md) |
| [`kolla-ansible-deployment-patterns`](https://github.com/OzarLand/kolla-ansible-deployment-patterns) | How operators deploy OpenStack with Kolla-Ansible: topologies, network and storage choices, inventories, configuration layout, common deployment errors, version differences | **Active**: what it holds and each page's status are in its [index](https://github.com/OzarLand/kolla-ansible-deployment-patterns#index) |
| [`openstack-vm-runbooks`](https://github.com/OzarLand/openstack-vm-runbooks) | Diagnosing and resolving instance problems: stuck states, scheduling, boot, migration, networking, volume attachment, with Nova, Neutron, Glance and Cinder diagnostics | **Active**: what it holds and each page's status are in its [index](https://github.com/OzarLand/openstack-vm-runbooks#index) |
| [`openstack-quick-lab`](https://github.com/OzarLand/openstack-quick-lab) | Try OpenStack in about one hour: an all-in-one Kolla-Ansible lab on one VM, guided exercises that use the runbooks, one command to delete everything; see [ADR-0009](adr/0009-openstack-quick-lab-repository.md) | **Active**: variants and exercises are listed in its [README](https://github.com/OzarLand/openstack-quick-lab#readme) |
| [`openstack-operator-skills`](https://github.com/OzarLand/openstack-operator-skills) | Agent skills for Claude that apply an operating method and this knowledge to incidents, changes, maintenance, VM troubleshooting and Kolla-Ansible work; every procedure states its validation status, and the skills never act on a platform themselves | **Active**: validation coverage per skill is in its [README](https://github.com/OzarLand/openstack-operator-skills#-validation-status) |
| `openstack-upgrade-playbooks` | Upgrade preparation, prerequisites, health checks, common problems, rollback limits and real upgrade reports, per release and per deployment method | Planned, priority 2. Until it exists, Kolla-Ansible version notes and upgrade reports are in `kolla-ansible-deployment-patterns` (`version-notes/`) |
| `openstack-operations-runbooks` | Candidate umbrella for incident, networking, storage and performance runbooks once the first contributions show how they should be grouped | Under evaluation |

Open questions and [discussions](https://github.com/OzarLand/ozarland/discussions) live in this repository until a
dedicated space proves necessary. Initial READMEs
and structures for the planned repositories are kept under [`community/blueprints/`](../community/blueprints/) so they
can be created as soon as the first content is ready. Blueprints are removed once their repository exists. Deploying with another tool than Kolla-Ansible? Your patterns
are welcome too: start an [*Ideas* discussion](https://github.com/OzarLand/ozarland/discussions/new?category=ideas).

Earlier OzarLand repositories that developed operator tooling (`ozar-deploy`, `ozar-ops`, `ozar-kb`, `ozar-lab`)
are archived. They are not part of the community's scope and are kept read-only for reference. The reasoning
behind the repositioning is recorded in [ADR-0008](adr/0008-community-knowledge-sharing-space.md).

## Guiding rule

**A repository is created when there is content to put in it, not before.** An empty repository with a good name
attracts nobody and signals a community that does not exist yet. Content starts in the most general place that
fits, and is moved to a dedicated repository when it is large enough to deserve its own entry point, its own
issue flow and its own maintainers.

The costs of a new repository are real: another README to keep accurate, another set of templates and labels to
keep in sync, another place for a newcomer to look, and another split in the search results. The benefits are also
real: a clear scope that people can bookmark, a focused issue list, and maintainers who know the subject.

## Needs of OpenStack operators

The content operators ask for, roughly in the order they ask for it:

1. **"My instance / volume / network is broken, what do I check?"** Symptom-driven runbooks, immediately useful,
   high reuse across environments. The most common entry point for a newcomer.
2. **"How do others deploy this?"** Deployment patterns and their consequences. Needed when building, re-building
   or growing a platform. Strongly tied to the deployment tool, which is why it is split by tool.
3. **"We have to upgrade, what should we expect?"** Upgrade preparation, pitfalls, rollback limits. Needed
   periodically, high stakes, strongly tied to release pairs and deployment method.
4. **"How do we run this day to day?"** Health checks, maintenance windows, capacity, backups, patching.
5. **"Why is it slow?" / "Why did the network break?" / "What is wrong with Ceph?"** Domain troubleshooting.
6. **"Is anyone else seeing this?"** Open questions and discussions.

## Proposed structure

### Phase 1: launch

| Repository | Scope | Why it comes first |
|---|---|---|
| `ozarland` | Community home. Mission, principles, contribution model, shared templates, conventions, repository blueprints, launch plan. **Hosts the community's Discussions** (questions, experience reports, show and compare, ideas) during the launch phase. | Exists already. One visible meeting place is worth more than several empty ones. |
| `openstack-vm-runbooks` | Diagnosing and resolving instance problems: stuck states, scheduling and boot failures, create, delete and migration errors, instance networking, volume attachment, plus the Nova, Neutron, Glance and Cinder diagnostics these require, recovery after incidents and post-fix checks. | The most frequent operator pain, the easiest content to contribute from existing notes, and the clearest format (symptom → checks → cause → fix → verification). Produces the community's first validated pages. |
| `kolla-ansible-deployment-patterns` | How operators deploy OpenStack with Kolla-Ansible: reference topologies, lab versus pre-production versus production, network and storage choices, inventories, variables and configuration layout, secrets handling, architectural choices and their consequences, common deployment errors, version differences. | Kolla-Ansible is one of the most widely used deployment methods and its users have no shared place to compare approaches. Pattern pages present context, benefits, limits and lessons, never a single correct architecture. |

### Phase 2: once the first contributions exist

| Repository | Scope | Trigger to create it |
|---|---|---|
| `openstack-upgrade-playbooks` | Upgrade preparation, prerequisite checks, supported paths (verified against upstream release notes before being stated), version differences, strategies per deployment method, Kolla-Ansible upgrades, health checks before, during and after, common problems, rollback strategies and their limits, real upgrade reports. | Two or more upgrade experience reports in Discussions, or an operator willing to write the first playbook from a real upgrade. Until then, upgrade reports are collected in Discussions and in the blueprint. |

### Phase 3: consolidate, then split only if needed

The remaining suggestions overlap heavily with each other and with the phase 1 repositories:

| Suggested name | Assessment |
|---|---|
| `openstack-incident-runbooks` | Generic incident procedures (control plane down, database or message queue trouble, API errors) are runbooks with the same format as VM runbooks. Many VM incidents are control-plane incidents in disguise. Splitting them from the start fragments the runbook corpus. |
| `openstack-networking-troubleshooting` | Instance connectivity is already in `openstack-vm-runbooks`. Agent, routing and MTU problems are the other half of the same investigations. A separate repository forces contributors to decide where a "VM cannot reach the gateway" page belongs. |
| `openstack-storage-operations` | Cinder attachment problems are in `openstack-vm-runbooks`. Ceph and backend operations are a distinct domain with its own experts, and the strongest candidate for a separate repository later. |
| `openstack-performance-troubleshooting` | Cross-cutting by nature (compute, network, storage, database). Pages here are mostly diagnostics that refer to the other domains. |
| `openstack-operations-handbook` | Day-to-day practices, health checks, maintenance. Valuable, but a handbook is a collection of practices that are hard to write without first having runbooks to point to. |
| `openstack-operator-questions` | Covered by GitHub Discussions on `ozarland`. A repository whose content is only issues has no pages to maintain and splits the conversation away from the content. |

**Recommendation:** when runbooks beyond the VM scope start arriving, create **one** repository,
`openstack-operations-runbooks`, organised by domain directories (`control-plane/`, `networking/`, `storage/`,
`performance/`, `maintenance/`), using the same runbook template, labels and issue flow as `openstack-vm-runbooks`.
A domain gets its own repository when it has enough content and enough dedicated contributors to justify it;
storage (Ceph) is the likeliest first split. The handbook content (health checks, maintenance practices) starts
as a `maintenance/` and `health-checks/` section in the same repository.

An alternative was considered before phase 1: name the first runbook repository `openstack-runbooks` with
`compute/` as its first domain, so that it could absorb the other domains without a later rename. Phase 1 kept the
more specific `openstack-vm-runbooks`, which is what people search for; runbooks outside the instance scope go to
`openstack-operations-runbooks` as described above.

## Trade-offs: separate repositories versus grouped documentation

| Criterion | Favors separate repositories | Favors grouping |
|---|---|---|
| Contributor profile | Different people (Kolla-Ansible deployers versus Ceph operators) | Same people (anyone who troubleshoots instances also troubleshoots their network) |
| Content format | Different templates (pattern pages versus runbooks) | Same template |
| Issue flow | Different kinds of items (deployment errors versus incidents) | Same kinds |
| Lifecycle | Different cadence (upgrade content follows release pairs) | Same cadence |
| Discoverability | A name people search for (`kolla-ansible`) | Cross-cutting problems that would otherwise land in two places |
| Maintenance load | Enough maintainers to own it | A small team keeping consistency across everything |

Applied to the suggestions: deployment patterns and upgrade playbooks pass the "separate" test (different format,
different contributors, different cadence). Runbooks of all domains fail it (same format, same people, same flow),
which is why they are grouped first and split later.

## Naming

- Lowercase, hyphenated, descriptive of the content rather than of a tool, except where the content is specific to
  a tool (`kolla-ansible-deployment-patterns`).
- `-runbooks` for symptom-driven procedures, `-patterns` for design and deployment comparisons, `-playbooks` for
  multi-step operations such as upgrades.
- No `ozar-` prefix: the community publishes operator knowledge, not OzarLand products.

## Creating a repository

1. Propose it in a Discussion (*Ideas*) with the content that is ready to go into it.
2. Record the decision in a short [decision record](adr/README.md).
3. Create it from the blueprint under [`community/blueprints/`](../community/blueprints/) and the shared files under
   [`community/repo-template/`](../community/repo-template/).
4. Enable Discussions, apply the shared labels, and add it to [current repositories](#current-repositories) and to the
   short list in the main README.
5. Remove its blueprint from `community/blueprints/`: the repository is now the reference.
