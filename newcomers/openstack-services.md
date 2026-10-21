# The OpenStack services, for operators

What each service does, what it depends on, and what usually goes wrong with it in production. This page is about
operating OpenStack, not about using it, and it applies whatever tool deployed your platform.

## The big picture

An OpenStack cloud is a set of independent services that talk to each other. Each one has an API, its own database,
and workers. Underneath them sit a few shared infrastructure services: a database cluster, a message bus, a cache
and a load balancer. Underneath those are the hosts: controllers that run the services, and computes that run the
virtual machines.

```text
 users, CLI, Horizon
        │ HTTPS through the load balancer (HAProxy + keepalived VIP)
        ▼
 ┌─────────────── control plane ───────────────┐
 │ Keystone  Nova  Placement  Neutron  Glance  │
 │ Cinder  (Horizon, Heat, Octavia, ...)       │
 │       │            │             │          │
 │   MariaDB/Galera  RabbitMQ   memcached      │
 └──────────────────────┬──────────────────────┘
                        │ RPC and REST
 ┌──────────────── data plane ─────────────────┐
 │ computes: nova-compute, libvirt/QEMU,       │
 │ OVS or OVN, the instances and their disks;  │
 │ network nodes: routers, DHCP, metadata      │
 └─────────────────────────────────────────────┘
```

One fact explains much of what operators do: **the control plane and the data plane fail separately.** When the
APIs, the database or the message bus are down, running instances keep running and keep their network; what stops
is creating, changing or deleting things. See the runbook
[Control plane down: what still works for running instances](https://github.com/OzarLand/openstack-vm-runbooks/blob/main/diagnostics/control-plane-down-what-still-works-for-instances.md).

## The core services

| Service | What it does | Depends on | What usually breaks |
|---|---|---|---|
| **Keystone** (identity) | Authenticates users and services, issues tokens, holds projects, users, roles and the service catalogue | MariaDB, memcached | Expired certificates, inconsistent Fernet keys between nodes, memcached loss making every call slow |
| **Nova** (compute) | Creates and manages instances. `nova-api` takes requests, `nova-scheduler` picks a host, `nova-conductor` coordinates and talks to the database, `nova-compute` drives the hypervisor on each compute | Keystone, Placement, Neutron, Glance, Cinder, RabbitMQ, MariaDB | `No valid host`, instances stuck in a transitional state, a compute service reported down, stale records |
| **Placement** | Keeps the inventory of resources (CPU, RAM, disk, devices) of each host and the allocations of each instance; the scheduler asks it where things fit | Keystone, MariaDB | Allocations that no longer match reality, wrong allocation ratios |
| **Neutron** (networking) | Networks, subnets, ports, routers, floating IPs, security groups. `neutron-server` plus agents (Open vSwitch, L3, DHCP, metadata) or OVN controllers on the hosts | Keystone, RabbitMQ (agent-based backends), MariaDB, OVS or OVN | Port binding failures, agents down, MTU mismatches, routers stuck on a dead agent, no metadata |
| **Glance** (images) | Stores and serves the images instances boot from | Keystone, MariaDB, a storage backend (file, Ceph, Swift...) | Backend full or unreachable, slow image downloads during boot |
| **Cinder** (block storage) | Volumes and their attachment to instances; `cinder-volume` drives the storage backend | Keystone, RabbitMQ, MariaDB, a backend (Ceph, LVM, NFS, arrays) | Volumes stuck attaching or detaching, attachments Nova and Cinder disagree on |
| **Horizon** (dashboard) | The web interface | Keystone and every service's API | Mostly the services behind it |

Other services you may meet: **Heat** (orchestration), **Octavia** (load balancers), **Designate** (DNS),
**Swift** (object storage), **Ironic** (bare metal), **Barbican** (secrets), **Magnum** (container clusters). Each
has its own agents and its own ways to fail.

## The shared infrastructure

| Component | Role | Why operators care |
|---|---|---|
| **MariaDB with Galera** | The databases of every service, replicated across controllers | Writable only while a majority of nodes see each other; recovery after a full outage must start from the most advanced node |
| **RabbitMQ** | The message bus for RPC inside services (and between Neutron and its agents with agent-based backends) | Partitions, memory or disk alarms and queues without consumers stop work silently while processes look alive |
| **memcached** | Cache, notably for token validation | Its loss makes every API call slow or failing |
| **HAProxy and keepalived** | Load balancing of the APIs behind a virtual IP that moves between controllers | The VIP is how users reach anything; it is also what lets operators stop the APIs in a controlled way |
| **libvirt and QEMU/KVM** | The hypervisor on each compute | Instances are QEMU processes; libvirt can often be restarted without stopping them |
| **Open vSwitch or OVN** | The virtual switching on each host | A dead `ovs-vswitchd` cuts every instance of a compute while Nova still shows them `ACTIVE` |
| **Ceph** (when used) | Shared storage for images, volumes and instance disks | A storage problem becomes a problem of every service using it |

## How a deployment tool fits in

OpenStack can be deployed with Kolla-Ansible (services in containers), OpenStack-Ansible, Charmed OpenStack, vendor
distributions or by hand. The services and what can go wrong with them are the same; what changes is where they run,
how they are restarted and where their logs are. Runbooks give the commands for the deployment methods their authors
know and mark them (`**Kolla-Ansible:**`, `**Any:**`). If yours is missing, adding it is a good first contribution.

## Go further

- Next on the newcomer path: the [glossary](glossary.md), for the words this page used without explaining.
- [openstack-vm-runbooks](https://github.com/OzarLand/openstack-vm-runbooks): what to do when one of these services lets an instance down.
- [kolla-ansible-deployment-patterns](https://github.com/OzarLand/kolla-ansible-deployment-patterns): how operators deploy these services, and the choices they made.
- Upstream: the [OpenStack documentation](https://docs.openstack.org/) and each project's administrator guide.
