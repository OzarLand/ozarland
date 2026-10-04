# ADR-0001: Record architecture decisions

- **Status:** Accepted
- **Date:** 2026-10-04
- **Deciders:** @soufian-zaouam

## Context

OzarLand is meant to become a community project that outlives its founders. The reasons behind decisions are
as important as the decisions themselves, and must be readable by future maintainers and users.

## Decision

Significant decisions are recorded as Architecture Decision Records (ADRs) in Markdown, in the repository they
concern: organization-level decisions in `ozarland/docs/adr/`, project decisions in each project's `docs/adr/`.
ADRs are numbered sequentially per repository, never renumbered and never deleted. A replaced decision is marked
"Superseded by ADR-NNNN". Every ADR states whether upstream already solves the problem.

## Consequences

- Decisions become reviewable through pull requests like any other change.
- When repositories go public, the reasoning goes public with them.
- Writing an ADR costs time; it is reserved for decisions that are expensive to reverse or that affect several projects.
