# Licensing

**Status: confirmed by the organization owner on 2026-10-18.**

## Decision

Every OzarLand repository, and everything in it (documentation, runbooks, patterns, playbooks, reports, scripts,
configuration examples), is licensed under the **[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)**.

## Why

- It is the licence of OpenStack, Kolla and Kolla-Ansible, so content and examples can move upstream without friction.
- It is permissive: operators can copy a runbook into an internal wiki, adapt a pattern, or reuse a script,
  commercially or not, as long as attribution and the licence notice are kept.
- One licence for everything keeps the rules simple for contributors and readers. Apache-2.0 is less common than
  Creative Commons for prose, but it is well understood by the OpenStack community and perfectly valid for
  documentation.

## What it means in practice

- Each repository carries the `LICENSE` file (the Apache-2.0 text) and a one-line licence statement in its README.
- Reusing content requires keeping the attribution and the licence notice. A link to the source page plus
  "Licensed under Apache-2.0" is enough.
- Contributions are accepted under the same licence, certified by the Developer Certificate of Origin sign-off
  (`git commit -s`, automatic on web commits). There is no contributor licence agreement.
- Content quoted from upstream documentation stays under its own licence and is attributed.

## Alternatives considered

| Option | Why not |
|---|---|
| CC BY 4.0 for documentation, Apache-2.0 for code | Two licences to explain; the boundary between "a page" and "a script in a page" is blurry in runbooks. |
| CC BY-SA 4.0 | Share-alike would prevent copying pages into internal, non-public wikis, one of the main intended uses. |
| CC0 / public domain | Loses attribution, which is what contributors get back. |
