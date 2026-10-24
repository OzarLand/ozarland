# Governance

OzarLand keeps governance deliberately light. The aim is to make it easy to ask, answer, share and review, and to
keep content trustworthy, without creating a bureaucracy.

## Roles

| Role | Who | What they do |
|---|---|---|
| **Contributor** | Anyone | Asks questions, answers them, proposes or improves content, reviews pull requests, confirms procedures in their own environment |
| **Maintainer** | Contributors trusted with write access to one or more repositories | Triage issues and discussions, review and merge pull requests, keep the structure and conventions consistent, protect the community from unsafe or sensitive content |
| **Operator reviewer** (automated) | Reviews open pull requests as an experienced operator and merges clear, safe content pull requests within the [review and merge policy](review-policy.md); escalates everything else |
| **Organization owner** | The founding maintainer today | Creates repositories, manages organization settings and membership, resolves conflicts that maintainers cannot |

Today OzarLand has a single maintainer and organization owner, @soufian-zaouam. Becoming a maintainer is based on
sustained, constructive contributions and is decided by the existing maintainers. The first external maintainers
are expected to be recruited from the first active contributors; see the [launch plan](launch-plan.md).

## How decisions are made

- **Content decisions** (is this runbook correct, is this pattern well described) are made in the pull request,
  by review and discussion. Disagreement is documented in the content as a trade-off, not resolved by authority.
- **Structural decisions** (a new repository, a change to templates or conventions, a licence change) are proposed
  as an issue or discussion in this repository and recorded as a short decision record in [`docs/adr/`](adr/README.md).
  The pull request that applies one follows the [review and merge policy](review-policy.md): agents merge it after a
  review without reservation, unless it is one of the risky changes the owner validates.
  Decision records exist so that newcomers can understand why things are the way they are; they are not a gate.
- **Code of conduct matters** are handled by the maintainers in private, as described in
  [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md).

## What maintainers commit to

- Acknowledge new questions and contributions within a reasonable time, and say so when they cannot.
- Review on substance (is it accurate, safe, well scoped) rather than on style.
- Never merge content that contains secrets, identifiable infrastructure data or unflagged destructive commands.
- Keep the maturity labels honest: a page is "validated" only when more than one operator has confirmed it.
- Prefer merging an imperfect but correct contribution and improving it later over blocking it.

## Independence

OzarLand is independent of any vendor, employer or foundation. Content may describe commercial products when
operators use them, with the same neutrality as any other approach. No company's product is required to take part
or to use the content.
