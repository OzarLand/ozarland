# ADR-0008: OzarLand becomes a knowledge-sharing community for OpenStack operators

- **Status:** Proposed (becomes Accepted when the repositioning pull request is merged into `main`)
- **Date:** 2026-10-18
- **Deciders:** @soufian-zaouam
- **Supersedes:** ADR-0002, ADR-0004, ADR-0005, ADR-0006, ADR-0007. ADR-0001 (record decisions) and ADR-0003
  (open source by design) stand, with the adjustments below.

## Context

OzarLand was founded in October 2026 as an open-source operator toolkit around Kolla Ansible: an engine for
operations (`ozar-ops`), a deployment toolkit (`ozar-deploy`), a tested knowledge base (`ozar-kb`) and a
qualification lab (`ozar-lab`). ADR-0002 to ADR-0007 describe that design.

Two things became clear while scoping it:

1. The value operators asked for was the **knowledge** (how to investigate a failure, what causes it, what to do),
   not the engine that runs it. The toolkit design spent most of its effort on how to encode and qualify that
   knowledge mechanically, which raised the bar for contributing it to a level very few operators could meet.
2. A toolkit, however neutral in intent, is perceived as a way of operating OpenStack that its authors recommend.
   Operators run OpenStack with many tools and distributions; a space built around one toolchain excludes most
   of them from the start.

The tooling repositories have been archived. The question this record answers is what OzarLand is instead.

## Decision

**OzarLand is a collaborative knowledge-sharing space for OpenStack operators.** Its purpose is to let operators
share experiences, document solutions and learn from each other, with no imposed tools and no single way of
operating OpenStack. The mission and principles are in [docs/vision.md](../vision.md).

Consequences for earlier decisions:

| Earlier decision | Now |
|---|---|
| ADR-0002, Kolla Ansible remains the engine | Superseded. OzarLand has no engine. Kolla-Ansible is one deployment method among those the community documents, and gets a dedicated patterns repository because many operators use it, not because OzarLand prefers it. |
| ADR-0003, open source by design | Stands. Apache-2.0 remains for code. A documentation licence (proposed CC BY 4.0) is added for the content that is now the bulk of the organisation; see [licensing](../conventions/licensing.md). DCO stays; no CLA. Public-ready content from the first commit stays, with the [sensitive data](../conventions/sensitive-data.md) rules. |
| ADR-0004, `ozar-` naming and initial repositories | Superseded. Community repositories are named after their content (`openstack-vm-runbooks`, `kolla-ansible-deployment-patterns`), with no product prefix. The initial repository set is in [docs/repositories.md](../repositories.md). A new repository still requires a short decision record, to avoid sprawl. |
| ADR-0005, knowledge base and lab repositories | Superseded. Knowledge is contributed as human-readable pages with explicit validity metadata and peer confirmation, not as machine-qualified cases. No qualification lab is required to contribute. |
| ADR-0006 and ADR-0007, candidate cases and lab trials | Superseded with ADR-0005. The idea they protected, that unconfirmed knowledge must be visibly distinguished from confirmed knowledge, survives as the `draft` / `validated` / `experimental` statuses of the [knowledge lifecycle](../knowledge-lifecycle.md). |
| ADR-0001, record decisions | Stands, lighter. Decision records are kept for structural decisions (repositories, templates, licence) so newcomers understand why things are as they are. They are not required for content decisions, and the "upstream check" field becomes optional. |

## Options considered

| Option | Pros | Cons |
|---|---|---|
| **Repositioning as a knowledge-sharing community (chosen)** | Low barrier to contribute; welcomes every deployment method; knowledge is the value operators asked for; the existing hub repository and conventions are reusable | Content quality depends on peer review rather than automated qualification; needs active community animation to start |
| Continue the toolkit | Design work already done; a working tool is a strong attractor | Excludes operators who do not use Kolla-Ansible; contribution bar too high; perceived as prescriptive |
| Both in the same organisation | Nothing lost | Mixed message; the toolkit would be read as "the OzarLand way"; maintenance split across two very different kinds of project |
| New organisation for the community | Clean history | Loses the name, the existing hub and the settings already in place; the history is short and single-author, so there is little to gain |

## Git history

The history of `ozarland` before this record describes the toolkit. It is kept as it is:

- it is short (eight commits), single-author, and contains nothing sensitive;
- rewriting it would break the references to pull requests #1 to #9 and to this organisation's archived
  repositories, invalidate every existing clone, and invalidate the verified signatures of the existing commits;
- a visible, honest transition is consistent with the community's principles. A newcomer who reads this record
  understands where OzarLand comes from.

The repositioning is applied as new commits on `main`. The superseded records stay in `docs/adr/` with their status
updated, as ADR-0001 requires. See the main README for the current state, and this record for the transition.

## Consequences

- The main README, vision, governance, contribution guide, security policy and GitHub templates are rewritten for
  the community. Shared templates and repository blueprints are added under `community/`.
- The organisation and repository descriptions and topics are updated by the organization owner.
- GitHub Discussions are enabled on `ozarland` as the community's meeting place during the launch.
- The archived tooling repositories stay archived and private. They are mentioned in the README for honesty, not
  listed in the directory of community repositories.
- Success is measured by whether operators find help, share experiences and improve content together, not by the
  number of repositories. The [launch plan](../launch-plan.md) lists the first steps.

## Validation

- Within three months of going public: at least one question answered by someone other than the maintainer, and
  at least one page validated by someone other than its author.
- No content in the organisation prescribes a tool or an architecture as the correct one.
