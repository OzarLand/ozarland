# Glossary

The words you will meet in runbooks and discussions, one line each. Missing a word? Adding it is a
`good first contribution`.

| Term | Meaning |
|---|---|
| **Agent** (Neutron) | A process on a host that applies Neutron's decisions there: Open vSwitch agent, L3 agent (routers), DHCP agent, metadata agent |
| **Allocation** | The resources Placement has reserved for one instance on one host |
| **Allocation ratio** | How much of a resource Placement may hand out compared with what the host really has (overcommit), for CPU, RAM and disk |
| **Availability zone** | A named group of hosts users can target; often a failure domain |
| **Boot from volume** | An instance whose root disk is a Cinder volume rather than a local disk on the compute |
| **Cell** (Nova cells v2) | A partition of Nova with its own database and message bus; every deployment has at least one, and every compute must be mapped to a cell |
| **Cold migration** | Moving an instance to another host by stopping it first |
| **Compute (host)** | A host that runs instances: `nova-compute`, the hypervisor and the networking of the instances |
| **Conductor** (`nova-conductor`) | The Nova service that coordinates multi-step operations and talks to the database for the computes |
| **Control plane** | The APIs, schedulers, conductors, databases and message bus: what decides and records |
| **Controller** | A host that runs control-plane services |
| **Data plane** | The hypervisors, instance disks and network paths: what runs the workloads |
| **Deployment method** | How a platform was installed and is changed: Kolla-Ansible, OpenStack-Ansible, a distribution, by hand |
| **Destructive** (in a runbook) | A step that can lose data, interrupt workloads or cannot be undone; marked 🛑 |
| **DHCP agent** | The Neutron agent that gives instances their address on networks served by it (ML2/OVS); OVN answers DHCP itself |
| **Evacuation** | Rebuilding the instances of a dead compute on other hosts; only safe once the dead host is fenced |
| **Fencing** | Making sure a host is really off (power it down, cut it from the network) before taking over its workloads |
| **Fernet keys** | The keys Keystone uses to encrypt and validate tokens; they must be identical on every Keystone node |
| **Flavor** | The size of an instance: vCPUs, RAM, disk and extra properties |
| **Floating IP** | A public address mapped to an instance's private address by a Neutron router |
| **Galera** | The replication layer that turns MariaDB nodes into a cluster; needs a majority (quorum) to accept writes |
| **Hypervisor** | The software that runs virtual machines; on most OpenStack computes, QEMU/KVM driven by libvirt |
| **Image** | The template an instance boots from, stored by Glance |
| **Instance** | A virtual machine (also called a server in the API) |
| **Kolla-Ansible** | A deployment tool that runs OpenStack services in containers, configured with Ansible |
| **L3 agent** | The Neutron agent that runs routers (ML2/OVS) |
| **Live migration** | Moving a running instance to another host with a brief pause |
| **Metadata service** | The address (`169.254.169.254`) where an instance reads its SSH key, user data and hostname at boot |
| **Microversion** | A numbered version of a service's API; behaviour can change between microversions |
| **ML2** | Neutron's plugin framework; "ML2/OVS" means Neutron with the Open vSwitch agent, "ML2/OVN" with OVN |
| **MTU** | The largest packet a link carries; overlays (VXLAN, Geneve) take some of it, and mismatches drop large packets silently |
| **OVN** | A networking backend in which distributed controllers on each host replace most Neutron agents |
| **OVS** (Open vSwitch) | The virtual switch on each host that connects instances, tunnels and physical networks |
| **Placement** | The service that tracks resources and allocations so the scheduler knows where instances fit |
| **Port** | A Neutron object for one network interface: address, MAC, security groups, binding to a host |
| **Port binding** | The moment Neutron wires a port on a host; a failure leaves the instance stuck in BUILD |
| **Project** | A tenant: the unit that owns resources and quotas |
| **Provider network** | A network mapped directly to a physical network or VLAN, usually for external access |
| **Quorum** | A majority of members; Galera and RabbitMQ quorum queues stop accepting work without it |
| **Quorum queue** | A RabbitMQ queue replicated on several nodes, available while a majority of them is up |
| **RabbitMQ partition** | A split of the RabbitMQ cluster into sides that cannot see each other; services stop agreeing |
| **Release** (series) | A six-month OpenStack version, named by year and number (2025.1, 2025.2, 2026.1...) |
| **Request id** | The identifier (`req-...`) an API request carries through every service's logs; the way to follow one failure |
| **Resource provider** | Placement's name for something that has resources: a compute, a shared storage pool |
| **Runbook** | A page that goes from a symptom to a verified fix: checks, diagnosis, causes, resolution, verification |
| **Scheduler** (`nova-scheduler`) | The Nova service that picks a host for a new instance |
| **Security group** | Firewall rules attached to ports |
| **SLURP** | Skip Level Upgrade Release Process: every other release can be upgraded to directly from the previous SLURP release |
| **State-changing** (in a runbook) | A step that changes the platform in a reversible or bounded way; marked ⚠️ |
| **Tunnel network** (VXLAN, Geneve) | Tenant networks carried between hosts inside encapsulated packets |
| **VIF** | The virtual network interface of an instance; Nova waits for Neutron's `network-vif-plugged` event before finishing a boot |
| **VIP** | The virtual IP of the load balancer, held by one controller at a time and moved by keepalived |
| **Volume** | A block device provided by Cinder, attached to an instance |
