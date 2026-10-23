# Start a discussion

How to ask a question, share what happened on your platform or compare approaches with other operators. Everything
happens in the [OzarLand Discussions](https://github.com/OzarLand/ozarland/discussions), in this repository, whatever
the topic: VM runbooks, deployment, upgrades or the community itself. You need a GitHub account, nothing else.

## Discussion, issue or pull request?

| You want to… | Use | Why |
|---|---|---|
| Ask "how do I…", "has anyone seen…", compare observations, tell what happened | **Discussion** | Open-ended: there is nothing to fix yet, and several answers can be right |
| Report that a page is wrong, missing or unsafe; offer a problem you solved so it becomes a page | **Issue** in the repository of the page | It has a "done" state and is closed by a pull request |
| Add or change a page yourself | **Pull request** | Reviewable and attributable; see [your first contribution](first-contribution.md) |

Not sure? Start a discussion. Someone will move it to the right place if needed.

## The five categories

| Category | For | Example title |
|---|---|---|
| **Q&A** | A question that has an answer; the best reply can be marked as the answer | *Instance stuck in BUILD on 2025.1 with OVN, no error in nova-compute: where next?* |
| **Experience reports** | Something that happened, told first-hand: an upgrade, an incident, a migration, a choice | *Upgrading 2025.1 to 2026.1 with Kolla-Ansible on three controllers: what broke and what we would redo* |
| **Show and compare** | "Here is how we do X. How do you do it?" | *How do you drain a compute before patching: live migration by script, or host aggregates?* |
| **Ideas** | Proposals about OzarLand itself: a page that is missing, a template, a new repository | *A runbook section for OpenStack-Ansible variants?* |
| **Announcements** | News from the maintainers; only they can post, everyone can reply | *Welcome: how to use OzarLand Discussions* |

## Open one, step by step

1. **Search first.** Look in the [runbooks index](https://github.com/OzarLand/openstack-vm-runbooks#index), the
   [deployment patterns index](https://github.com/OzarLand/kolla-ansible-deployment-patterns#index) and the
   [existing discussions](https://github.com/OzarLand/ozarland/discussions). If a discussion already covers your
   topic, reply there instead of opening a new one.
2. **Pick the category** and open the form directly:
   - [New Q&A question](https://github.com/OzarLand/ozarland/discussions/new?category=q-a)
   - [New experience report](https://github.com/OzarLand/ozarland/discussions/new?category=experience-reports)
   - [New show and compare](https://github.com/OzarLand/ozarland/discussions/new?category=show-and-compare)
   - [New idea](https://github.com/OzarLand/ozarland/discussions/new?category=ideas)
3. **Write a title that names the symptom or the topic**, with the release and the component when they matter. A
   reader scanning the list should know whether it is their problem.
4. **Fill in the form.** Q&A, Experience reports and Show and compare open with a short form whose fields are the
   context below; Ideas is free text.
5. **Re-read for sensitive data** (next section), then select **Start discussion**.
6. **Follow up.** Answer the questions people ask you. When a reply solves a Q&A question, select **Mark as answer**
   on it, and say what you did in one line: that is what the next reader looks for.

## What to include

- the **OpenStack release** (`2025.1`, `2026.1`…);
- the **deployment method** (Kolla-Ansible, OpenStack-Ansible, a distribution, by hand) and what matters in your
  environment: number of controllers, network backend (ML2/OVS, ML2/OVN), storage backend, OS;
- **what you see**: the exact error message, the instance or service state, when it started;
- **what you already checked**, with the commands, and what they returned (redacted);
- **links to the pages you already read**, and where they stopped matching what you see.

Short is fine. "I don't understand why…" is a good question too.

## What never to post

Discussions are public and indexed by search engines. Never post:

- secrets of any kind: passwords, tokens, keys, `passwords.yml`, keyrings, even "test" ones;
- real hostnames, domains, IP or MAC addresses;
- customer, employer, project or person names;
- logs or command output you have not redacted.

Replace them with placeholders (`controller-1`, `<server-id>`, `192.0.2.10`); the
[sensitive data rules](../docs/conventions/sensitive-data.md) show how. If you posted something by mistake, edit it
out at once and follow [SECURITY.md](../SECURITY.md): an edited post keeps its history, so secrets must also be
rotated.

## How a good answer becomes a runbook

An answer that stays in a thread is knowledge the next operator will not find. When a discussion solved something:

1. The author marks the answer and confirms, in one line, what fixed it and on which release.
2. Someone, often the author, opens a *Problem solved* issue in the repository where the page belongs
   ([VM runbooks](https://github.com/OzarLand/openstack-vm-runbooks/issues/new/choose) or
   [deployment patterns](https://github.com/OzarLand/kolla-ansible-deployment-patterns/issues/new/choose)) and links
   the discussion.
3. A contributor writes the page from it with the [runbook template](../community/templates/runbook.md) and opens a
   pull request. The page starts as `draft`; confirmations from other operators move it to `validated`.

Experience reports and comparisons follow the same path towards experience-report or pattern pages. The full flow is
in the [knowledge lifecycle](../docs/knowledge-lifecycle.md).

## Go further

- [Your first contribution](first-contribution.md): from a question to your first pull request.
- [openstack-vm-runbooks](https://github.com/OzarLand/openstack-vm-runbooks#index): check whether your symptom already has a runbook.
- [kolla-ansible-deployment-patterns](https://github.com/OzarLand/kolla-ansible-deployment-patterns#index): how others deploy, before you ask how they do it.
- [GitHub conventions](../docs/github-conventions.md): discussions, issues, labels and branches, for every repository.
