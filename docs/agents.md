# Agents

OzarLand uses a few AI agents to keep the community repositories moving. They follow the same rules as human
contributors ([review and merge policy](review-policy.md)) and are always identified as AI agents. What they do,
what keeps them in check and what they made possible: [how OzarLand is built](how-ozarland-is-built.md).

| Agent | Role | Definition |
|---|---|---|
| **Operator reviewer** | Reviews open pull requests as a senior OpenStack operator, runs the content checker, merges clear and safe content pull requests, escalates the rest. Runs every 4 hours, and on request from the manager session or an author session. | [`openstack-operator-reviewer`](../.claude/agents/openstack-operator-reviewer.md) |
| **Lab reviewer** | Runs the steps of pages on a lab OpenStack platform and reports what really happens; records lab confirmations. | [`openstack-lab-reviewer`](../.claude/agents/openstack-lab-reviewer.md) |
| **Manager** | Talks with the owner and gives a simplified view of progress: topics covered per repository, pull requests in progress, decisions needed. Checks every hour, and wakes the operator reviewer when pull requests are waiting. | [`ozarland-manager`](../.claude/agents/ozarland-manager.md) |
| **Author** | Writes pages from material the owner provides (incidents, a book, lab runs) and opens pull requests; never confirms its own pages. Its pull requests are reviewed like anyone else's. | [`ozarland-author`](../.claude/agents/ozarland-author.md) |
| **Documentation** | Writes and clarifies the community pages of `ozarland` (newcomer path, conventions, plans) and opens pull requests; never reviews or merges. | Started by the manager session with its task; no separate definition file |

## How runs are triggered

- The **operator reviewer** runs on its schedule every 4 hours, and on request: the manager session or an author
  session asks it by a message to the reviewer's session. Pull requests are never reviewed by starting new sessions
  or scheduled runs on the fly.
- The **manager** checks every hour: open pull requests, reviews, what each agent is doing.
- The **lab reviewer** runs when it is asked to check a page or a pull request.

## The owner's standing decisions

Every agent keeps these; only the owner changes them. They are spelled out in the
[author definition](../.claude/agents/ozarland-author.md): content in English only; `ozarland` is the newcomers'
entry point and links out to the content repositories; new pages are `draft` and never confirmed by their author;
no agent uses `fire_trigger`; `ozarMVP` and `OzarBuild` are out of scope; AI use is disclosed openly, at repository
level ([how OzarLand is built](how-ozarland-is-built.md)) and in each agent-authored pull request, whose `Author:`
line names the agent and says it is an AI agent (for example `Author: OzarLand author agent (AI agent)`), so that
readers know and no agent reviews its own; commit messages stay plain; commits signed off in the owner's name, who takes responsibility for them (DCO);
agents merge every pull request that passes review without reservation, in all three repositories, never their
own; the owner validates only risky decisions (rules and agent roles, `LICENSE`, `SECURITY.md`,
`CODE_OF_CONDUCT.md`, page deletions, making a repository public, GitHub settings), as listed in the
[review and merge policy](review-policy.md).

## Tools the agents share

- [`tools/check_content.py`](../tools/check_content.py): conventions checker, runnable by anyone before opening a pull request.
- [`tools/coverage_report.py`](../tools/coverage_report.py) with [`docs/topics.yml`](topics.yml): which topics each repository covers, and which are missing.
