# Review and merge policy

How pull requests on the OzarLand community repositories are reviewed and merged, including by the automated
operator reviewer. The aim is to keep contributions flowing without letting an unsafe procedure reach a reader.

## Who reviews

| Reviewer | What they do |
|---|---|
| **Any contributor** | Reviews, confirms pages in their environment, suggests changes. Anyone can review. |
| **Operator reviewer** (automated) | Runs every 4 hours on open pull requests, and on request from the manager session or an author session. Reviews each one as an experienced OpenStack operator would, runs the content checker, and squash-merges the pull requests that pass its review without reservation and touch nothing the owner validates. Its definition is [`.claude/agents/openstack-operator-reviewer.md`](../.claude/agents/openstack-operator-reviewer.md). |
| **Lab reviewer** (agent on a lab platform) | Runs the steps of a page on a lab OpenStack platform: read-only steps on any lab, state-changing and destructive steps only on a lab declared disposable. Reports in a review what it ran, on which release and deployment method, and what differed. Its findings are reviews like any other; a successful run can become a `type: lab` confirmation and move a page to `lab-verified`. |
| **Maintainers** | Handle everything the automated reviewer escalates and any pull request labelled `hold`. The owner validates the risky changes listed under [What only the owner validates](#what-only-the-owner-validates). Can override any automated decision. |

The manager agent checks every hour for pull requests waiting on a review and wakes the operator reviewer when
needed, so a pull request rarely waits for the next scheduled run.

Reviews by the automated reviewer start with **Operator review:**, reviews by a lab agent with **Lab review:**; both
are clearly identified as automated. Agents are reviewers in their own right: their findings block a merge exactly
like a human reviewer's, and an author (human or agent) answers them by pushing fixes or by explaining why not.

## Agents as authors

Agents can also write pages ([author definition](../.claude/agents/ozarland-author.md)). An agent-authored pull
request follows the same rules as any other. New pages are `draft`: an author never confirms its own work, and a lab
confirmation is recorded by a lab reviewer in a separate pull request. It says in its description where the content
comes from (a contributor's incident, a book, upstream documentation, a lab run). Content not observed on a real
platform stays `draft` until a lab run or an operator confirms it.

**Identification and disclosure.** AI use is disclosed openly. At repository level,
[how OzarLand is built](how-ozarland-is-built.md) says what the agents do, the safeguards and the limits. In each
agent-authored pull request, the description carries one `Author:` line that names the agent and says it is an AI
agent, for example `Author: OzarLand author agent (AI agent)` or `Author: OzarLand lab reviewer agent (AI agent)`.
Commit messages stay plain descriptions of the change. A reviewer reads the `Author:` line and never reviews or merges
a pull request it wrote: neither the operator reviewer nor the lab reviewer reviews a pull request that names it as
author.

**Sign-off (DCO).** Agents sign off their commits in the owner's name, with the owner's git configuration. The owner
provides the material the agents write from and takes responsibility for the contribution under the
[Developer Certificate of Origin](https://developercertificate.org/), exactly as for a commit they wrote by hand.

## What agents merge

The owner's rule: **agents merge every pull request that passes review without reservation, in all three
repositories** (`ozarland`, `openstack-vm-runbooks`, `kolla-ansible-deployment-patterns`). A session never merges
its own work, and never merges a pull request whose description names it as author.

A review passes without reservation when all of the following hold:

1. The [content checker](../tools/check_content.py) reports no error on the changed files: front matter, required
   sections, risk markers consistent with the declared risk, no address or secret outside the documentation
   ranges, relative links resolve.
2. Every command is correct for the tool it names, run where the page says, and every state-changing or
   destructive step carries its [risk warning](conventions/risk-warnings.md).
3. Claims are true for the releases stated, and the page states its validity and limits honestly. An upgrade path
   is never presented as officially supported without an upstream link.
4. Nothing sensitive: see [sensitive data](conventions/sensitive-data.md).
5. The page is neutral about tools and approaches.
6. New pages are `draft` or `experimental`. A page becomes `lab-verified` through a `type: lab` confirmation that
   says what was run, and `validated` only through a `type: operator` confirmation by someone other than its author.
7. The pull request is mergeable, its checks pass, and no reviewer (human or agent) has a blocking finding or an
   unresolved change request.

This covers content pages, READMEs, `tools/`, `community/`, templates, `CONTRIBUTING.md` and the documentation in
`docs/`, except the files listed below.

## What only the owner validates

Risky decisions are reviewed like anything else, but merged only after the owner validates them:

- Changes to the rules and agent roles: `docs/review-policy.md`, `docs/governance.md`, `docs/agents.md`, and
  anything under `.claude/`.
- `tools/check_content.py`, the checker that gates every merge.
- `LICENSE`, `SECURITY.md`, `CODE_OF_CONDUCT.md`.
- Deleting a page.
- Making a repository public, and GitHub settings (including anything under `.github/`).
- Any pull request labelled `hold`.
- Anything a reviewer is not confident about: it labels the pull request `needs-maintainer` and says why.

## Labels

| Label | Meaning |
|---|---|
| `hold` | A maintainer handles this pull request personally. The automated reviewer skips it. |
| `needs-changes` | The automated reviewer found blocking issues, listed in its review. Push fixes; it will review again. |
| `needs-maintainer` | A change only the owner validates, or content the automated reviewer could not judge with confidence. |
| `needs-lab` | The reviewer wants the steps run on a lab before merging (for example a destructive procedure with no observed run). |
| `status/lab-verified` | The pull request records a lab run of a page. |

Applying a label that does not exist yet creates it.

## Merging

Pull requests are squash-merged. The commit title is the pull request title with its number; the message is a
short summary followed by the contributors' `Signed-off-by` lines (DCO).

## Disagreeing with a decision

Comment on the pull request. A maintainer will look at it. An automated "changes requested" is a request, not a
verdict: if you think the reviewer is wrong, say why, with the upstream reference if you have one.
