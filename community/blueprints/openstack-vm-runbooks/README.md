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
| | | | |

## First pages to write

Candidate seed runbooks, chosen because almost every operator has met them. Each needs a real occurrence behind it.

1. Instance stuck in `deleting` after the compute host was lost.
2. `No valid host was found` with enough apparent capacity (Placement allocation candidates, aggregates, traits).
3. Instance stuck in `BUILD` / `spawning` (image download, volume creation, port binding, hypervisor).
4. Live migration fails: pre-check errors, shared storage assumptions, CPU model mismatch.
5. Instance has no network: no DHCP lease versus no metadata versus no external connectivity, and how to tell.
6. Floating IP does not answer: where to look between the router, the gateway and the security groups.
7. Volume stuck in `attaching` or `detaching`, and stale attachments on the Nova side.
8. Instance in `ERROR` after a resize: recovering with `reset-state` and what that does not fix.
9. Console not available: VNC/SPICE proxy and hypervisor side.
10. Evacuating instances from a dead compute node, and verifying nothing was duplicated.

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
