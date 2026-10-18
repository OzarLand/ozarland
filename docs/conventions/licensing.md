# Licensing

**Status: proposed, to be confirmed by the organization owner before any repository goes public.**

## Why it matters

Community content is only useful if people can copy a runbook into their internal wiki, adapt a pattern to their
platform, quote an experience report in a post-mortem, or publish a translation. The licence has to allow that
clearly, and contributors have to know under which terms they are giving their work.

## Proposal

| Content | Licence | Rationale |
|---|---|---|
| **Documentation** (runbooks, patterns, playbooks, reports, this repository's docs) | [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) | The standard licence for technical documentation. Allows copying, adaptation and commercial use with attribution. Compatible with the licence of the OpenStack documentation. No copyleft, so companies can reuse content internally without publishing their own wiki. |
| **Code** (scripts, snippets longer than a few lines, Ansible or configuration examples meant to be run) | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) | Already in place in this repository. The licence of OpenStack and Kolla, so examples can move upstream. Explicit patent grant. |

Each repository carries a `LICENSE` file (Apache-2.0, for code), a `LICENSE-docs` file (CC BY 4.0) and a sentence
in its README stating which applies to what. Short command examples inside a page are part of the documentation.

## Contributor terms

Contributions keep the Developer Certificate of Origin sign-off (`git commit -s`, automatic on web commits): the
contributor certifies they have the right to submit the content under the repository's licences. There is no
contributor licence agreement.

## Alternatives considered

| Option | Why not (for now) |
|---|---|
| CC BY-SA 4.0 for documentation | Share-alike would prevent companies from copying pages into internal, non-public wikis, which is one of the main intended uses. |
| Apache-2.0 for everything | Workable, but unusual for prose and awkward for attribution of text; CC BY is what readers of documentation expect. |
| CC0 / public domain | Loses attribution, which is the only thing contributors get back. |

## To confirm

- [ ] CC BY 4.0 for documentation, Apache-2.0 for code (or another combination).
- [ ] Add `LICENSE-docs` to this repository and to the blueprint.
- [ ] Add the licence sentence to every README (already present in the templates, marked "to confirm").
