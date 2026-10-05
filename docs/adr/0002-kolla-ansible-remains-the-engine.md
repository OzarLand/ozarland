# ADR-0002: Kolla Ansible remains the engine

- **Status:** Accepted
- **Date:** 2026-10-04 (clarified 2026-10-05)
- **Deciders:** @soufian-zaouam

## Context

Operators who run OpenStack with Kolla Ansible in production need more than deployment: environments under control,
traceable changes, safe upgrades, local patches, host maintenance, checks before acting. Kolla Ansible already deploys
and manages the lifecycle of OpenStack services in containers, and Kolla builds and customises the images.
Replacing or forking that engine would duplicate a mature upstream project and create a maintenance burden no small
team can carry.

## Decision

1. **Kolla Ansible is used as it is.** OzarLand does not fork it and does not redo what it already does.
2. **OzarLand exists for the operator.** A function belongs in OzarLand when an operator needs it to run Kolla Ansible
   in production — not because Kolla Ansible lacks a feature.
3. **No duplication.** Before adding a function, check that Kolla Ansible (or another existing tool) does not already
   provide it; if it does, use it.
4. **Kolla Ansible stays visible.** OzarLand keeps the upstream vocabulary and never hides Kolla Ansible's behaviour or
   output from operators.
5. **Eject path.** Removing OzarLand must leave a plain, working Kolla Ansible setup.

When a generic Kolla Ansible bug or documentation gap is found along the way, it can be reported upstream; this is a
good practice, not the purpose of OzarLand.

## Consequences

- OzarLand's scope is defined by operator tasks, which keeps it focused and understandable.
- OzarLand stays small and benefits from every upstream improvement.
- OzarLand projects must track OpenStack series and Kolla Ansible releases closely.
