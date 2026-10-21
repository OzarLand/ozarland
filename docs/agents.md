# Agents

OzarLand uses a few AI agents to keep the community repositories moving. They follow the same rules as human
contributors ([review and merge policy](review-policy.md)) and are always identified as automated.

| Agent | Role | Definition |
|---|---|---|
| **Operator reviewer** | Reviews open pull requests as a senior OpenStack operator, runs the content checker, merges clear and safe content pull requests, escalates the rest. Runs every 4 hours. | [`openstack-operator-reviewer`](../.claude/agents/openstack-operator-reviewer.md) |
| **Lab reviewer** | Runs the steps of pages on a lab OpenStack platform and reports what really happens; records lab confirmations. | [`openstack-lab-reviewer`](../.claude/agents/openstack-lab-reviewer.md) |
| **Manager** | Talks with the owner and gives a simplified view of progress: topics covered per repository, pull requests in progress, decisions needed. | [`ozarland-manager`](../.claude/agents/ozarland-manager.md) |
| **Authors** | Agents that write pages from material the owner provides (incidents, a book, lab runs). Their pull requests are reviewed like anyone else's. | No fixed definition |

## Tools the agents share

- [`tools/check_content.py`](../tools/check_content.py): conventions checker, runnable by anyone before opening a pull request.
- [`tools/coverage_report.py`](../tools/coverage_report.py) with [`docs/topics.yml`](topics.yml): which topics each repository covers, and which are missing.
