# Glossary

The words you will meet in runbooks and discussions, one line each. Missing a word? Adding it is a
`good first contribution`.

| Term | Meaning |
|---|---|
| **Agent** (Neutron) | A process on a host that applies Neutron's decisions there: Open vSwitch agent, L3 agent (routers), DHCP agent, metadata agent |
| **All-in-one** | A deployment where every service runs on a single host; for labs and learning, never for production |
| **Allocation** | The resources Placement has reserved for one instance on one host |
| **Allocation ratio** | How much of a resource Placement may hand out compared with what the host really has (overcommit), for CPU, RAM and disk |
| **Attachment** (volume) | Cinder's record that a volume is connected to an instance on a host; Nova keeps its own record of the same disk, and both must agree |
| **Availability zone** | A named group of hosts users can target; often a failure domain |
| **Boot from volume** | An instance whose root disk is a Cinder volume rather than a local disk on the compute |
| **Cell** (Nova cells v2) | A partition of Nova with its own database and message bus; every deployment has at least one, and every compute must be mapped to a cell |
| **Ceph RBD** | Ceph's block devices (RADOS Block Device), often used for Cinder volumes, Glance images and instance disks |
| **Cold migration** | Moving an instance to another host by stopping it first |
| **Compute (host)** | A host that runs instances: `nova-compute`, the hypervisor and the networking of the instances |
| **Conductor** (`nova-conductor`) | The Nova service that coordinates multi-step operations and talks to the database for the computes |
| **Control plane** | The APIs, schedulers, conductors, databases and message bus: what decides and records |
| **Controller** | A host that runs control-plane services |
| **CPU pinning** (dedicated CPUs) | Giving each vCPU of an instance its own host CPU (`hw:cpu_policy=dedicated` in the flavor) instead of sharing them |
| **Data plane** | The hypervisors, instance disks and network paths: what runs the workloads |
| **Deployment method** | How a platform was installed and is changed: Kolla-Ansible, OpenStack-Ansible, a distribution, by hand |
| **Destructive** (in a runbook) | A step that can lose data, interrupt workloads or cannot be undone; marked 🛑 |
| **DHCP agent** | The Neutron agent that gives instances their address on networks served by it (ML2/OVS); OVN answers DHCP itself |
| **Evacuation** | Rebuilding the instances of a dead compute on other hosts; only safe once the dead host is fenced |
| **Fencing** | Making sure a host is really off (power it down, cut it from the network) before taking over its workloads |
| **Fernet keys** | The keys Keystone uses to encrypt and validate tokens; they must be identical on every Keystone node |
| **Flavor** | The size of an instance: vCPUs, RAM, disk and extra properties |
| **Floating IP** | A public address mapped to an instance's private address by a Neutron router |
| **Front matter** | The YAML block at the top of an OzarLand page: release, components, deployment method, status, risk |
| **Galera** | The replication layer that turns MariaDB nodes into a cluster; needs a majority (quorum) to accept writes |
| **Gateway chassis** (OVN) | A host that carries a router's traffic to and from the external network; one is active per router, the others stand by |
| **`globals.yml`** | Kolla-Ansible's main configuration file: which services to enable, network interfaces, VIP, images; its secrets live apart in `passwords.yml` |
| **HAProxy** | The load balancer in front of the APIs on the controllers; with keepalived it answers on the VIP |
| **Host aggregate** | A group of computes with metadata, used by scheduler filters to send some flavors or images to some hosts |
| **Hypervisor** | The software that runs virtual machines; on most OpenStack computes, QEMU/KVM driven by libvirt |
| **Image** | The template an instance boots from, stored by Glance |
| **Instance** | A virtual machine (also called a server in the API) |
| **Inventory** (Ansible) | The file that lists the hosts and their groups (control, network, compute, storage); Kolla-Ansible deploys from it |
| **Kolla-Ansible** | A deployment tool that runs OpenStack services in containers, configured with Ansible |
| **L3 agent** | The Neutron agent that runs routers (ML2/OVS) |
| **Live migration** | Moving a running instance to another host with a brief pause |
| **LVM** (Cinder backend) | Volumes created as logical volumes on a storage host and exported to the computes, usually over iSCSI |
| **Metadata service** | The address (`169.254.169.254`) where an instance reads its SSH key, user data and hostname at boot |
| **Microversion** | A numbered version of a service's API; behaviour can change between microversions |
| **ML2** | Neutron's plugin framework; "ML2/OVS" means Neutron with the Open vSwitch agent, "ML2/OVN" with OVN |
| **MTU** | The largest packet a link carries; overlays (VXLAN, Geneve) take some of it, and mismatches drop large packets silently |
| **Multinode** | A deployment spread over several hosts: controllers, computes, sometimes network and storage hosts |
| **Network node** | A host that runs routers and their external traffic: L3, DHCP and metadata agents with ML2/OVS, a gateway chassis with OVN |
| **Northbound / southbound database** (OVN) | OVN's two databases: northbound holds the logical networks as Neutron wrote them, southbound what the hosts must apply |
| **`nova-manage`** | Nova's administration command; it works on the databases directly (cells, Placement audit, clean-up), not through the API |
| **NUMA** | The split of a host's CPUs and memory into nodes; Nova keeps a pinned instance's CPUs and memory within a node |
| **OVN** | A networking backend in which distributed controllers on each host replace most Neutron agents |
| **`ovn-controller`** | The OVN process on every host that reads the southbound database and programs the local Open vSwitch |
| **OVS** (Open vSwitch) | The virtual switch on each host that connects instances, tunnels and physical networks |
| **Placement** | The service that tracks resources and allocations so the scheduler knows where instances fit |
| **Port** | A Neutron object for one network interface: address, MAC, security groups, binding to a host |
| **Port binding** | The moment Neutron wires a port on a host; a failure leaves the instance stuck in BUILD |
| **Project** | A tenant: the unit that owns resources and quotas |
| **Provider network** | A network mapped directly to a physical network or VLAN, usually for external access |
| **ProxySQL** | A database proxy that Kolla-Ansible puts in front of MariaDB by default since 2025.1, in place of HAProxy, for database connections |
| **Quorum** | A majority of members; Galera and RabbitMQ quorum queues stop accepting work without it |
| **Quorum queue** | A RabbitMQ queue replicated on several nodes, available while a majority of them is up |
| **RabbitMQ partition** | A split of the RabbitMQ cluster into sides that cannot see each other; services stop agreeing |
| **Release** (series) | A six-month OpenStack version, named by year and number (2025.1, 2025.2, 2026.1...) |
| **Request id** | The identifier (`req-...`) an API request carries through every service's logs; the way to follow one failure |
| **Reset state** | `openstack server set --state ...`: changes only Nova's record of an instance, never the hypervisor; a last resort |
| **Resize** | Changing an instance's flavor; done as a cold migration that the user then confirms or reverts |
| **Resource provider** | Placement's name for something that has resources: a compute, a shared storage pool |
| **Runbook** | A page that goes from a symptom to a verified fix: checks, diagnosis, causes, resolution, verification |
| **Scheduler** (`nova-scheduler`) | The Nova service that picks a host for a new instance |
| **Security group** | Firewall rules attached to ports |
| **SLURP** | Skip Level Upgrade Release Process: every other release can be upgraded to directly from the previous SLURP release |
| **SR-IOV** | A network card that splits into virtual functions handed directly to instances, bypassing Open vSwitch |
| **State-changing** (in a runbook) | A step that changes the platform in a reversible or bounded way; marked ⚠️ |
| **Steal time** | Time a vCPU was ready to run but the host ran something else; shown as `st` in `top` inside the guest |
| **Tunnel network** (VXLAN, Geneve) | Tenant networks carried between hosts inside encapsulated packets |
| **VIF** | The virtual network interface of an instance; Nova waits for Neutron's `network-vif-plugged` event before finishing a boot |
| **VIP** | The virtual IP of the load balancer, held by one controller at a time and moved by keepalived |
| **`virsh`** | libvirt's command line on a compute: shows what the hypervisor really runs, whatever Nova's records say |
| **Volume** | A block device provided by Cinder, attached to an instance |

## Go further

- Next on the newcomer path: [how to read a runbook](how-to-read-a-runbook.md).
- [openstack-vm-runbooks](https://github.com/OzarLand/openstack-vm-runbooks): these words in context, in real diagnoses.
- [kolla-ansible-deployment-patterns](https://github.com/OzarLand/kolla-ansible-deployment-patterns): the deployment vocabulary in context.
