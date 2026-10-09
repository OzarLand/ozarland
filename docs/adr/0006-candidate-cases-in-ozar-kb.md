# ADR-0006: Candidate cases in ozar-kb

- **Status:** Proposed
- **Date:** 2026-10-09
- **Deciders:** @soufian-zaouam
- **Amends:** ADR-0005, section 3 (reproduction is mandatory).
- **Upstream check:** no. Upstream keeps no catalogue of Kolla Ansible failures; this is about where OzarLand keeps
  failures that were reproduced on a lab but are not qualified yet.

## Context

ADR-0005 says that a case enters `ozar-kb` only once its reproduction has passed several runs in a row and its
qualification has passed, and that a failure nobody knows how to reproduce stays an open issue.

Qualification needs the probes of `ozar-ops` and the qualification loop of `ozar-lab` (its milestone L5). Neither
exists yet. Meanwhile, `ozar-lab` has injected and observed more than twenty failures on its labs and written each
up in the case format of its ADR-0004: symptom, signature, cause, read-only evidence, remediation with its
preconditions and blast radius, reproduction task files, and the observations of the run. They are kept in `kb/` of
`ozar-lab`, which contradicts "ozar-lab holds no knowledge" (ADR-0005, section 5), and its ADR-0004 decided to move
them to `ozar-kb` with their task files.

Moving them as they are into `ozar-kb` would contradict section 3: none is qualified, and their investigation and
verification are commands, not probes.

## Decision

`ozar-kb` has two areas:

| Area | What it holds | Entry criterion | Read by `ozar-ops` |
|---|---|---|---|
| `cases/` | Qualified cases | ADR-0005, section 3, unchanged: reproduction passed several runs in a row, qualification passed, review by a maintainer | Yes |
| `candidates/` | Candidate cases | Injected and observed at least once on a qualification lab built by `ozar-lab`, with a clean undo; written up in the case format of `ozar-kb`, investigation and verification as read-only commands; review by a maintainer | Never |

- A candidate moves from `candidates/` to `cases/` when it is qualified, its commands having become probes.
- A failure observed but never reproduced on purpose is not a candidate: it stays an open issue of `ozar-kb`, with
  its evidence, as section 3 says.
- Every page of `candidates/` says that its content is not qualified and must not be run in production as is.
- The exact criteria, the format and the contribution rules are decided by ADR in `ozar-kb`.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| **A `candidates/` area in `ozar-kb`** (chosen) | The knowledge is in the repository meant for it, public and reviewed, as soon as it exists; `ozar-lab` holds no knowledge; promotion to `cases/` is a move within one repository | Two areas to keep apart; a reader may take a candidate for a proven case (mitigated by the warning on every page and by `ozar-ops` never reading `candidates/`) |
| Candidates stay in `ozar-lab` until qualified | ADR-0005 unchanged | `ozar-lab` holds knowledge for a long time (until L5 at least); `ozar-kb` stays empty; contradicts the decision of `ozar-lab` ADR-0004 |
| Candidates in `cases/` with a status field | One area | `cases/` no longer means "proven"; `ozar-ops` would have to filter by status, and one mistake runs an unproven case |

## Consequences

- `ozar-kb` can be bootstrapped now and receive the candidates of `ozar-lab`, with their history.
- `ozar-ops` reads `cases/` only. Its versioning contract with `ozar-kb` (ADR-0005, follow-up 2) covers `cases/`
  only.
- The bar for `cases/` does not move: a qualified case still needs everything section 3 asks.
- Follow-ups: the case format and contribution ADR of `ozar-kb` defines both areas; `ozar-lab` reads the candidates
  from a pinned version of `ozar-kb` and removes its own `kb/`.

## Validation

- No file under `cases/` of `ozar-kb` is unqualified.
- `ozar-ops` never loads a file from `candidates/`.
