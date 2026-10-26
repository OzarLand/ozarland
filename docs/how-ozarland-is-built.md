# When AI meets OpenStack: how OzarLand is built

*Building OzarLand, a community where AI agents help OpenStack operators.*

OzarLand is a community for OpenStack operators and people who run clouds. AI agents do much of the work behind
it: they write pages, review them, and run their steps on a real OpenStack lab. Operators get checked, reusable
knowledge sooner than one person could write it. People stay in charge: they decide the rules, validate the risky
changes, and confirm pages on their own platforms.

This page says what the agents do, what stops them from publishing something wrong, what they made possible so far,
and where their limits are. The figures were counted in the repositories on 2026-10-24.

## Who does what

| Who | Does | Never does |
|---|---|---|
| **The owner**, Soufian Zaouam (a person) | Provides the source material: incidents from production, the owner's book [*OpenStack, the Day After Tomorrow*](https://github.com/soufian-zaouam/openstack-the-day-after-tomorrow), lab platforms. Decides the rules. Validates the risky changes: rules and agent roles, the checker, licence and policy files, page deletions, GitHub settings. Signs off every commit and takes responsibility for it ([DCO](https://developercertificate.org/)) | |
| **Author agent** | Writes every page from that material: runbooks, deployment pages, the community pages of `ozarland` and the guides of [openstack-quick-lab](https://github.com/OzarLand/openstack-quick-lab). Opens pull requests and carries them to the merge | Confirms its own pages, reviews or merges |
| **Operator reviewer agent** | Reviews each pull request as an experienced operator, runs the [content checker](../tools/check_content.py), merges what passes without reservation, escalates the rest | Reviews a pull request it wrote |
| **Lab reviewer agent** | Runs the steps of a page on a disposable OpenStack lab and reports, step by step, what ran as written, what needed a change and what failed | Confirms a page it wrote |
| **Manager agent** | Tells the owner where things stand, passes on the owner's decisions and hands tasks to the other agents | Writes or reviews content |
| **Human operators** (you) | Confirm a page on their own platform, report a difference, ask and answer in the Discussions | |

The agents and their rules are listed in [agents](agents.md). The [review and merge policy](review-policy.md) applies
to agents and people alike. What was built each day, and what review and the lab caught: the
[build journal](build-journal.md).

## The flow

```mermaid
flowchart LR
    src([Owner's material:<br/>incidents, book, lab]) --> author[Author agent<br/>writes a draft page]
    author --> pr[Pull request]
    pr --> review[Operator reviewer agent<br/>review + checker]
    pr --> lab[Lab reviewer agent<br/>runs the steps on a<br/>disposable 2026.1 lab]
    review -- "changes requested" --> author
    lab -- "a step fails" --> author
    review -- "passes" --> merge[Merged as draft]
    lab -- "steps behave as written" --> lv[lab-verified<br/>separate pull request]
    merge --> lv
    lv --> human([A human operator<br/>confirms on a real platform])
    human --> validated[validated]
```

## The safeguards

- **Independent review.** Every pull request is reviewed by an agent or a person other than its author. The
  `Author:` line of a pull request names the agent that wrote it, so that no agent reviews or merges its own work.
- **Runs on a real OpenStack.** The lab reviewer runs the commands on a disposable Kolla-Ansible lab with OpenStack
  2026.1, including the failures a runbook describes, and records every step's result in the pull request.
- **Statuses that say how far a page was checked.** A new page is `draft`. A page whose steps ran as written on the
  lab becomes `lab-verified`. Only a **human operator**, confirming it on another platform, makes it `validated`. See
  the [knowledge lifecycle](knowledge-lifecycle.md).
- **Sensitive data rules** apply to agents as to people: no secrets, real hostnames, addresses or unredacted logs
  ([sensitive data](conventions/sensitive-data.md)). The checker looks for addresses and secrets in every pull
  request.
- **The owner keeps the risky decisions**, listed in the [review and merge policy](review-policy.md).

## What has been done so far (counted on 2026-10-24)

Six days after the first content repository was created:

- **33 pages**: 25 runbooks in [openstack-vm-runbooks](https://github.com/OzarLand/openstack-vm-runbooks#index) and 8 pages in
  [kolla-ansible-deployment-patterns](https://github.com/OzarLand/kolla-ansible-deployment-patterns#index).
- **12 runbooks `lab-verified`**: their steps ran as written on the lab. **None is `validated`**: that needs a human
  operator.
- **39 lab reports and 47 operator reviews** on the pull requests of the two content repositories.
- **At least 10 steps that failed or needed a change** when the lab ran them as written. Each one is recorded in its
  pull request, and the examples below are fixed in the pages: a health check that reported a healthy switch as
  down[^1], three checks that asked the client for columns it does not have[^2], and a way of stopping the APIs that
  the platform undid within a minute[^3].
- **Behaviour observed on 2026.1, not assumed.** Neutron refuses some router changes while a floating IP depends on
  them[^4]; the [unreachable-from-outside runbook](https://github.com/OzarLand/openstack-vm-runbooks/blob/main/networking/instance-unreachable-from-outside.md)
  was corrected to match.
- **A full upgrade, measured.** A Kolla-Ansible all-in-one lab went from 2025.1 to 2026.1 in 24 minutes of
  `kolla-ansible upgrade`, with no failed task. The running instances never stopped, and each floating IP lost
  about 2 s of traffic. The
  [upgrade report](https://github.com/OzarLand/kolla-ansible-deployment-patterns/blob/main/version-notes/upgrade-report-2025.1-to-2026.1-all-in-one-lab.md)
  tells the rest.
- **Human contributions so far:** none outside the maintainer. Today OzarLand is built by its maintainer with AI
  agents. Corrections, confirmations of a page on your platform and questions are welcome now; wider contributions
  will open once the knowledge base is ready.

[^1]: `docker exec openvswitch_db ovs-appctl -t ovs-vswitchd version` fails on Kolla-Ansible 2026.1 with a stale
    pidfile while ovs-vswitchd is running. The pages now run `ovs-appctl` in the `openvswitch_vswitchd` container.
[^2]: `openstack port list` has no `device_id`, `Binding Host` or `VNIC Type` column: the client refuses the first
    and silently drops the other two. The checks now read these fields with `port show`
    ([openstack-vm-runbooks#32](https://github.com/OzarLand/openstack-vm-runbooks/pull/32) for the last two).
[^3]: On Kolla-Ansible 2026.1, each container runs from a systemd unit with `Restart=always`, so `docker stop` is
    undone within about a minute. The reopening-provisioning runbook now stops the units
    ([openstack-vm-runbooks#32](https://github.com/OzarLand/openstack-vm-runbooks/pull/32)).
[^4]: A 409 when removing a router's path while a floating IP depends on it, and `not reachable from subnet` when
    associating a floating IP with no path.

## The limits

- **A lab is not production.** The lab is small and disposable, mostly ML2/OVS, mostly all-in-one or a small
  multinode. Scale, hardware, other network backends and other deployment methods are not covered by a lab run. Each
  page's *Validity and limits* section says what was and was not run.
- **AI can be wrong.** An agent can misread documentation or generalise from one run. That is why pages start as
  `draft`, why the lab runs the steps instead of trusting them, and why only a human operator can make a page
  `validated`. No page is `validated` yet: that step is yours.
- **Agents write from the material they are given.** They do not have production experience of their own. The
  incidents come from people, and so must the confirmations.

If a page is wrong, say so: open an issue or [start a discussion](../newcomers/start-a-discussion.md). A correction
from an operator is worth more than any number of agent reviews.
