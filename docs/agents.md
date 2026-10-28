# Agents

OzarLand uses a few AI agents to keep the community repositories moving. They follow the same rules as human
contributors ([review and merge policy](review-policy.md)) and are always identified as AI agents. What they do,
what keeps them in check and what they made possible: [how OzarLand is built](how-ozarland-is-built.md).

## Who writes, who reviews, who merges

OzarLand runs four agents, one per role, across all four repositories (`ozarland`, `openstack-vm-runbooks`,
`kolla-ansible-deployment-patterns`, `openstack-quick-lab`).

| Agent | Writes | Reviews | Merges |
|---|---|---|---|
| **Author** | Every page: runbooks, deployment patterns, the community pages of `ozarland` and the guides and exercises of [`openstack-quick-lab`](https://github.com/OzarLand/openstack-quick-lab), from material the owner provides (incidents, a book, lab runs) | No | No |
| **Operator reviewer** | No | Every pull request of the four repositories, as an experienced OpenStack operator, with the content checker; every hour | Pull requests that pass its review without reservation, never its own |
| **Lab reviewer** | Lab confirmations, and the scripts of `openstack-quick-lab`, which only a lab can test | Runs the steps of pages on a disposable OpenStack lab and reports what really happens | No |
| **Manager** | No content: it reports progress to the owner, passes on the owner's decisions and hands tasks to the other agents | No | Only changes the owner has validated |

No agent reviews or merges a pull request it wrote: the `Author:` line of each agent-authored pull request names the
agent and says it is an AI agent (for example `Author: OzarLand author agent (AI agent)`).

**The author of a pull request carries it to the merge.** The agent that opened a pull request fixes what its
reviews ask and resolves its merge conflicts, without waiting to be asked. Where it can, it subscribes to its pull
request's activity so that a review wakes it.

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

The agents' detailed working instructions are in [`.claude/agents/`](../.claude/agents/), one file per agent.

## Tools the agents share

- [`tools/check_content.py`](../tools/check_content.py): conventions checker, runnable by anyone before opening a pull request.
- [`tools/status_blocks.py`](../tools/status_blocks.py): regenerates the page-status badges, progress bars and counts in the READMEs of `ozarland` and the content repositories, and in [knowledge lifecycle](knowledge-lifecycle.md); without `--write` it reports stale blocks.
- [`tools/coverage_report.py`](../tools/coverage_report.py) with [`docs/topics.yml`](topics.yml): which topics each repository covers, and which are missing.
