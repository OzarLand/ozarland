# ADR-0011: Variant-specific exercises in the quick lab

- **Status:** Accepted
- **Date:** 2026-10-25
- **Deciders:** @soufian-zaouam (owner decision)
- **Amends:** the point "Every exercise works on any variant" of
  [ADR-0009](0009-openstack-quick-lab-repository.md); the rest of ADR-0009 stands.

## Context

[ADR-0009](0009-openstack-quick-lab-repository.md) says that every exercise of `openstack-quick-lab` works on any
variant, so that no exercise depends on one provider. It also planned "a multinode variant later, once the all-in-one
lab is used and stable".

On 2026-10-25 the owner decided to start the multinode variant now: one controller and two computes (three VMs),
designed to grow to three controllers and two computes (five VMs) with the same scripts and one setting. Some of the
operations operators most need to practise cannot run on a single VM: live migration, evacuation and fencing, host
maintenance, rescheduling, and with three controllers the loss of a controller and the recovery of the database and
message bus clusters.

## Decision

- **An exercise may need one variant,** for example the two computes of the multinode variant, **if it says so at
  the top**, before any step.
- **An exercise that can run on every variant still must.** The all-in-one exercises stay runnable on every variant.
- The requirement is about the lab's shape (one VM, several computes, several controllers), never about a provider:
  no exercise requires a particular cloud.
- **Recorded here as well:** the multinode variant was started on 2026-10-25 by owner decision, ahead of ADR-0009's
  "later, once the all-in-one lab is used and stable".

## Options considered

| Option | Pros | Cons |
|---|---|---|
| **Exercises may need a variant, stated at the top (chosen)** | Multinode operations can be practised; a reader knows before starting whether their lab fits | Not every exercise runs everywhere |
| Keep "every exercise works on any variant" | Simplest for readers | Rules out the operations that need more than one host |
| Separate repository for multinode exercises | Keeps the rule intact | Splits the quick lab in two; the variants already share scripts |

## Consequences

- Each exercise that needs a variant states it at the top, with what it needs (for example "Needs the multinode
  variant: two computes").
- The exercises index can show which exercises run on which variant.
- ADR-0009 keeps its text, as [ADR-0001](0001-record-architecture-decisions.md) requires, and is marked amended on
  this point.
