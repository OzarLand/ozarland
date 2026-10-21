# Launch plan

A concrete sequence to turn the repositioning into a working community. Each step names what has to be done and
who can do it. "Owner" means an organization owner is needed because the action requires GitHub permissions that
a repository contributor does not have.

## Step 0: finish the repositioning (this repository)

| Action | Who | Status |
|---|---|---|
| Merge the repositioning pull request into `main` | Maintainer | Pending review |
| Update the repository description and topics (values below) | Owner | To do, manual |
| Update the organization description (value below) | Owner | To do, manual |
| Enable GitHub Discussions on `ozarland` and create the five categories listed in [github-conventions.md](github-conventions.md) | Owner | To do, manual |
| Apply the shared label taxonomy | Owner | To do, manual |
| Licence: Apache-2.0 for all content ([conventions/licensing.md](conventions/licensing.md)) | Owner | Decided 2026-10-18 |
| Set the contact channels in `SECURITY.md` and `CODE_OF_CONDUCT.md`: GitHub issues for questions, errors and proposals; private vulnerability reporting for security problems and sensitive data; a LinkedIn message to the owner for the code of conduct and anything personal; no e-mail address | Owner | Done 2026-10-21 |
| `ozarMVP` and `OzarBuild` stay private and outside the community scope | Owner | Decided 2026-10-18 |

## GitHub metadata

**Organization description** (160 characters max on GitHub):

> A community of OpenStack operators sharing deployment practices, runbooks, upgrade experiences and lessons from production. Tool-neutral, open to all.

**Repository `ozarland` description:**

> Home of the OzarLand community: a knowledge-sharing space where OpenStack operators share runbooks, deployment patterns, upgrade experiences and help each other.

**Repository `ozarland` topics:** `openstack`, `openstack-operations`, `runbooks`, `sre`, `cloud-operations`,
`knowledge-sharing`, `community`, `kolla-ansible`, `day-2-operations`

**Organization profile README** (optional, requires a public `.github` repository): reuse the first two sections of
the main README.

## Step 1: seed content (before inviting anyone)

A community with empty repositories does not start. Before announcing anything:

| Action | Target |
|---|---|
| Write 5 to 10 VM runbooks from real incidents, anonymised, using the runbook template | Done: 10 seed runbooks in the `openstack-vm-runbooks` blueprint, derived from the incidents in *OpenStack, the Day After Tomorrow* |
| Write 2 to 3 Kolla-Ansible deployment patterns from real platforms (for example: all-in-one lab, three-controller production with OVN, separated storage network) | `kolla-ansible-deployment-patterns` blueprint |
| Write 1 upgrade experience report | `openstack-upgrade-playbooks` blueprint, or a Discussion |
| Open 3 to 5 genuine open questions in Discussions to show what the Q&A space is for | `ozarland` Discussions |

Seed content is the standard the community will copy. It is worth writing carefully.

## Step 2: create the phase 1 repositories

| Action | Who |
|---|---|
| Create `openstack-vm-runbooks` and `kolla-ansible-deployment-patterns` from the blueprints and the shared template files | Done 2026-10-18 |
| Move the seed content into them through pull requests, so the first pages show the expected workflow | Done for the VM runbooks (PR open for review); Kolla-Ansible patterns still to write |
| Enable Discussions and labels on each | Owner |
| Update the directory in the main README from "Planned" to "Active" | Maintainer |

## Step 3: go public

| Action | Who |
|---|---|
| Run the go-public checklist in [governance.md](governance.md) on `ozarland` and the two phase 1 repositories | Maintainer, Owner |
| Make the three repositories public | Owner |
| Create the public `.github` organization repository with the organization profile README and the shared community files | Owner |
| Enable branch protection, secret scanning, push protection | Owner |

## Step 4: invite the first contributors

| Action | Notes |
|---|---|
| Invite 5 to 10 operators you know personally, with one specific ask each ("could you review this runbook against your 2025.1 platform?") | Specific asks get answered; "please contribute" does not |
| Post on OpenStack community channels (openstack-discuss mailing list, OpenInfra forums, relevant Slack and Matrix rooms, LinkedIn) once there is content to show | Lead with a useful runbook, not with the organisation |
| Tag 5 to 10 items `good first contribution` ("confirm this runbook on your release", "add the OVS variant of this page") | Validation reports are the easiest first contribution |
| Answer every question in the first weeks, even with "I don't know, has anyone else seen this?" | Response speed in the first weeks sets the tone |

## Step 5: grow and adjust

| Signal | Action |
|---|---|
| Two or more upgrade reports | Create `openstack-upgrade-playbooks` |
| Runbooks arriving outside the VM scope | Create `openstack-operations-runbooks` (see [repositories.md](repositories.md)) |
| A contributor reviews and answers regularly for a few months | Offer them a maintainer role on the repository they are active in |
| A template is being skipped or fought | Simplify it |
| Discussions are more active in a repository than in `ozarland` | Enable Discussions there too; keep `ozarland` for cross-cutting topics |

## Success criteria

Not the number of repositories. The signs that matter, at three months:

- Questions get answers from someone other than the maintainer.
- At least one page has been validated by someone other than its author.
- At least one contributor has reported a difference ("works, but on 2024.2 you also need to…"), and the page was
  updated.
- Someone found a runbook through a search engine and used it.
