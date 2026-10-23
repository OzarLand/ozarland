# OzarLand

**OpenStack operators sharing what they learn in production: fixes, deployment choices, experience.**
Open to everyone, whatever tool deployed your cloud.
*[When AI meets OpenStack](docs/how-ozarland-is-built.md): AI agents write, review and lab-test pages; people decide and confirm.*

## Where to start?

| You are… | Go to |
|---|---|
| 🌱 **New to OpenStack** | [Newcomer path](newcomers/README.md): five short pages, read in order |
| 🧪 **Want to try OpenStack** | [openstack-quick-lab](https://github.com/OzarLand/openstack-quick-lab): one VM, about one hour, one command to delete it |
| 🔧 **Fixing a problem with a VM** | [VM runbooks](https://github.com/OzarLand/openstack-vm-runbooks#index) (step-by-step guides to diagnose and fix a known problem): find your symptom |
| 🏗️ **Deploying a platform** | [Deployment patterns](https://github.com/OzarLand/kolla-ansible-deployment-patterns#index) (how real platforms were built, and what each choice implies): learn from others |
| 🤝 **Ready to contribute** | [Your first contribution](newcomers/first-contribution.md): start with ten minutes |

Nothing matches, or a question? [Start a discussion](newcomers/start-a-discussion.md) (the public question-and-answer
forum of this repository).

## What OzarLand does not do

- It does not recommend one way, one tool or one architecture to run OpenStack.
- It does not certify procedures: "validated" means confirmed by operators, nothing more.
- It does not replace the upstream OpenStack documentation; it adds operational experience and links to it.
- It is not a support service: people help each other when they can.

More in [mission and principles](docs/vision.md).

## What makes a page trustworthy

- It says **where it was observed**: OpenStack release, components, deployment method.
- It says **how much it was checked**, with one of four statuses
  ([knowledge lifecycle](docs/knowledge-lifecycle.md)):

  | Status | What it means |
  |---|---|
  | `draft` | Written; its commands have not been run by anyone other than the author. |
  | `lab-verified` | Its commands were run on a lab by someone other than the author, on the release stated in the page. |
  | `validated` | Confirmed by a human operator, other than the author, on a real platform. |
  | `experimental` | Possibly outdated, or confirmed only under narrow conditions. |

  Today (2026-10-23, counted with [`tools/coverage_report.py`](tools/coverage_report.py)): **0 validated, 12 lab-verified, 21 draft,
  0 experimental**, out of the 33 pages of the runbook and deployment-pattern repositories.

- Pages are written and lab-tested with AI agents, reviewed independently, and validated only by human operators:
  [how OzarLand is built](docs/how-ozarland-is-built.md).
- Commands that change things are marked ⚠️, destructive ones 🛑.
- No secrets, real hostnames or addresses, or unredacted logs, ever.

## Repositories

| Repository | What it holds |
|---|---|
| [openstack-vm-runbooks](https://github.com/OzarLand/openstack-vm-runbooks) | Symptom-driven runbooks for instance problems |
| [kolla-ansible-deployment-patterns](https://github.com/OzarLand/kolla-ansible-deployment-patterns) | How operators deploy with Kolla-Ansible (one of the common tools that install OpenStack), and what each choice implies |
| [openstack-quick-lab](https://github.com/OzarLand/openstack-quick-lab) | A disposable all-in-one OpenStack on one VM, with exercises that use the runbooks |
| `ozarland` (here) | The newcomer path, the community rules, the templates, the [Discussions](https://github.com/OzarLand/ozarland/discussions) |

Status, planned and archived repositories: [current repositories](docs/repositories.md#current-repositories).

## Learn more

- [Mission, principles and who OzarLand is for](docs/vision.md)
- [What you will find, and how repositories are organised](docs/repositories.md)
- [How to contribute](CONTRIBUTING.md), short on purpose
- [Content conventions](docs/conventions/README.md) and [shared templates](community/README.md)
- [Glossary](newcomers/glossary.md)
- [Governance](docs/governance.md), [agents](docs/agents.md) and the [review and merge policy](docs/review-policy.md)
- [GitHub conventions](docs/github-conventions.md) and [decision records](docs/adr/README.md)

## License

Apache License 2.0 for all content ([LICENSE](LICENSE), [licensing](docs/conventions/licensing.md)). OzarLand is an
independent community initiative, not affiliated with or endorsed by the OpenInfra Foundation or any vendor.
