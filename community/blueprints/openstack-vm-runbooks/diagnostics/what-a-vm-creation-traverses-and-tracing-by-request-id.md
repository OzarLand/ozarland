---
title: What a VM creation traverses, and how to trace one failed boot by request id
kind: diagnostic
status: draft
openstack_releases: [unrecorded]
components: [nova, placement, neutron, glance, cinder, keystone, rabbitmq]
deployment_methods: [any]
environment:
  topology: any
  network: any
  storage: any
  os: any
risk: read-only
confirmed_by: []
upstream_refs:
  - https://docs.openstack.org/nova/latest/admin/architecture.html
  - https://docs.openstack.org/nova/latest/admin/cells.html
last_verified: 2026-10-18
---

# What a VM creation traverses, and how to trace one failed boot by request id

A failed VM creation says what the user experienced, not which service caused it. A scheduling problem looks like
a Nova problem, a network timeout like a Neutron problem, a slow operation like a capacity problem, and the
architecture makes each plausible without making any true. Knowing the path, and following one request id through
the logs, replaces guessing by timestamp.

## The path

```text
 user ──► Keystone (token) ──► nova-api ─────────────────────────────► API database (request recorded)
                                  │ RPC (RabbitMQ)
                                  ▼
                             nova-conductor ──► nova-scheduler ──► Placement (candidates, claim allocation)
                                  │                                   cell mapping: which cell DB holds the instance
                                  │ RPC
                                  ▼
                             nova-compute (selected host)
                                  ├──► Glance: image  (or Cinder: boot volume)
                                  ├──► Neutron: create + bind port  ──► agent / ovn-controller wires it
                                  │        ◄── network-vif-plugged event (Neutron ─► nova-api)
                                  └──► libvirt/QEMU: start the domain
```

Where each step fails, and what it looks like:

| Step | Failure shows as | First place to look |
|---|---|---|
| Keystone / memcached | 401, 503, or everything slow | Keystone logs, memcached, certificate expiry |
| nova-api → conductor (RPC) | Request accepted, instance never leaves `scheduling`; `MessagingTimeout` | RabbitMQ health, `nova-api.log` |
| Scheduler / Placement | `ERROR`, fault `No valid host was found`; no host assigned | `nova-scheduler.log`, Placement candidates ([runbook](../scheduling/no-valid-host-with-free-capacity.md)) |
| Cell mapping | `Host '<host>' is not mapped to any cell` | `nova-conductor.log`, `nova-manage cell_v2 list_hosts` |
| Glance | `BUILD`/`spawning` then image download error | `nova-compute.log`, `glance-api.log`, image store backend |
| Cinder (boot from volume) | `BUILD`/`block_device_mapping` stuck; volume stays `creating` | `cinder-volume.log`, storage backend |
| Neutron port create/bind | `binding_failed`; `Failed to bind port` | `neutron-server.log` |
| vif plug on the host | `BUILD`/`spawning` for `vif_plugging_timeout` then `ERROR` | Agent / `ovn-controller` on the host ([runbook](../lifecycle/instance-stuck-in-build-waiting-for-vif-plugged.md)) |
| libvirt / QEMU | `ERROR` with a libvirt error in `fault` | `nova-compute.log`, `libvirtd` log on the host |

Inside Nova the API, conductor, scheduler and compute talk over RabbitMQ. Calls to Keystone, Placement, Glance,
Neutron and Cinder are REST calls through the service catalogue. With agent-based networking, `neutron-server`
talks to its agents over RabbitMQ as well; OVN uses its own databases instead. Every service reads and writes its
own database. A user-visible failure can therefore originate in any service, in the bus, in the database cluster,
or in the network and storage underneath.

## Tracing one request

Every API request carries a request id (`req-<uuid>`) that the services propagate in their logs. Get it, then
follow it.

```bash
# From the failed instance's actions (the request id of the create action)
openstack server event list <server-id>
openstack server event show <server-id> <request-id>       # per-service events and tracebacks (admin)

# Or from the client that made the call
openstack --debug server create ... 2>&1 | grep -i x-openstack-request-id
```

Then search every service's logs for that id, in path order:

**Kolla-Ansible:** logs are under `/var/log/kolla/<service>/` on each node.
```bash
grep -h "<request-id>" /var/log/kolla/nova/nova-api.log /var/log/kolla/nova/nova-conductor.log \
     /var/log/kolla/nova/nova-scheduler.log /var/log/kolla/placement/placement-api.log \
     /var/log/kolla/neutron/neutron-server.log /var/log/kolla/glance/glance-api.log | sort
# and on the selected compute host
grep "<request-id>" /var/log/kolla/nova/nova-compute.log
```
**Any:** `journalctl -u <service> | grep <request-id>`, or the configured log files. A platform whose logs are
centralised and searchable by request id follows one boot across Nova, Placement, Neutron and Glance in minutes.

Note that Neutron and Glance log their own request ids for the calls Nova makes to them; Nova logs the
downstream id next to its own (`req-... req-...` pairs in recent releases), which is how you hop from one service
to the next.

## Reading what you find

- The **last service that logged the request id** is where it stopped; the first error after that point is the
  cause, or the symptom of a dependency (bus, database) failing underneath.
- Separate **facts** (observed in logs), **hypotheses** (explain the facts) and **assumptions** (not yet shown).
  Familiar fixes are attractive; a known fix applied to a different failure mode adds risk.
- **Try to disprove** your hypothesis as well as confirm it: can the behaviour be reproduced on one host, with one
  flavor, on one network? Reducing the surface makes every observation worth more.
- If one request fails and others succeed, compare them: same host? same network type? same image? The difference
  is the lead.

## Validity and limits

Describes the Nova cells v2 architecture (mandatory since Pike) with the libvirt driver and the Neutron ML2 or OVN
backends. Log paths are given for Kolla-Ansible; other deployments differ. Request-id pairing in logs depends on
release and on `oslo.log` configuration.

## Related

- [VM creation fails platform-wide: check the shared dependencies first](vm-creation-fails-platform-wide-check-shared-dependencies.md).
- Source: *OpenStack, the Day After Tomorrow* (S. Zaouam), chapters 5, 8 and 9.
