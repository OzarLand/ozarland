# Security policy

## What this policy covers

OzarLand repositories contain documentation, runbooks and occasional scripts contributed by OpenStack operators.
Two kinds of security issues can arise:

1. **Sensitive data published by mistake**: a secret, a real hostname or address, an unredacted log, anything that
   identifies an infrastructure or a person. See [sensitive data](https://github.com/OzarLand/ozarland/blob/main/docs/conventions/sensitive-data.md).
2. **Unsafe procedures**: a runbook or script whose steps could cause data loss or an outage without the warning
   required by [risk warnings](https://github.com/OzarLand/ozarland/blob/main/docs/conventions/risk-warnings.md), or a procedure that weakens the security of an
   OpenStack platform (for example by disabling authentication or exposing a service).

## How to report

**Do not open a public issue or discussion for either case.**

Use GitHub private vulnerability reporting: "Report a vulnerability" in the Security tab of the repository
concerned. Only you and the maintainers see the report. If the Security tab does not offer it, message the
organization owner on GitHub. OzarLand has no e-mail contact.

Questions, errors in a page and proposals that involve nothing sensitive go in a GitHub issue. Anything about the
code of conduct or a personal matter follows the [code of conduct](CODE_OF_CONDUCT.md#reporting).

Tell us which repository and page, what you found, and, for an unsafe procedure, what could go wrong. Do not
include the sensitive data itself in the report beyond what is needed to locate it.

## What to expect

- Acknowledgement within 5 business days.
- Sensitive data is removed promptly. If a secret was exposed, the contributor is contacted so they can rotate it,
  and the history is rewritten if needed.
- Unsafe procedures are corrected or marked `status: experimental` with a warning until they are fixed.
- Credit to the reporter in the fix, unless they prefer to stay anonymous.

## Vulnerabilities in OpenStack itself

A vulnerability in OpenStack, Kolla, Kolla-Ansible or another upstream project is reported to the
[OpenStack Vulnerability Management Team](https://security.openstack.org/), not here. We will help route it if you
are unsure. Content in OzarLand that describes a workaround for a published upstream vulnerability links to the
upstream advisory.
