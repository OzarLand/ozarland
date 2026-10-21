# Content metadata

Every page starts with a metadata block so that a reader knows at a glance whether the content applies to their
platform, and how much it has been verified. It is written as YAML front matter, which GitHub renders as a table.

```yaml
---
title: Instance stuck in deleting state
kind: runbook                 # runbook | pattern | playbook | experience-report | diagnostic | comparison
status: draft                 # draft | lab-verified | validated | experimental
openstack_releases: [2024.2, 2025.1]   # releases where this was observed; use upstream names
components: [nova, neutron]   # OpenStack and infrastructure components involved
deployment_methods: [kolla-ansible]    # kolla-ansible | openstack-ansible | charmed | vendor | manual | any
environment:                  # only what matters for validity
  topology: multinode, 3 controllers
  network: ovn
  storage: ceph-rbd
  os: ubuntu-24.04
risk: state-changing          # read-only | state-changing | destructive  (highest level present in the page)
confirmed_by:                 # one entry per independent confirmation
  - { who: "@handle", type: operator, release: 2025.1, deployment: kolla-ansible, date: 2026-11-02, note: "also needed X" }
  - { who: "agent:lab-reviewer", type: lab, release: 2025.1, deployment: kolla-ansible all-in-one, date: 2026-10-21, note: "read-only steps run; destructive steps reproduced on a disposable lab" }
upstream_refs:                # bugs, docs, changes this page relates to
  - https://bugs.launchpad.net/nova/+bug/NNNNNNN
last_verified: 2026-10-18
---
```

## Field rules

- **`openstack_releases`** uses upstream release names (`2024.1`, `2024.2`, `2025.1`, `2025.2`, …, or legacy
  names such as `zed`, `antelope`). Never write "latest". A page observed on one release lists one release.
- **`components`** uses lowercase project names (`nova`, `neutron`, `cinder`, `glance`, `keystone`, `placement`,
  `octavia`, `horizon`) and infrastructure names (`mariadb`, `rabbitmq`, `haproxy`, `keepalived`, `memcached`,
  `ceph`, `ovn`, `ovs`, `libvirt`, `qemu`).
- **`deployment_methods`** says where the procedure was applied. `any` is allowed only when the procedure uses
  OpenStack APIs and CLI alone and does not depend on how services are deployed.
- **`status`** follows the [knowledge lifecycle](../knowledge-lifecycle.md): `draft` until checked, `lab-verified`
  once its steps were run on a lab (`type: lab` confirmation), `validated` once an operator other than the author
  confirmed it (`type: operator`), `experimental` when unconfirmed, narrow or possibly outdated.
- **`confirmed_by[].type`** is `operator` (a person who applied the page on a real platform; the default) or `lab`
  (a lab run by a contributor or an agent). Lab entries say what was run: read-only steps only, or the full
  procedure on a disposable lab.
- **`confirmed_by`** is appended by reviewers or by the people who report back, never by the author for their own
  page. A confirmation on a new release adds the release to `openstack_releases`.
- **`risk`** is the highest risk level of any command in the page, so that a reader knows before opening it. See
  [risk warnings](risk-warnings.md).
- **`last_verified`** is updated whenever someone confirms the page still holds.

## Stating validity in prose

Beyond the front matter, every runbook and pattern has a short **Validity and limits** section:

> Observed on 2024.2 and 2025.1 with Kolla-Ansible and OVN. Not tested with OVS or on OpenStack-Ansible. The
> `nova-manage` step is unnecessary on 2025.1 (fixed upstream, see bug …). We believe but did not confirm that the
> cause is X.

Be concrete about what you did not test. It helps the next person far more than a confident generalisation.
