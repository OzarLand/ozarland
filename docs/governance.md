# Governance

OzarLand keeps governance deliberately light. The aim is to make it easy to ask, answer, share and review, and to
keep content trustworthy, without creating a bureaucracy.

## Roles

| Role | Who | What they do |
|---|---|---|
| **Contributor** | Anyone | Asks questions, answers them, proposes or improves content, reviews pull requests, confirms procedures in their own environment |
| **Maintainer** | Contributors trusted with write access to one or more repositories | Triage issues and discussions, review and merge pull requests, keep the structure and conventions consistent, protect the community from unsafe or sensitive content |
| **Organization owner** | The founding maintainer today | Creates repositories, manages organization settings and membership, resolves conflicts that maintainers cannot |

Today OzarLand has a single maintainer and organization owner, @soufian-zaouam. Becoming a maintainer is based on
sustained, constructive contributions and is decided by the existing maintainers. The first external maintainers
are expected to be recruited from the first active contributors; see the [launch plan](launch-plan.md).

## How decisions are made

- **Content decisions** (is this runbook correct, is this pattern well described) are made in the pull request,
  by review and discussion. Disagreement is documented in the content as a trade-off, not resolved by authority.
- **Structural decisions** (a new repository, a change to templates or conventions, a licence change) are proposed
  as an issue or discussion in this repository and recorded as a short decision record in [`docs/adr/`](adr/README.md).
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

## Going public

The repositories are private while the repositioning is completed. Before a repository becomes public:

1. A full-history scan confirms no secret was ever committed.
2. A content review confirms no customer, employer or project names, no real hostnames, domains, addresses or
   personal paths.
3. `SECURITY.md` and `CODE_OF_CONDUCT.md` carry a working contact address.
4. The documentation licence is confirmed (see [conventions/licensing.md](conventions/licensing.md)).
5. GitHub Discussions, issue templates and labels are in place.
6. Branch protection on `main` (pull request required, no force push) and secret scanning are enabled.
