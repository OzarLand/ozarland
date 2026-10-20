# Review and merge policy

How pull requests on the OzarLand community repositories are reviewed and merged, including by the automated
operator reviewer. The aim is to keep contributions flowing without letting an unsafe procedure reach a reader.

## Who reviews

| Reviewer | What they do |
|---|---|
| **Any contributor** | Reviews, confirms pages in their environment, suggests changes. Anyone can review. |
| **Operator reviewer** (automated) | Runs a few times a day on open pull requests. Reviews each one as an experienced OpenStack operator would, runs the content checker, and squash-merges the pull requests that are clear, safe and within this policy. Its definition is [`.claude/agents/openstack-operator-reviewer.md`](../.claude/agents/openstack-operator-reviewer.md). |
| **Maintainers** | Handle everything the automated reviewer escalates, all structural changes, and any pull request labelled `hold`. Can override any automated decision. |

Reviews by the automated reviewer start with **Operator review:** and are clearly identified as automated.

## What can be merged automatically

Only **content** pull requests in `openstack-vm-runbooks` and `kolla-ansible-deployment-patterns`: new or
improved community pages, the index table of the README, and confirmations added to a page. All of the
following must hold:

1. The [content checker](../tools/check_content.py) reports no error on the changed files: front matter, required
   sections, risk markers consistent with the declared risk, no address or secret outside the documentation
   ranges, relative links resolve.
2. Every command is correct for the tool it names, run where the page says, and every state-changing or
   destructive step carries its [risk warning](conventions/risk-warnings.md).
3. Claims are true for the releases stated, and the page states its validity and limits honestly. An upgrade path
   is never presented as officially supported without an upstream link.
4. Nothing sensitive: see [sensitive data](conventions/sensitive-data.md).
5. The page is neutral about tools and approaches.
6. New pages are `draft` or `experimental`. A page becomes `validated` only through a confirmation by someone other
   than its author.
7. The pull request is mergeable, its checks pass, and no human reviewer has an unresolved change request.

## What is never merged automatically

- Anything in `ozarland`.
- Any change to `.github/`, `.claude/`, `tools/`, templates, `LICENSE`, `SECURITY.md`, `CODE_OF_CONDUCT.md`,
  `CONTRIBUTING.md`, or a README outside its index table.
- Any pull request labelled `hold`.
- Anything the reviewer is not confident about: it labels the pull request `needs-maintainer` and says why.

## Labels

| Label | Meaning |
|---|---|
| `hold` | A maintainer handles this pull request personally. The automated reviewer skips it. |
| `needs-changes` | The automated reviewer found blocking issues, listed in its review. Push fixes; it will review again. |
| `needs-maintainer` | Structural change, or content the automated reviewer could not judge with confidence. |

## Merging

Pull requests are squash-merged. The commit title is the pull request title with its number; the message is a
short summary followed by the contributors' `Signed-off-by` lines (DCO).

## Disagreeing with a decision

Comment on the pull request. A maintainer will look at it. An automated "changes requested" is a request, not a
verdict: if you think the reviewer is wrong, say why, with the upstream reference if you have one.
