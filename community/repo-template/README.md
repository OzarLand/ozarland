[← OzarLand home](https://github.com/OzarLand/ozarland)

# <repository-name>

**<One sentence: what this repository collects, for whom.>**

<!-- Layout and visual rules: https://github.com/OzarLand/ozarland/blob/main/docs/conventions/readme-identity.md -->

<!-- Two or three sentences: what this repository is for, and the operational problems it helps with. -->

Part of [OzarLand](https://github.com/OzarLand/ozarland): *a shared land for better OpenStack operations.* No imposed
tools, no single way of operating OpenStack.

## Scope

<!-- What belongs here, what does not, and where the rest goes (link to the other community repositories). -->

**In scope:**

-

**Out of scope:**

-

## How content is organised

```text
<directory>/        <what it holds>
templates/          page templates for this repository
```

Every page carries metadata (release, components, deployment method, status, confirmations) as described in the
[content conventions](https://github.com/OzarLand/ozarland/blob/main/docs/conventions/README.md). A page's `status`
tells you how much it has been verified: `draft` (one operator), `lab-verified` (its steps were run on a lab),
`validated` (confirmed by another operator), `experimental` (unconfirmed or possibly outdated).

## Index

<!-- Keep a flat, searchable list of pages, grouped by directory. -->

| Page | Components | Releases | Status |
|---|---|---|---|
| | | | |

## Contributing

- **Ask a question:** open a Q&A discussion.
- **Share a problem you solved:** open an issue with the *Problem solved* template, or a pull request with a page.
- **Confirm a page in your environment:** comment on it or open a *Documentation proposal* issue. This is how pages
  become validated.
- **Add or improve a page:** copy the template from `templates/`, open a pull request.

Rules that are not optional: no secrets, hostnames, addresses or unredacted logs; flag state-changing and
destructive commands; say where your solution was observed. Full guide: [CONTRIBUTING.md](CONTRIBUTING.md).

## 🌍 Part of OzarLand

**OzarLand: a shared land for better OpenStack operations.** It started as a personal initiative by Soufian Zaouam
to share practical OpenStack operational knowledge, and it is meant to grow into a space where operators exchange
experience, document solutions and help each other run more reliable platforms. It is open to everyone: your
knowledge, questions and corrections are welcome.

| | Repository | What it holds |
|:-:|---|---|
| | [ozarland](https://github.com/OzarLand/ozarland) | Start here: newcomer path, community rules, [Discussions](https://github.com/OzarLand/ozarland/discussions) |
| 🔧 | [openstack-vm-runbooks](https://github.com/OzarLand/openstack-vm-runbooks) | Symptom-driven runbooks for instance problems |
| 🏗️ | [kolla-ansible-deployment-patterns](https://github.com/OzarLand/kolla-ansible-deployment-patterns) | Ways to deploy with Kolla-Ansible, compared |
| 🧪 | [openstack-quick-lab](https://github.com/OzarLand/openstack-quick-lab) | A disposable OpenStack lab to practise on |
| 🤖 | [openstack-operator-skills](https://github.com/OzarLand/openstack-operator-skills) | Claude skills that apply this knowledge |

## License

All content, documentation and code alike, is licensed under the Apache License 2.0 ([LICENSE](LICENSE)). Reuse it
freely with attribution. See [licensing](https://github.com/OzarLand/ozarland/blob/main/docs/conventions/licensing.md).

OpenStack is a project of the OpenInfra Foundation community. OzarLand is an independent community initiative.
