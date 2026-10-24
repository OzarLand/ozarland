# ADR-0010: Felcloud wording

- **Status:** Accepted
- **Date:** 2026-10-24
- **Deciders:** @soufian-zaouam (owner decision)
- **Supersedes:** the Felcloud disclosure point of [ADR-0009](0009-openstack-quick-lab-repository.md); the rest of
  ADR-0009 stands.

## Context

[ADR-0009](0009-openstack-quick-lab-repository.md) created `openstack-quick-lab` and made Felcloud its first and
recommended variant, for one checkable reason: it is prepaid, so spending cannot exceed the credit loaded. It also
required a disclosure sentence about Felcloud, in the record and in the repository README.

## Decision

- The disclosure requirement of ADR-0009 is withdrawn.
- The only wording about Felcloud in OzarLand is: *"Felcloud was used to build and test OzarLand's labs because its
  prepaid model fits a lab with no surprise bill."*

Everything else in ADR-0009 stands: the one checkable reason for the recommendation, the link to the provider's own
terms, other providers and a personal-machine variant on equal terms, no requirement to use Felcloud, and the
stated tension with tool neutrality.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| **Withdraw the disclosure requirement, one fixed sentence (chosen)** | One wording everywhere; the recommendation rests only on its stated reason | Readers learn the reason for the recommendation, not more |
| Keep ADR-0009 unchanged | No change | Not the owner's decision |

## Consequences

- The `openstack-quick-lab` README uses the sentence above where it explains Felcloud.
- ADR-0009 keeps its text, as [ADR-0001](0001-record-architecture-decisions.md) requires, and is marked superseded
  on this point.
