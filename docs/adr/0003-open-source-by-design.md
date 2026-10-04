# ADR-0003: Open source by design

- **Status:** Accepted
- **Date:** 2026-10-04
- **Deciders:** @soufian-zaouam

## Context

OzarLand is intended to become an open-source ecosystem used and maintained by the OpenStack operator community.
Its repositories start private, to give the projects time to be scoped and stabilised before they are opened.
Decisions taken during the private phase must not make opening the projects difficult later.

## Decision

1. **Licence:** every OzarLand repository is licensed under the **Apache License 2.0**, the licence of OpenStack,
   Kolla and Kolla Ansible. Code and documentation can therefore move upstream without friction, and the explicit
   patent grant suits the enterprises that operate OpenStack.
2. **Contributions:** the **Developer Certificate of Origin** (`Signed-off-by:`) is required; no CLA.
3. **Public-ready content from the first commit:** no secrets, no customer, employer or project names, no real
   hostnames, domains or IP addresses, no dependency on a personal environment. Examples use RFC 2606 domains and
   RFC 5737 addresses.
4. **Open workflow from the first commit:** issues, branches, pull requests, documented decisions — as if the
   repositories were already public.
5. **Independence:** using OzarLand must never require a commercial product, a SaaS, or a specific company's
   infrastructure.
6. **Progressive opening:** each repository goes public individually after the go-public review described in
   [governance](../governance.md).

## Options considered

| Option | Pros | Cons |
|---|---|---|
| Apache-2.0 + DCO (chosen) | Same as upstream; patent grant; low contributor friction | Permissive: forks may stay closed |
| GPL/AGPL | Forces openness of derivatives | Incompatible culture with upstream; deters operator companies |
| CLA | Relicensing flexibility | Contributor friction; OpenStack itself moved away from CLAs |

## Consequences

- Opening a repository is a review, not a rewrite.
- Each repository carries its own `LICENSE` file.
