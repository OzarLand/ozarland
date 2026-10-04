# Security policy

## Reporting a vulnerability

**Do not open a public issue for a security problem.**

- **While OzarLand repositories are private:** contact the maintainers directly through the organization owner on GitHub.
- **Once repositories are public:** use GitHub private vulnerability reporting ("Report a vulnerability" in the Security tab). This policy will be updated with a dedicated contact address before any repository becomes public.

Please include the affected component and version, reproduction steps and the impact you observed.
Never include secrets, real inventories, IP addresses or customer data in a report.

## What to expect

- Acknowledgement within 5 business days, triage within 10.
- Coordinated disclosure, with a default embargo of 90 days.
- Credit in the advisory unless you prefer to stay anonymous.
- Fixes are published as GitHub Security Advisories, with a CVE when applicable.

## Scope

OzarLand code, container images, release artefacts and documentation.

Vulnerabilities in **Kolla, Kolla Ansible or OpenStack** must be reported upstream to the
[OpenStack Vulnerability Management Team](https://security.openstack.org/). We will help route them.

## Supported versions

OzarLand is pre-release (0.x). Until a first release exists, only `main` is supported.
