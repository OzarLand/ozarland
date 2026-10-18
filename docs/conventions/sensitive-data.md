# Sensitive data

OzarLand repositories are, or will be, public. Content describes real platforms, which makes it easy to leak things
that must not be published. These rules apply to pages, issues, discussions, pull requests and comments alike.

## Never publish

- **Secrets:** passwords, tokens, API keys, private keys, certificates, Kolla `passwords.yml`, Keystone
  credentials, Ceph keyrings, database credentials, even "test" ones.
- **Infrastructure identifiers:** real hostnames, FQDNs, domains, public or private IP addresses, MAC addresses,
  VLAN IDs tied to a real network plan, serial numbers, asset tags.
- **Organisational identifiers:** customer, employer, project or tenant names; team or person names other than
  your own GitHub handle; internal ticket numbers; internal URLs.
- **Unredacted logs and command output.** Logs contain all of the above. Redact before pasting.
- **Topology at a level that identifies a platform:** "three controllers and twenty computes" is fine; a rack
  diagram with real names is not.
- **Personal data** of users of the platform, including usernames in instance names or project names.

## How to redact

| Instead of | Write |
|---|---|
| Real hostnames | `controller-1`, `compute-07`, `ceph-mon-2`, or `<controller>` |
| Real domains | `example.org`, `cloud.example.com` ([RFC 2606](https://www.rfc-editor.org/rfc/rfc2606)) |
| Real IPv4 addresses | `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24` ([RFC 5737](https://www.rfc-editor.org/rfc/rfc5737)) |
| Real IPv6 addresses | `2001:db8::/32` ([RFC 3849](https://www.rfc-editor.org/rfc/rfc3849)) |
| Real UUIDs | `<server-id>`, or a visibly fake UUID such as `00000000-0000-4000-8000-000000000001` |
| Real MAC addresses | `fa:16:3e:00:00:01` (the OpenStack prefix with an obviously fake suffix) |
| Project and user names | `<project>`, `demo`, `admin` |
| Employer or customer | "a telecom operator", "a public research cloud", or nothing |

Keep what makes the content useful: the error message text, the sequence of events, the relevant configuration
keys and their non-secret values, the timings.

## Before you submit

The pull request and issue templates ask you to confirm:

- [ ] No secrets, credentials or keys.
- [ ] No real hostnames, domains, IP or MAC addresses.
- [ ] No customer, employer, project or person names.
- [ ] Logs and command output are redacted.

Maintainers will ask for redaction before reviewing anything else. If something sensitive is merged by mistake,
tell a maintainer privately (see [SECURITY.md](../../SECURITY.md)); removing it requires rewriting history and
rotating any exposed secret, and the sooner it is done the better.
