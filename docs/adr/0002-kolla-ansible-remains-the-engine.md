# ADR-0002: Kolla Ansible remains the engine

- **Status:** Accepted
- **Date:** 2026-10-04
- **Deciders:** @soufian-zaouam
- **Upstream check:** This ADR *is* the upstream check, applied to the whole organization.

## Context

Kolla Ansible already deploys and manages the lifecycle of OpenStack services in containers, and Kolla builds and
customises the images. What production teams lack is around it: reproducibility, traceability, safe operations,
governance. Re-implementing the engine would duplicate a mature upstream project, fragment the community and create
a maintenance burden no small team can carry.

## Decision

OzarLand builds **around** Kolla Ansible and never replaces it:

1. OzarLand does not re-implement any capability that Kolla Ansible or Kolla already provides correctly.
2. Before any feature, the question is asked and answered in writing: *"must this live in OzarLand, or in Kolla Ansible?"*
3. Generic gaps — true for every Kolla Ansible user — are contributed upstream first. A temporary OzarLand workaround
   is allowed only if it is clearly marked and linked to the upstream work (label `upstream`).
4. OzarLand keeps the upstream vocabulary and never hides Kolla Ansible's behaviour or output from operators.
5. Removing OzarLand must leave a plain, working Kolla Ansible setup (eject path).

## Consequences

- OzarLand stays small and benefits from every upstream improvement.
- Some valuable work will happen upstream rather than in OzarLand; that is a success, not a loss.
- OzarLand projects must track OpenStack series and Kolla Ansible releases closely.
