# How to read a runbook

OzarLand pages all follow the same structure, so that you can find what you need quickly, even under pressure.
Five minutes here will save you time on every page you read afterwards.

## The block at the top

Every page starts with a block of metadata. Read it first: it tells you whether the page applies to your platform.

```yaml
status: lab-verified                  # how much it has been checked (below)
openstack_releases: ["2026.1"]        # releases on which it was observed
deployment_methods: [kolla-ansible]   # how the platform was deployed
environment:                          # the conditions that matter
  network: ml2/ovs (VXLAN)
risk: state-changing                  # the most dangerous step in the page
```

If your release, deployment method or network backend differs, the page may still help, but read it as a lead,
not as a recipe.

## What the status means

| Status | Meaning | How much to trust it |
|---|---|---|
| `draft` | Written by one person from their experience or from documentation | A good lead; check each step |
| `lab-verified` | Its steps were run on a lab platform and behaved as written | The commands work; production may differ |
| `validated` | Confirmed by another operator on another platform | The strongest level; still check the release |
| `experimental` | Unconfirmed, narrow, or possibly outdated | Read the page's warnings carefully |

The **Validity and limits** section near the end of every page says exactly what was and was not tested. A
solution that worked somewhere is documented as exactly that, never as universal.

## The sections, in order

1. **Symptom**: what you see. Compare it carefully with what you see.
2. **Impact**: who and what is affected.
3. **Quick checks**: three to five **read-only** commands that confirm you are on the right page.
4. **Diagnosis**: how to find the cause, still read-only.
5. **Possible causes**: the known causes and how to tell them apart.
6. **Resolution**: the fix for each cause. This is where commands change things.
7. **Verification**: how to prove it is fixed and nothing else broke.
8. **Validity and limits**: where the page was observed, and what was not tested.

Read sections 1 to 5 before running anything in section 6.

## The warnings

| Marker | Meaning | What to do |
|---|---|---|
| no marker | Read-only: observes, changes nothing | Safe on any platform you can access |
| ⚠️ **State-changing** | Changes the platform in a bounded, reversible way (restart a service, disable a host) | Understand the warning; do it on a platform you are responsible for |
| 🛑 **Destructive** | Can lose data, interrupt workloads, or cannot be undone | Check the precondition, take the backup, and get a second pair of eyes if you are new |

As a newcomer: run the read-only steps freely on a lab or a test project, and leave the ⚠️ and 🛑 steps to
platforms you own and understand.

## Placeholders

Commands use placeholders in angle brackets: `openstack server show <server-id>`. Replace them with your own
values. Lines marked `**Kolla-Ansible:**` or `**Any:**` give variants for a deployment method; `Any` works with
the OpenStack CLI whatever deployed the platform.

## Go further

- Next on the newcomer path: the [reading path through the runbooks](reading-path.md).
- [openstack-vm-runbooks](https://github.com/OzarLand/openstack-vm-runbooks): every runbook follows this structure.
- [kolla-ansible-deployment-patterns](https://github.com/OzarLand/kolla-ansible-deployment-patterns): deployment patterns follow a similar structure, with context and choices
  instead of symptoms.
- The [content conventions](../docs/conventions/README.md) behind this page, for contributors.
