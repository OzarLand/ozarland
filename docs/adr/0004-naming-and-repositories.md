# ADR-0004: Product naming and initial repositories

- **Status:** Accepted
- **Date:** 2026-10-04
- **Deciders:** @soufian-zaouam

## Context

The organization needs a recognisable naming scheme and a starting set of repositories. Creating many repositories
early makes an ecosystem look larger than it is and multiplies maintenance; creating too few mixes concerns with
different users and release rhythms.

## Decision

1. **Naming:** every OzarLand product is prefixed `ozar-` (`ozar-<function>`). Names are lowercase, kebab-case,
   and describe a function, not a technology.
2. **Initial repositories** (all private during the foundation phase):

   | Repository | Role |
   |---|---|
   | `ozarland` | Home of the ecosystem: vision, governance, cross-project decisions, contribution guide |
   | `ozar-deploy` | Deployment lifecycle around Kolla Ansible |
   | `ozar-ops` | Day-2 operations |

3. **Deployment and Day-2 are separate products**, because they serve different moments, carry different risk
   (changing the platform versus observing it) and will evolve at different speeds.
4. **New repositories** require an ADR showing a distinct audience, release cadence or trust level.
5. **Deferred on purpose:** an organization `.github` repository (useful only once public), a lab repository,
   example repositories, a website.

## Consequences

- The ecosystem starts small and readable.
- Repository renames remain possible (GitHub redirects old URLs), but product names should be stable before going public.
