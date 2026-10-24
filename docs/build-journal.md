# Building OzarLand with AI agents: the journal

One entry per day: what was built, by which agents, and what review and the lab caught. Numbers are counted from the
git history and the pull requests of the four repositories (`ozarland`, `openstack-vm-runbooks`,
`kolla-ansible-deployment-patterns`, `openstack-quick-lab`). Days are UTC dates. The roles and safeguards are
described in [When AI meets OpenStack](how-ozarland-is-built.md).

The journal gets one entry a day. The last row of the summary can be a day still in progress: its entry says until
when it was counted, and the next update completes it.

How each number is counted:

| Metric | Counted as |
|---|---|
| Pages published | Pages with front matter on `main` of the two content repositories at the end of the day |
| Lab-verified | Of those, pages with `status: lab-verified` |
| Pull requests merged | Merged that day, all four repositories |
| Operator reviews | Reviews and comments starting with **Operator review** posted that day |
| Blocking findings | Bullet points under **Blocking** in those reviews |
| Lab runs | Lab reports (starting with **Lab review**) posted that day; one report covers one page on one lab |
| Lab findings | Steps those reports mark as **Failed** or **Needed a change** when run as written |

## Summary

| Day | Pages published | Lab-verified | Pull requests merged | Operator reviews | Blocking findings | Lab runs | Lab findings |
|---|---|---|---|---|---|---|---|
| 18 Oct | 0 | 0 | 3 | 0 | 0 | 0 | 0 |
| 19 Oct | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 20 Oct | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| 21 Oct | 25 | 0 | 18 | 24 | 13 | 0 | 0 |
| 22 Oct | 33 | 6 | 15 | 17 | 4 | 14 | 6 |
| 23 Oct | 33 | 12 | 23 | 44 | 17 | 20 | 4 |
| 24 Oct | 35 | 15 | 26 | 26 | 21 | 5 | 6 |

## 18 October: the repositioning

OzarLand had been, since 4 October, an operator toolkit project. On 18 October it became a knowledge-sharing space
([ADR-0008](adr/0008-community-knowledge-sharing-space.md)). Three pull requests in `ozarland`: the repositioning,
ten seed runbooks written from the incidents of the owner's book *OpenStack, the Day After Tomorrow* (as a blueprint
in `ozarland`), and the two content repositories created and marked active. No agent definition existed yet; these
pull requests carry no `Author:` line.

## 19 October

No merge.

## 20 October: the first reviewer agent

The operator reviewer agent and the [review and merge policy](review-policy.md) were added to `ozarland`. From then
on, every pull request has an independent review.

## 21 October: the first pages, and the first reviews

- **Built:** 25 pages published in one day. In `openstack-vm-runbooks`: eleven runbooks from the book, eleven
  runbooks from failures reproduced on lab builds. In `kolla-ansible-deployment-patterns`: the first pattern, a
  deployment error from a real lab build, and a configuration-layout pattern. In `ozarland`: the newcomer space, the
  manager agent, agents as reviewers, the owner's standing rules, contact channels.
- **Agents:** the author agent wrote the content pages (7 pull requests with its `Author:` line); the operator reviewer
  reviewed them; the manager agent started reporting to the owner.
- **Review caught:** 24 operator reviews, 6 of them requesting changes, with 13 blocking findings. For example,
  pages that went beyond what had been observed, and policy points the owner had to decide.

## 22 October: the lab starts running the pages

- **Built:** 8 more pages (33 in all): two volume runbooks, a runbook on instances unreachable from outside, and five
  deployment pages (all-in-one lab topology, networking, storage, version notes from 2025.1 to 2026.1, and an
  upgrade report).
- **Agents:** the author agent (7 pull requests) and the lab reviewer agent (8). The lab reviewer ran pages on a
  disposable all-in-one OpenStack 2026.1 lab (Kolla-Ansible 22.2.0), and in the evening ran a full upgrade of a lab
  from 2025.1 to 2026.1.
