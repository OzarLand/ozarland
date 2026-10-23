# GitHub conventions

How OzarLand uses GitHub. These conventions apply to every community repository.

## Where things happen

| Need | Where | Why |
|---|---|---|
| Ask for help, compare observations, share an experience report, discuss an architecture choice | **GitHub Discussions** (categories below) | Threaded, open-ended, no "done" state to manage |
| Report that a page is wrong, missing or unsafe; propose a new page; track a problem until it becomes a runbook | **Issues** (templates below) | Has a clear done state and can be linked to a pull request |
| Add or change content | **Pull requests** | Reviewable, attributable, versioned |
| The content itself | **Markdown files in the repository** | Readable on GitHub, diffable, forkable |

Discussions should be enabled on every community repository. In the first phase, discussions are centralised in
`ozarland` so that the community has one visible place to meet; see [knowledge lifecycle](knowledge-lifecycle.md).

### Discussion categories

| Category | Type | Purpose |
|---|---|---|
| **Q&A** | Question / answer | "How do I…", "Has anyone seen…". An accepted answer can be turned into a runbook. |
| **Experience reports** | Open discussion | Upgrades, incidents, migrations, architecture choices told first-hand |
| **Show and compare** | Open discussion | "Here is how we do X, how do you do it?" |
| **Ideas** | Open discussion | Proposals about the community itself: structure, templates, new repositories |
| **Announcements** | Announcement | Maintainer updates |

Discussion category forms for Q&A, Experience reports and Show and compare live in this repository's
`.github/DISCUSSION_TEMPLATE/`, with a copy for new repositories under `community/repo-template/.github/DISCUSSION_TEMPLATE/`.
A form file is named after its category slug (`q-a.yml`, `experience-reports.yml`, `show-and-compare.yml`).
For readers, [Start a discussion](../newcomers/start-a-discussion.md) explains how to use the categories.

### Issue templates

| Template | Purpose | Default labels |
|---|---|---|
| Question | A specific operational question that needs a tracked answer | `kind/question`, `status/needs-info` or `status/open` |
| Problem solved | A problem you fixed that could become a runbook | `kind/problem-solved`, `status/candidate` |
| Documentation proposal | A new page, or a correction to an existing one | `kind/docs`, `status/open` |
| Experience report | Offer an experience report to be written up | `kind/experience`, `status/open` |

Templates live under `community/repo-template/.github/ISSUE_TEMPLATE/` and are copied into each repository.

## Labels

Labels are shared across repositories so that cross-repository searches work.

| Group | Labels | Meaning |
|---|---|---|
| Kind | `kind/question`, `kind/problem-solved`, `kind/docs`, `kind/experience`, `kind/community` | What the item is |
| Status | `status/open`, `status/needs-info`, `status/candidate`, `status/in-review`, `status/validated`, `status/stale` | Where it is in the [knowledge lifecycle](knowledge-lifecycle.md) |
| Component | `component/nova`, `component/neutron`, `component/cinder`, `component/glance`, `component/keystone`, `component/placement`, `component/octavia`, `component/ceph`, `component/mariadb`, `component/rabbitmq`, `component/haproxy`, `component/other` | OpenStack or infrastructure component involved |
| Deployment | `deploy/kolla-ansible`, `deploy/openstack-ansible`, `deploy/charmed`, `deploy/vendor`, `deploy/other`, `deploy/any` | Deployment method the content applies to |
| Risk | `risk/destructive`, `risk/production-impact` | Content contains commands that need explicit warnings |
| Review | `hold`, `needs-changes`, `needs-maintainer` | See the [review and merge policy](review-policy.md) |
| Other | `good first contribution`, `help wanted`, `security`, `upstream` | Onboarding, calls for help, security review needed, upstream bug involved |

Release-specific items use a milestone or the release name in the title (for example `[2025.1]`) rather than a label
per release, to keep the label set small.

## Branches, commits, pull requests

- `main` is the published state. Work happens on short-lived branches named after what they change
  (`runbook/nova-instance-stuck-deleting`, `pattern/three-controller-ovn`, `fix/typo-cinder-attach`).
- Commit messages are plain descriptive sentences. [Conventional Commits](https://www.conventionalcommits.org/)
  prefixes (`docs:`, `fix:`, `chore:`) are welcome but not required.
- Every commit carries a Developer Certificate of Origin sign-off (`git commit -s`). Web commits are signed off
  automatically by organization policy. This is the only legal formality; there is no contributor agreement.
- Pull requests are squash-merged. One page, pattern or runbook per pull request keeps review easy.
- A pull request is merged by a maintainer or by an agent once it passes review without reservation, following the
  [review and merge policy](review-policy.md); the risky changes listed there are validated by the owner. A contribution that reports "I confirmed this in my
  environment" on an existing page is merged quickly: it is how content gets validated.

## Organization settings to apply

Settings that cannot be changed from a repository and need an organization owner:

| Setting | Target value |
|---|---|
| Organization description | See [launch plan](launch-plan.md), section "GitHub metadata" |
| Repository description and topics | Per repository, see the launch plan |
| Discussions | Enabled on `ozarland` first, then on each community repository |
| Default labels | The taxonomy above, applied organization-wide |
| Visibility | Public, once the go-public checklist in [governance](governance.md) is complete |
| Member repository creation | Owners only, to avoid repository sprawl; repositories are created from a decision record |
| Commit sign-off on web commits | Required (already set) |
| Two-factor authentication | Required for members |
