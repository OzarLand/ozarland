# Contributing to OzarLand

Thank you for sharing what you know. This guide applies to every OzarLand community repository. It is short on
purpose: the goal is to make sharing easy, not to make it formal.

## Ways to contribute

| You want to… | Do this |
|---|---|
| Ask for help with an operational problem | Open a **Q&A discussion**, or an issue with the *Question* template if you want it tracked |
| Share a problem you solved | Open an issue with the *Problem solved* template, or go straight to a pull request with a runbook |
| Add or improve a runbook, pattern or playbook | Open a pull request using the matching template from [`community/templates/`](community/templates/) |
| Tell what happened during an upgrade, an incident or a migration | Start an **Experience reports** discussion, or submit an experience-report page |
| Confirm that a page works (or does not) in your environment | Comment on the page's pull request or open a *Documentation proposal* issue with your release, deployment method and result. This is how pages become **validated** |
| Fix a typo, a broken link, an outdated command | Open a pull request directly, no issue needed |
| Propose a change to the community itself (templates, structure, a new repository) | Start an **Ideas** discussion in `ozarland` |

If you are not sure where something goes, open a discussion. Someone will point you to the right place.

## What a good contribution contains

Operational knowledge is only reusable with its context. Whatever you share, give:

- the **OpenStack release(s)** (upstream names, for example `2025.1`);
- the **components** involved (Nova, Neutron, Cinder, MariaDB, RabbitMQ, Ceph, OVN…);
- the **deployment method** (Kolla-Ansible, OpenStack-Ansible, Charmed, a vendor distribution, manual);
- the **environment conditions that matter** (topology, network plugin, storage backend, OS);
- what you **already checked** or **actually did**, with the commands;
- what you **are not sure about**.

The templates ask for these fields so that you do not have to remember them. See
[content metadata](docs/conventions/content-metadata.md) for the full list.

## The rules that are not optional

1. **No sensitive data.** No secrets, no real hostnames, domains, IP or MAC addresses, no customer, employer or
   person names, no unredacted logs. See [sensitive data](docs/conventions/sensitive-data.md) for how to redact.
   Maintainers will ask for redaction before anything else.
2. **Flag risky commands.** State-changing commands carry a ⚠️ warning; destructive ones carry a 🛑 warning with
   what can be lost and what to check first. See [risk warnings](docs/conventions/risk-warnings.md). Unflagged
   destructive commands are not merged.
3. **Say where it was observed.** A solution that worked on your platform is documented as exactly that. Never
   present a procedure or an upgrade path as universally valid or officially supported without a reference.
4. **Respect other approaches.** When your way differs from a documented one, add yours with its context. Do not
   replace someone else's approach with your own.
5. **Follow the [code of conduct](CODE_OF_CONDUCT.md).**

## Mechanics

- Content is **Markdown**, in **English**, with Mermaid diagrams when a diagram helps.
- Work on a branch, open a **pull request** against `main`. One page per pull request is easiest to review.
- Sign off your commits (`git commit -s`) to certify the
  [Developer Certificate of Origin](https://developercertificate.org/). Web commits are signed off automatically.
  There is no contributor agreement.
- Pull requests are **squash-merged** after one maintainer approval. Reviews focus on accuracy, safety and scope,
  not on style.
- Contributions are published under the Apache License 2.0, which covers all content, documentation and code alike
  (see [licensing](docs/conventions/licensing.md)).

## Reviewing

Reviewing is contributing. Useful review comments:

- "Confirmed on 2025.1 / Kolla-Ansible / OVN." (adds a confirmation and may move the page to validated)
- "On OpenStack-Ansible the service is restarted with … instead." (adds a variant)
- "This command also deletes X, it needs a destructive warning." (safety)
- "I believe the cause is actually Y, because …" (accuracy, discussed in the thread, both views kept if unresolved)

Reviewers do not need to be maintainers. Maintainers merge; anyone can review.

## Conventions and templates

- [Content conventions](docs/conventions/README.md): metadata, runbook structure, risk warnings, sensitive data,
  licensing.
- [Document templates](community/templates/): runbook, deployment pattern, upgrade playbook, experience report.
- [Knowledge lifecycle](docs/knowledge-lifecycle.md): how content moves from an open question to a validated page.
- [GitHub conventions](docs/github-conventions.md): discussions, issues, labels, branches.
