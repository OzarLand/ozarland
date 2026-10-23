# ADR-0009: A quick-lab repository to try OpenStack in about one hour

- **Status:** Proposed
- **Date:** 2026-10-23
- **Deciders:** @soufian-zaouam
- **Discussion:** to be opened in *Ideas* once this record is merged; until then, this pull request

## Context

OzarLand's entry points assume reading first: the [newcomer path](../../newcomers/README.md), then runbooks and
deployment patterns. Many people learn the other way round. They want a running OpenStack they can break and repair
before they read about it. Today they have to put together a lab themselves from the
[all-in-one lab pattern](https://github.com/OzarLand/kolla-ansible-deployment-patterns/blob/main/topologies/all-in-one-lab-on-a-single-vm.md),
which is written for operators, not for a first afternoon.

Two things stop newcomers from trying:

1. **Time and effort.** Building a lab from scratch takes a day or more for someone who has never done it.
2. **Fear of a surprise bill.** A lab on a cloud costs money every hour it runs. Someone who forgets to delete their
   VMs on a pay-as-you-go account can receive a bill far larger than they expected.

[repositories.md](../repositories.md) requires a decision record before a repository is created. This record proposes
one.

## Decision

Create a community repository, working name **`openstack-quick-lab`**: *Try OpenStack in about one hour, with no risk
of a surprise bill.* It is for people who want to experiment before they read.

### What it contains

- **An all-in-one OpenStack on one VM**, deployed with Kolla-Ansible, ready in about an hour, with scripts and a
  step-by-step guide.
- **Guided exercises that link to the existing runbooks.** For example: stop the DHCP agent, watch a new instance
  get no address, then diagnose and fix it with the
  [DHCP runbook](https://github.com/OzarLand/openstack-vm-runbooks/blob/main/networking/new-instance-gets-no-ip-dhcp-agents-down.md).
  The exercises send readers to the runbooks; they do not copy them.
- **A multinode variant later**, once the all-in-one lab is used and stable.

### Where the lab runs, and neutrality

- The repository explains how to build the lab **on any OpenStack cloud, or on a personal machine**. Every variant
  is documented on equal terms, with its requirements and its limits.
- **Felcloud is the first variant, and the one recommended to start with.** Felcloud is a prepaid cloud service
  built on OpenStack. Because spending cannot exceed the credit loaded, it is the recommended way to start without
  risk of a surprise bill. That reason is the only basis of the recommendation, and a reader can check it. The variant must link to the provider's own terms that state it. If the reason stops being true,
  the recommendation is withdrawn.
- **Variants for other providers, and a personal-machine variant, are welcome on equal terms**: same structure,
  same safety section, same review.
- **OzarLand stays independent.** No product or provider is required to follow the guide or the exercises.

### Safety built in

- **Every variant states its cost risk.** Prepaid: spending is limited to the credit. Pay-as-you-go: set a budget
  alert before you start, with how to do it on that provider. Personal machine: no cloud cost.
- **An estimated cost per hour is shown before launch.** The launch script prints it and asks for confirmation.
- **One command deletes everything** the lab created.
- **A reminder to delete the VMs** appears at the end of the guide and of every exercise.

### Who does what

| Who | Does |
|---|---|
| Lab session (agent with access to Felcloud labs) | Writes the scripts and tests them on its Felcloud labs; records the releases and timings it observed |
| Author | Writes the guide and the exercises, linking to the runbooks |
| Reviewers | Review as usual, under the [review and merge policy](../review-policy.md) |
| Owner | Creates the repository and sets its description, topics and Discussions |

### What stays out

- **No credentials in the repository**: no cloud credentials, no `clouds.yaml` with secrets, no `passwords.yml`.
  The [sensitive data](../conventions/sensitive-data.md) rules apply as everywhere.
- **No vendor marketing**: no prices beyond the cost estimate needed for safety, no promotional text, no logos.
- **No requirement to use Felcloud.** Every exercise works on any variant.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| **Separate `openstack-quick-lab` repository (chosen)** | One clear entry point for "try it now"; its scripts, tests and issues stay apart from the pattern pages; it can be linked from the README's newcomer door | One more repository to keep consistent; scripts need maintenance across releases |
| A `quick-lab/` section in `kolla-ansible-deployment-patterns` | No new repository | Hidden inside an operators' repository; mixes runnable scripts with pattern pages; newcomers would not find it |
| Only link to upstream guides (Kolla-Ansible quickstart, DevStack) | Nothing to maintain | No exercises tied to the runbooks; no cost safety; the barrier stays where it is |
| No recommended provider, all variants equal from the start | Strictly neutral | Someone has to test a first variant end to end; with nothing recommended, a newcomer still has to judge cost risk alone |

## Consequences

- **Tension with tool neutrality, and how it is handled.** The [principles](../vision.md) say no vendor is promoted.
  Recommending a provider as the starting point is an exception. It is limited to one checkable property that
  protects newcomers from a surprise bill. Other providers can be added on
  equal terms. Reviewers check every page of the repository against this limit.
- The newcomer path and the README's newcomer door get a link to the lab once it works end to end.
- The lab's scripts need maintenance for each OpenStack and Kolla-Ansible release. Each page states the releases on
  which the scripts were last run, like any other page.
- When the repository is created: add it to [current repositories](../repositories.md) and to the README's short
  list, and update this record's status to Accepted.

## Validation

- A newcomer with no prior lab runs the all-in-one variant and its first exercise in about one hour, following the
  guide alone.
- Nobody who followed the guide reports a cloud bill they did not expect.
- At least one variant other than Felcloud is contributed within six months.
