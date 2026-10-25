# Agents

OzarLand uses a few AI agents to keep the community repositories moving. They follow the same rules as human
contributors ([review and merge policy](review-policy.md)) and are always identified as AI agents. What they do,
what keeps them in check and what they made possible: [how OzarLand is built](how-ozarland-is-built.md).

## Who writes, who reviews, who merges

| Agent | Writes | Reviews | Merges |
|---|---|---|---|
| **Author** | Runbooks and deployment pages, from material the owner provides (incidents, a book, lab runs) | No | No |
| **Documentation** | The community pages of `ozarland`: newcomer path, conventions, plans | No | No |
| **Quick-lab documentation** | The guides of [`openstack-quick-lab`](https://github.com/OzarLand/openstack-quick-lab): its variants and their safety rules | No | No |
| **Operator reviewer** | No | Every pull request, as an experienced OpenStack operator, with the content checker; about every 4 hours | Pull requests that pass its review without reservation, never its own |
| **Lab reviewer** | Lab confirmations, in separate pull requests | Runs the steps of pages on a disposable OpenStack lab and reports what really happens | No |
| **Manager** | No | No | No: it reports progress to the owner and passes on the owner's decisions |

No agent reviews or merges a pull request it wrote: the `Author:` line of each agent-authored pull request names the
agent and says it is an AI agent (for example `Author: OzarLand author agent (AI agent)`).

## What people decide

- **The owner** sets the rules and validates the risky changes: rules and agent roles, the checker, `LICENSE`,
  `SECURITY.md`, `CODE_OF_CONDUCT.md`, page deletions, making a repository public, GitHub settings. The full list is
  in the [review and merge policy](review-policy.md). Commits are signed off in the owner's name, and the owner takes
  responsibility for them under the [DCO](https://developercertificate.org/).
- **Human operators** are the only ones who can make a page `validated`, by confirming it on their own platform.
  An agent never confirms a page it wrote.

## The rules every agent follows

- Content in English only.
- `ozarland` is the newcomers' entry point and links out to the content repositories.
- New pages are `draft`; a lab confirmation is recorded by the lab reviewer in a separate pull request.
- AI use is disclosed openly, at repository level and in each agent-authored pull request; commit messages stay
  plain.
- The [sensitive data](conventions/sensitive-data.md) rules apply as for everyone.

The agents' detailed working instructions are in [`.claude/agents/`](../.claude/agents/). The documentation agent has
no definition of its own: it follows the [author definition](../.claude/agents/ozarland-author.md) (writing rules,
disclosure, sign-off), limited to the community pages of `ozarland`, and never reviews or merges. The quick-lab documentation agent follows
the same definition, limited to the guides of `openstack-quick-lab`.

## Tools the agents share

- [`tools/check_content.py`](../tools/check_content.py): conventions checker, runnable by anyone before opening a pull request.
- [`tools/coverage_report.py`](../tools/coverage_report.py) with [`docs/topics.yml`](topics.yml): which topics each repository covers, and which are missing.
