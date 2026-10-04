# GitHub conventions

## Organization settings (applied 2026-10-04)

| Setting | Value |
|---|---|
| Plan | Free |
| Repository visibility | All repositories private during the foundation phase |
| Base member permission | Read |
| Repository creation by members | Disabled (owners only) — avoids repository sprawl |
| Forking of private repositories | Disabled |
| Visibility change, deletion, transfer | Owners only |
| Team and Pages creation by members | Disabled |
| App access requests | Members only; repository admins cannot install apps without approval |
| Default branch | `main` |
| Commit sign-off on web commits | Required for all repositories (DCO) |
| Immutable releases | Required for all repositories |
| Default repository labels | OzarLand taxonomy (below) |
| GitHub Actions | GitHub-created actions only, pinned to a full commit SHA; read-only `GITHUB_TOKEN`; Actions cannot approve pull requests; approval required for outside contributors' workflows |
| Two-factor authentication required | Pending owner action |

**Limits of the Free plan for private repositories:** no branch protection or rulesets, no secret scanning or push
protection, no code scanning, no private vulnerability reporting, and organization-wide community files only work
from a public `.github` repository. These become available when a repository goes public. Until then, the pull
request workflow is a maintainer commitment.

## Labels

| Group | Labels |
|---|---|
| Type | `type/bug`, `type/feature`, `type/epic`, `type/docs`, `type/adr`, `type/spike`, `type/chore` |
| Area | `area/deploy`, `area/images`, `area/upgrade`, `area/secrets`, `area/day2`, `area/lab`, `area/ci`, `area/governance` |
| Priority | `priority/critical`, `priority/high`, `priority/medium`, `priority/low` |
| Status | `status/triage`, `status/blocked`, `status/needs-decision` |
| Other | `upstream`, `security`, `good first issue`, `help wanted` |

## Branches, commits, pull requests

- `main` is always releasable. Work happens on short-lived branches: `feat/<issue>-<slug>`, `fix/…`, `docs/…`, `chore/…`.
- Commits follow [Conventional Commits 1.0](https://www.conventionalcommits.org/en/v1.0.0/) with a DCO sign-off.
- Pull requests are squash-merged; the PR title becomes the commit message.
- No AI co-author trailers in commits.
- The first content of each repository was added through a single bootstrap pull request.

Issue planning, milestones, versioning and release conventions will be defined later.
