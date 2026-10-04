# Governance

## Today

OzarLand is in its **private foundation phase** with a single maintainer, who is the organization owner.
Decisions are taken by the maintainer and recorded as ADRs. Proposed ADRs stay "Proposed" until the
maintainer explicitly accepts them.

## Decision making

- Cross-project decisions → an ADR in `ozarland/docs/adr/`.
- Project-level decisions → an ADR in that project's `docs/adr/`.
- An ADR is never deleted; a replaced decision is marked "Superseded by ADR-NNNN".
- A new repository, a new mandatory dependency or a new product requires an ADR.

## Independence

OzarLand is an independent open-source project around Kolla Ansible. It is not affiliated with or endorsed
by the OpenInfra Foundation. Everything OzarLand ships must work with upstream Kolla Ansible alone: using
OzarLand must never require a commercial product or a specific company's infrastructure.

## From private to public

Each repository goes public individually, after a go-public review:

1. Full-history secret scan is clean; any historical secret is rotated and the history rewritten.
2. Content review: no customer, employer or project names; no real hostnames, domains or IP addresses; no personal paths.
3. `SECURITY.md` and `CODE_OF_CONDUCT.md` carry a real contact address; private vulnerability reporting is enabled.
4. A ruleset protects `main` (pull request required, checks required, no force push).
5. Secret scanning, push protection and Dependabot alerts are enabled.
6. The organization `.github` repository is created **public** with the shared community files; per-repository copies are removed.
7. The README states maturity honestly.

## Maintainers

| Name | Role |
|---|---|
| @soufian-zaouam | Founding maintainer, organization owner |

The maintainer model (additional maintainers, review rules, technical steering) will be written before the
Community phase.
