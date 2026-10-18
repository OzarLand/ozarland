# openstack-vm-runbooks

**Community runbooks for diagnosing and resolving virtual machine problems in OpenStack.**

Part of [OzarLand](https://github.com/OzarLand/ozarland), a collaborative knowledge-sharing space for OpenStack
operators. Share experiences, document solutions, learn from each other. No imposed tools, no single way of
operating OpenStack.

> **Repository metadata to apply:** description "Community runbooks for diagnosing and resolving OpenStack instance
> problems: stuck states, scheduling, boot, migration, networking, volumes. Nova, Neutron, Glance, Cinder." Topics:
> `openstack`, `nova`, `neutron`, `cinder`, `runbooks`, `troubleshooting`, `openstack-operations`, `sre`.

## Scope

Everything an operator does when an instance misbehaves, from the first symptom to the post-fix checks.

**In scope:**

- Instances stuck in an unexpected state (`BUILD`, `deleting`, `resizing`, `migrating`, `ERROR`, `SHUTOFF` when
  it should run, task states that never clear).
- Boot and scheduling failures: `No valid host`, Placement allocation problems, image or flavor issues, boot from
  volume failures, console not available.
- Create, delete and migration errors: live and cold migration, resize, evacuation, shelve and unshelve.
- Instance networking: no DHCP lease, no metadata, no floating IP connectivity, security group surprises, MTU
  symptoms as seen from the instance, port binding failures.
- Volumes: attach and detach failures, stale attachments, volumes stuck `attaching`/`detaching`/`in-use`, boot
  volume problems, multi-attach.
- Diagnostics across Nova, Neutron, Glance, Cinder and Placement with the OpenStack CLI, service logs and the
  hypervisor (libvirt, QEMU).
- Recovery after an incident (compute node loss, storage outage, control plane outage) as it affects instances,
  and the verifications to run afterwards.

**Out of scope:** deploying OpenStack (see `kolla-ansible-deployment-patterns`), upgrading it (see
`openstack-upgrade-playbooks`), and problems that do not surface through instances (control-plane-only,
networking-agent-only, storage-backend-only), which are collected in `ozarland` discussions until a dedicated
runbook repository exists.

## How content is organised

```text
lifecycle/        stuck states, create, delete, resize, shelve
scheduling/       No valid host, Placement, flavors, images, boot from volume
migration/        live and cold migration, evacuation, resize across hosts
networking/       instance connectivity, DHCP, metadata, floating IPs, security groups, port binding
volumes/          attach, detach, stale attachments, boot volumes
diagnostics/      how to read Nova, Neutron, Cinder, Glance, Placement, libvirt logs and states
recovery/         after a compute, storage or control plane incident; post-incident checks
templates/        runbook template
```

Each runbook follows the shared [runbook structure](https://github.com/OzarLand/ozarland/blob/main/docs/conventions/runbook-structure.md):
symptom, impact, quick checks, diagnosis, possible causes, resolution, verification, validity and limits.
State-changing commands carry ⚠️, destructive ones carry 🛑 with what can be lost and what to check first.

A runbook's `status` says how much it has been verified: `draft` (one operator), `validated` (confirmed by someone
else), `experimental` (unconfirmed or possibly outdated). A page written for one deployment method is welcome;
variants for other methods are added by whoever has them.

## Index

| Page | Components | Releases | Status |
|---|---|---|---|
| [Instance stuck in BUILD, then ERROR after vif_plugging_timeout](lifecycle/instance-stuck-in-build-waiting-for-vif-plugged.md) | nova, neutron, ovn, ovs | unrecorded | draft |
| [Stale records: stuck instances, orphan ports and attachments, phantom allocations](lifecycle/stale-records-stuck-instances-orphan-ports-attachments.md) | nova, placement, neutron, cinder | unrecorded | draft |
| [No valid host was found, although capacity exists](scheduling/no-valid-host-with-free-capacity.md) | nova, placement | unrecorded | draft |
| [Moving instances off a compute host for planned maintenance](migration/moving-instances-off-a-host-for-maintenance.md) | nova, libvirt, qemu | unrecorded | draft |
| [CPU steal time on pinned instances; live migration moves the symptom](migration/cpu-steal-on-pinned-instances.md) | nova, libvirt, qemu | unrecorded | draft |
| [Compute host unreachable: fence before you evacuate](recovery/compute-host-failure-fence-before-evacuate.md) | nova, libvirt, cinder, ceph | unrecorded | draft |
| [Reopening provisioning after a control-plane incident](recovery/reopening-provisioning-after-control-plane-incident.md) | nova, neutron, rabbitmq, mariadb | unrecorded | draft |
| [VM creation fails platform-wide: check the shared dependencies first](diagnostics/vm-creation-fails-platform-wide-check-shared-dependencies.md) | rabbitmq, mariadb, keystone, haproxy | unrecorded | draft |
| [What a VM creation traverses, and tracing one boot by request id](diagnostics/what-a-vm-creation-traverses-and-tracing-by-request-id.md) | nova, placement, neutron, glance, cinder | unrecorded | draft |
| [Control plane down: what still works for running instances](diagnostics/control-plane-down-what-still-works-for-instances.md) | nova, neutron, ovn, ovs | unrecorded | draft |

**About the seed pages.** The first pages were written from incidents and technical notes described by the
founding maintainer in *OpenStack, the Day After Tomorrow*, rewritten in runbook form with the author's
permission. The source does not record the OpenStack release on which each incident happened, so these pages carry
`openstack_releases: [unrecorded]` and `status: draft`. The first confirmations from other operators will add the
releases and move them to `validated`. Confirming one of them on your platform is the most useful first
contribution you can make.

## Pages wanted next

Candidate runbooks that almost every operator has met and that are not written yet. Each needs a real occurrence
behind it; open a *Problem solved* issue if you have one.

1. Live migration fails: pre-check errors, shared storage assumptions, CPU model mismatch.
2. Instance has no network: no DHCP lease versus no metadata versus no external connectivity, and how to tell.
3. Floating IP does not answer: where to look between the router, the gateway and the security groups.
4. Volume stuck in `attaching` or `detaching` (the Cinder side of stale attachments).
5. Instance in `ERROR` after a resize: recovering with `reset-state` and what that does not fix.
6. Console not available: VNC/SPICE proxy and hypervisor side.
7. Instance stuck in `deleting` after the compute host was lost (the deletion-specific details beyond the stale-records page).

## Contributing

- **Ask a question:** open a Q&A discussion.
- **Share a problem you solved:** open an issue with the *Problem solved* template, or a pull request with a runbook.
- **Confirm a runbook in your environment:** comment on it or open a *Documentation proposal* issue. This is how
  runbooks become validated.
- **Add or improve a runbook:** copy `templates/runbook.md`, open a pull request.

Rules that are not optional: no secrets, hostnames, addresses or unredacted logs; flag state-changing and
destructive commands; say where your solution was observed. Full guide: [CONTRIBUTING.md](CONTRIBUTING.md).

## License

All content, documentation and code alike, is licensed under the Apache License 2.0 ([LICENSE](LICENSE)). Reuse it
freely with attribution. See [licensing](https://github.com/OzarLand/ozarland/blob/main/docs/conventions/licensing.md).

OpenStack is a project of the OpenInfra Foundation community. OzarLand is an independent community initiative.
