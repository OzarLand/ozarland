# Reading path

An order in which to read the published runbooks of
[openstack-vm-runbooks](https://github.com/OzarLand/openstack-vm-runbooks), from understanding how things work to
handling incidents. Each stage builds on the previous one. Read the "Quick checks" and "Diagnosis" sections first;
they are read-only and you can try them on a lab or a test project. Leave the steps marked ⚠️ and 🛑 for later, and
never run them on a platform you do not own.

Keep the [glossary](glossary.md) open while you read.

## Stage 1: understand what a request goes through

1. [What a VM creation traverses, and how to trace one failed boot by request id](https://github.com/OzarLand/openstack-vm-runbooks/blob/main/diagnostics/what-a-vm-creation-traverses-and-tracing-by-request-id.md)
   — the path of a boot through Keystone, Nova, Placement, Glance and Neutron, and the one technique you will use
   in every investigation: following a request id through the logs.
2. [Control plane down: what still works for running instances](https://github.com/OzarLand/openstack-vm-runbooks/blob/main/diagnostics/control-plane-down-what-still-works-for-instances.md)
   — why an API outage is not a workload outage.

## Stage 2: the first failures you will meet

3. [No valid host was found, although capacity exists](https://github.com/OzarLand/openstack-vm-runbooks/blob/main/scheduling/no-valid-host-with-free-capacity.md)
   — the scheduler, Placement and cells, through the most common provisioning error.
4. [Instance stuck in BUILD, then ERROR after vif_plugging_timeout](https://github.com/OzarLand/openstack-vm-runbooks/blob/main/lifecycle/instance-stuck-in-build-waiting-for-vif-plugged.md)
   — how Nova and Neutron cooperate when an instance boots, and a networking problem that looks like a compute one.

## Stage 3: everyday operations

5. [Moving instances off a compute host for planned maintenance](https://github.com/OzarLand/openstack-vm-runbooks/blob/main/migration/moving-instances-off-a-host-for-maintenance.md)
   — live migration, cold migration and their constraints; the operation behind every patching campaign.
6. [Stale records: stuck instances, orphan ports and attachments, phantom allocations](https://github.com/OzarLand/openstack-vm-runbooks/blob/main/lifecycle/stale-records-stuck-instances-orphan-ports-attachments.md)
   — the routine clean-up of records that no longer describe anything real.
7. [CPU steal on pinned instances](https://github.com/OzarLand/openstack-vm-runbooks/blob/main/migration/cpu-steal-on-pinned-instances.md)
   — a deeper one: what CPU pinning does and does not isolate.

## Stage 4: incidents

8. [VM creation fails platform-wide: check the shared dependencies first](https://github.com/OzarLand/openstack-vm-runbooks/blob/main/diagnostics/vm-creation-fails-platform-wide-check-shared-dependencies.md)
   — Galera, RabbitMQ, memcached, the load balancer: what to look at before blaming Nova.
9. [Every API call fails at once: expired certificates or inconsistent Fernet keys](https://github.com/OzarLand/openstack-vm-runbooks/blob/main/diagnostics/expired-certificates-and-fernet-keys-break-every-api-call.md)
   — the most preventable outages.
10. [Compute host unreachable: fence before you evacuate](https://github.com/OzarLand/openstack-vm-runbooks/blob/main/recovery/compute-host-failure-fence-before-evacuate.md)
    — the rule that protects data when a host disappears.
11. [Reopening provisioning after a control-plane incident](https://github.com/OzarLand/openstack-vm-runbooks/blob/main/recovery/reopening-provisioning-after-control-plane-incident.md)
    — controlled degradation: stopping the APIs to recover safely.

## Pages on their way

More runbooks, many from failures reproduced on a lab, are in review in the repository's
[open pull requests](https://github.com/OzarLand/openstack-vm-runbooks/pulls): instance networking (DHCP,
metadata, routers, MTU, Open vSwitch), a full compute disk, `nova-compute` down. They will join this path once
merged. Deployment patterns are collected in
[kolla-ansible-deployment-patterns](https://github.com/OzarLand/kolla-ansible-deployment-patterns).

## Practising safely

- Read-only commands (`openstack ... list`, `show`, logs) are safe on any platform you have access to.
- For the rest, a lab: an all-in-one or small multinode deployment you can break and rebuild. The deployment
  patterns repository describes some.
- When a runbook did not match what you saw, say so in an issue. That is a contribution, and an important one.
