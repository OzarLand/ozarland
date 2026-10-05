# Contributing to OzarLand

This is the canonical contribution guide for every OzarLand repository. Each project repository adds only
its own build and test instructions.

## The first questions

Before proposing anything, answer these:

> 1. **Which operator task does this serve?** OzarLand exists for the people who run Kolla Ansible in production.
> 2. **Does it duplicate Kolla Ansible or an existing tool?** If it does, use what exists instead.

Feature requests must answer both explicitly.

## Workflow

```text
Issue → Branch → Implementation → Tests → Pull request → Review → Squash merge
```

1. **Open or pick an issue.** Significant work starts from an issue with acceptance criteria.
   Architectural changes start from an ADR (`docs/adr/`).
2. **Branch** from `main`: `feat/<issue>-<slug>`, `fix/<issue>-<slug>`, `docs/<slug>`, `chore/<slug>`.
3. **Commit** with [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) and a DCO sign-off
   (`git commit -s`). Types: `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `ci`, `chore`, `perf`, `revert`.
   Scope is the area: `feat(images): …`. Breaking changes use `!`.
4. **Open a pull request** using the template. The PR title becomes the squash commit message.
5. **Merge** with squash merge only. `main` must stay releasable.

Direct pushes to `main` are not allowed, except for the documented repository bootstrap.
While repositories are private on the GitHub Free plan this rule cannot be enforced by branch protection;
it is a maintainer commitment (see [GitHub conventions](docs/github-conventions.md)).

## Developer Certificate of Origin

Every commit must carry a `Signed-off-by:` line certifying the [Developer Certificate of Origin 1.1](https://developercertificate.org/).
OzarLand does not use a CLA. Web-based commits are signed off automatically (organization policy).

## Local checks and CI

Not defined yet. Tooling (linters, secret scanning, CI) will be decided through ADRs when the first
implementation work starts. The intended principle: CI logic lives in versioned scripts that run identically
on a workstation, so the project stays portable beyond GitHub.

## Content rules (publish-ready from day one)

Repositories are private today and will become public. Write everything as if it were public now:

- No secrets, credentials, private keys or `passwords.yml` in clear — ever.
- No customer, employer or project names; no real hostnames, domains or IP addresses.
- Use `example.org` / `example.com` (RFC 2606) and `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24` (RFC 5737) in examples.
- No dependency on a personal environment (paths such as `/Users/<name>`, private registries, internal mirrors).
- Real operational experience is welcome once anonymised and generalised into a pattern.

## Language and style

- All repository content is written in English.
- Markdown + Mermaid diagrams, rendered natively by GitHub.
- Prefer upstream vocabulary (Kolla Ansible verbs, OpenStack terms). Do not invent synonyms.

## Labels

Labels are shared across repositories: `type/*`, `area/*`, `priority/*`, `status/*`, plus `upstream`,
`security`, `good first issue`, `help wanted`. See [docs/github-conventions.md](docs/github-conventions.md).