- **The lab caught:** 14 lab runs, 6 steps that failed or needed a change. For example, a health check
  (`ovs-appctl` run in the wrong container) that reported a healthy switch as down; `ovs-vsctl` not found on the host
  of a containerised deployment; Nova logs not in `docker logs`. Each finding went back to the author agent, which
  applied the follow-ups in new pull requests (for example `openstack-vm-runbooks#17` and `#21`).
- **Result:** the first 6 pages became `lab-verified`, each through a separate confirmation pull request by the lab
  reviewer.
- **Review:** 17 operator reviews, 2 requesting changes, 4 blocking findings.

## 23 October: a multinode lab, a quick lab, and the community pages

- **Built:** 6 more runbooks confirmed on the lab (12 `lab-verified` in all). The new
  [openstack-quick-lab](https://github.com/OzarLand/openstack-quick-lab) repository, with an OpenStack cloud variant
  (create, deploy and destroy scripts, 57 minutes end to end on its measured run) and six exercises that use the
  runbooks. In `ozarland`, 11 pull requests from the documentation agent: how to start a discussion, current
  statuses, the newcomer reading path and glossary, a shorter README, and an open account of the agents' work
  ([When AI meets OpenStack](how-ozarland-is-built.md)).
- **Agents:** author (4), lab reviewer (8), documentation (11 merged). The lab reviewer moved to a multinode lab
  (one controller, two computes) for the pages that need more than one host: migration, CPU pinning, fencing,
  routers, MTU, a full disk.
- **The lab caught:** 20 lab runs, 4 steps that failed or needed a change, among them `port list` columns that do not
  exist and a `docker stop` that the platform undoes within a minute (fixed in `openstack-vm-runbooks#32`).
- **Review caught:** 44 operator reviews, 9 requesting changes, 17 blocking findings, among them a decision record
  whose disclosure the reviewer asked to restore before merge, and a pull request that had to wait for the owner.

## 24 October: production feedback, a comparison page, and five more lab runs

Counted at 21:30 UTC.

- **Built:** 26 pull requests merged. In the content repositories: a runbook on instances that stay `SHUTOFF` or lose
  their network after a compute reboot, the first comparison page in `kolla-ansible-deployment-patterns` (ML2/OVS
  versus ML2/OVN with Kolla-Ansible), the 2025.1 to 2026.1 version notes rewritten as an upgrade playbook with a
  go / no-go checklist, provenance on every page, and READMEs that start from what the reader sees. In
  `openstack-quick-lab`: the scripts refuse to start without a cost estimate. In `ozarland`: one status table,
  provenance in the templates, who is behind OzarLand, the build journal, and the Felcloud wording, recorded as
  [ADR-0010](adr/0010-felcloud-wording.md).
- **The owner's production report:** the owner reported that the behaviour of three runbooks (restarting
  `nova_libvirt`, `nova-compute` down with instances running, restarting the Open vSwitch agent) matches what they
  observed in production on an earlier Kolla-Ansible release. It is recorded on each page as an operator entry. After
  the operator review, the three pages stay `lab-verified`: the steps were not re-run, and the exact release is not
  recorded.
- **Agents:** author (11), documentation (11), lab reviewer (4).
- **The lab:** 5 lab runs, on 5 runbooks; 6 steps failed or needed a change. Three confirmations were merged (15
  runbooks `lab-verified` in all), one is in review, and one page stays `draft` with fixes in review. The most useful
  finding: `openstack volume attachment list --volume-id` in python-openstackclient 9.0.0 ignores the filter and
  lists every attachment of the cloud. A quick check built on it would have shown an operator the wrong volumes.
  The volume-stuck runbook now uses `cinder attachment-list --volume-id`, which filters correctly. The same fix for
  the stale-attachment runbook is in review; the stale-records runbook still uses the command, and is next.
- **Review:** 26 operator reviews, 10 requesting changes, 21 blocking findings, among them the reasons why the
  production report does not make the pages `validated`.
- **Owner decisions:** in the same pull request as its lab confirmation, a lab reviewer may correct a page with what
  its run observed, once an independent operator review has checked the corrections; and README index rows for a
  page are ordinary content. Both are being recorded in the [review policy](review-policy.md).
