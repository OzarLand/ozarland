# Reading path

An order in which to read the published runbooks of
[VM runbooks](https://academy.ozarland.com/runbooks/), from understanding how things work to
handling incidents. Each stage builds on the previous one. Read the "Quick checks" and "Diagnosis" sections first;
they are read-only and you can try them on a lab or a test project. Leave the steps marked ⚠️ and 🛑 for later, and
never run them on a platform you do not own.

Keep the [glossary](glossary.md) open while you read.

## Stage 1: understand what a request goes through

1. [What a VM creation traverses, and how to trace one failed boot by request id](https://academy.ozarland.com/runbooks/diagnostics/what-a-vm-creation-traverses-and-tracing-by-request-id/)
   — the path of a boot through Keystone, Nova, Placement, Glance and Neutron, and the one technique you will use
   in every investigation: following a request id through the logs.
2. [Control plane down: what still works for running instances](https://academy.ozarland.com/runbooks/diagnostics/control-plane-down-what-still-works-for-instances/)
   — why an API outage is not a workload outage.

## Stage 2: the first failures you will meet

3. [No valid host was found, although capacity exists](https://academy.ozarland.com/runbooks/scheduling/no-valid-host-with-free-capacity/)
   — the scheduler, Placement and cells, through the most common provisioning error.
4. [Instance stuck in BUILD, then ERROR after vif_plugging_timeout](https://academy.ozarland.com/runbooks/lifecycle/instance-stuck-in-build-waiting-for-vif-plugged/)
   — how Nova and Neutron cooperate when an instance boots, and a networking problem that looks like a compute one.
5. [New instance is ACTIVE but unreachable, it never got an IP address](https://academy.ozarland.com/runbooks/networking/new-instance-gets-no-ip-dhcp-agents-down/),
   then [New instance has an address, but no SSH key, no user data, default hostname](https://academy.ozarland.com/runbooks/networking/new-instance-boots-without-metadata/)
   — DHCP and the metadata service, the two things a new instance needs from Neutron at boot. Both were run on a lab.
6. [Instance has its address and metadata, but is unreachable from outside](https://academy.ozarland.com/runbooks/networking/instance-unreachable-from-outside/)
   — security groups, floating IPs and the router, in the order to check them.

## Stage 3: everyday operations

7. [Moving instances off a compute host for planned maintenance](https://academy.ozarland.com/runbooks/migration/moving-instances-off-a-host-for-maintenance/)
   — live migration, cold migration and their constraints; the operation behind every patching campaign.
8. [Restarting nova_libvirt on a compute](https://academy.ozarland.com/runbooks/lifecycle/restarting-nova-libvirt-does-not-stop-instances/) and
   [restarting the Open vSwitch agent on a compute](https://academy.ozarland.com/runbooks/networking/restarting-the-ovs-agent-does-not-cut-instances/)
   — which restarts running instances survive, measured on a lab.
9. [Stale records: stuck instances, orphan ports and attachments, phantom allocations](https://academy.ozarland.com/runbooks/lifecycle/stale-records-stuck-instances-orphan-ports-attachments/)
   — the routine clean-up of records that no longer describe anything real.
10. [Volume stuck in attaching, reserved or detaching](https://academy.ozarland.com/runbooks/volumes/volume-stuck-in-attaching-or-detaching/)
    — Nova and Cinder each keep a record of the attachment; forcing a status without checking the hypervisor is the
    real risk.
11. [CPU steal on pinned instances](https://academy.ozarland.com/runbooks/migration/cpu-steal-on-pinned-instances/)
    — a deeper one: what CPU pinning does and does not isolate.

## Stage 4: incidents

12. [VM creation fails platform-wide: check the shared dependencies first](https://academy.ozarland.com/runbooks/diagnostics/vm-creation-fails-platform-wide-check-shared-dependencies/)
    — Galera, RabbitMQ, memcached, the load balancer: what to look at before blaming Nova.
13. [Every API call fails at once: expired certificates or inconsistent Fernet keys](https://academy.ozarland.com/runbooks/diagnostics/expired-certificates-and-fernet-keys-break-every-api-call/)
    — the most preventable outages.
14. [nova-compute is down on a compute, but its instances are still running](https://academy.ozarland.com/runbooks/recovery/nova-compute-down-instances-still-running/)
    — a service down is not a host down; what to check before touching anything.
15. [Every instance on one compute loses the network (ovs-vswitchd down)](https://academy.ozarland.com/runbooks/networking/ovs-vswitchd-down-on-compute/)
    — the case where Nova shows `ACTIVE` and nothing answers.
16. [Compute host unreachable: fence before you evacuate](https://academy.ozarland.com/runbooks/recovery/compute-host-failure-fence-before-evacuate/)
    — the rule that protects data when a host disappears.
17. [Reopening provisioning after a control-plane incident](https://academy.ozarland.com/runbooks/recovery/reopening-provisioning-after-control-plane-incident/)
    — controlled degradation: stopping the APIs to recover safely.

The repository holds more runbooks than this path: a full compute disk, a drifted clock, an MTU mismatch, a router
stuck on a dead L3 agent, stale volume attachments and others. Find them in its
[index](https://academy.ozarland.com/runbooks/#index) when you meet the symptom.

## Practising safely

- Read-only commands (`openstack ... list`, `show`, logs) are safe on any platform you have access to.
- For the rest, a lab: an all-in-one or small multinode deployment you can break and rebuild. The deployment
  patterns repository describes some.
- When a runbook did not match what you saw, say so in an issue. That is a contribution, and an important one.

## Go further

- Next on the newcomer path: [your first contribution](first-contribution.md).
- [VM runbooks](https://academy.ozarland.com/runbooks/#index): the full index, including pages not in this path.
- [Deployment patterns](https://academy.ozarland.com/deploy/#index): labs and platforms you can practise on.
