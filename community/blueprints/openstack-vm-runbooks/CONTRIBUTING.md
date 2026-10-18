# Contributing

This repository follows the OzarLand community contribution guide:
[CONTRIBUTING.md in `ozarland`](https://github.com/OzarLand/ozarland/blob/main/CONTRIBUTING.md).

In short:

1. Give context: OpenStack release, components, deployment method, environment conditions, what you checked.
2. No sensitive data: no secrets, real hostnames, domains, IP or MAC addresses, customer or person names,
   unredacted logs ([how to redact](https://github.com/OzarLand/ozarland/blob/main/docs/conventions/sensitive-data.md)).
3. Flag risky commands: ⚠️ state-changing, 🛑 destructive
   ([risk warnings](https://github.com/OzarLand/ozarland/blob/main/docs/conventions/risk-warnings.md)).
4. Say where it was observed; never present a procedure as universal.
5. Use the templates in `templates/`, open a pull request, sign off your commits (`git commit -s`).

Repository-specific notes:

<!-- Anything specific to this repository: directory to use, naming of pages, extra fields. Keep it short. -->
- Put the page in the directory of its primary symptom (`lifecycle/`, `scheduling/`, `migration/`, `networking/`,
  `volumes/`, `recovery/`); cross-cutting investigation guides go in `diagnostics/`.
- Name the file after the symptom, lowercase, hyphenated: `instance-stuck-in-build-waiting-for-vif-plugged.md`.
- Add the page to the index table in `README.md` in the same pull request.
