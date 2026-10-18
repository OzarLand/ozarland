---
title: Control plane down. What still works for running instances, and what does not
kind: diagnostic
status: draft
openstack_releases: [unrecorded]
components: [nova, neutron, ovn, ovs, libvirt]
deployment_methods: [any]
environment:
  topology: any
  network: ml2/ovs or ovn; behaviour differs
  storage: any
  os: any
risk: read-only
confirmed_by: []
upstream_refs:
  - https://docs.openstack.org/nova/latest/admin/architecture.html
  - https://docs.openstack.org/neutron/latest/admin/config-dhcp-ha.html
  - https://docs.openstack.org/neutron/latest/admin/ovn/
last_verified: 2026-10-18
---

# Control plane down. What still works for running instances, and what does not

The facts that make "stop the APIs, protect the running workloads" a credible option rather than a euphemism for
an outage. Verify them for your own platform before an incident; they depend on the networking backend.

## What keeps working when the APIs, the bus and the databases are down

- **Running instances** keep running, keep their disks, keep exchanging traffic. The data plane (hypervisors,
  disks, network paths) does not depend on the control plane to carry existing state.
- **Existing DHCP leases** keep being served: with ML2/OVS, by the DHCP agent's `dnsmasq` on the network node as
  long as that host runs; with OVN, DHCP is answered locally on each compute by `ovn-controller`.
- **Router failover** with L3 HA (keepalived) or OVN gateway chassis is a data-plane mechanism and does not need
  the API.
- **Security groups, floating IPs, routes already programmed** stay in effect.

## What is lost

- Creating, modifying, migrating or deleting any resource.
- **Propagation of new state** to the data plane: a new port, a changed security-group rule, a newly associated
  floating IP will not take effect until the control plane returns.
- **Metadata**: an instance that boots or reboots during the outage may fail to reach the metadata service
  (cloud-init keys, hostname, user data), because the metadata agent or proxy needs Nova and Neutron APIs.
- **DHCP for new instances or expired leases** with ML2/OVS, if `neutron-dhcp-agent` cannot reach `neutron-server`
  for new port information (existing leases continue).
- Console access (VNC/SPICE proxies need the API).
- Monitoring that reads the APIs goes blind; the instances are fine, the dashboards are not.

## Two cautions

1. **"Stopping the control plane" means the APIs, the bus and the databases, not the agents.** Neutron agents and
   `ovn-controller` run on the data-plane nodes. Restarting some of them, depending on version and configuration,
   can interrupt traffic briefly (OVS agent restarts may reprogram flows). Leave them alone during a controlled
   stop.
2. **The exact behaviour depends on the backend and the deployment.** Verify on a lab or during a recovery
   exercise: stop the APIs and the bus, then check that an instance keeps its connectivity, renews its lease, and
   that a router failover still works. Write the result down for your platform.

## How to check on a live platform, read-only

```bash
# From a host that can reach the instance network (or from another instance)
ping -c 3 <instance-address>

# Lease state inside the instance (console or existing session)
ip -4 addr; cat /var/lib/dhcp/dhclient*.leases 2>/dev/null | tail -5     # or networkctl / nmcli

# ML2/OVS: dnsmasq still serving on the network node
ps -ef | grep -F "dnsmasq --no-hosts" | grep -F "<network-id>"
# OVN: controller still up on the compute, ports still bound
ovs-vsctl show | head; ovn-sbctl show 2>/dev/null       # sbctl needs the southbound DB, which may be up independently

# L3 HA: which node is master for the router
ip netns exec qrouter-<router-id> ip addr | grep -F "<router-external-address>"
```

## Validity and limits

General behaviour of Nova and Neutron with ML2/OVS and OVN as documented upstream and observed by an operator in a
real control-plane incident; release not recorded. Other backends (Linux Bridge, SR-IOV, vendor SDN) differ.
Octavia load balancers, Designate records and other services with their own data-plane components have their own
behaviour, not covered here.

## Related

- [Reopening provisioning after a control-plane incident](../recovery/reopening-provisioning-after-control-plane-incident.md).
- [VM creation fails platform-wide](vm-creation-fails-platform-wide-check-shared-dependencies.md).
- Source: *OpenStack, the Day After Tomorrow* (S. Zaouam), chapter 1, technical note on control plane and data plane.
