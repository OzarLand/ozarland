# Runbook structure

A runbook starts from a symptom and leads to a verified resolution. Every runbook has the same sections, in the
same order, so that someone under pressure can find what they need without reading the whole page.

| Section | Content | Required |
|---|---|---|
| **Metadata** | Front matter, see [content metadata](content-metadata.md) | Yes |
| **Symptom** | What the operator or the user sees. Exact error messages, states, CLI output, as observed. | Yes |
| **Impact** | Who and what is affected, and how badly. Is the platform degraded, is data at risk, is it one instance or all of them. | Yes |
| **Quick checks** | The three to five read-only commands that confirm you are looking at this problem and not another one. | Yes |
| **Diagnosis** | How to narrow the cause: commands, logs to read, what to look for in them. Grouped by component. | Yes |
| **Possible causes** | The causes known to produce this symptom, each with how to tell it apart from the others. | Yes |
| **Resolution** | The steps that fix it, one subsection per cause. Every state-changing or destructive command carries its [risk warning](risk-warnings.md). | Yes |
| **Verification** | How to prove the problem is gone and nothing else broke: commands and expected output. | Yes |
| **Validity and limits** | Where this was observed, what was not tested, what is uncertain. | Yes |
| **Related** | Links to other runbooks, upstream bugs and documentation, discussions where this was investigated. | If any |
| **History** | Who wrote and confirmed it, with dates and releases, when the front matter is not enough. | Optional |

## Writing rules

- **Commands are copy-pasteable** and use placeholders in angle brackets: `openstack server show <server-id>`.
  Never real IDs, hostnames or addresses from your platform.
- **Show expected output** when the command's result is what the reader must interpret. Trim it to the relevant
  lines and mark the trimming with `...`.
- **Say where a command runs**: on the controller, on the compute node, inside a container
  (`docker exec -it nova_compute …`), with which credentials.
- **One cause, one fix.** If two causes have the same fix, say so explicitly instead of merging the sections.
- **Do not guess.** If you do not know why a fix works, write that. It is an invitation for someone to explain.
- **Prefer upstream vocabulary**: the names Nova, Neutron and the CLI use, not local nicknames.

## Deployment-specific steps

Steps that depend on the deployment method are marked with a label line:

```markdown
**Kolla-Ansible:** `docker restart nova_compute`
**OpenStack-Ansible:** `systemctl restart nova-compute` inside the container
**Any:** `openstack compute service set --enable <host> nova-compute`
```

A runbook written for one method is still welcome; mark the method in the front matter and leave the other
variants for someone else to add.

## Templates

- [`community/templates/runbook.md`](../../community/templates/runbook.md)
- [`community/templates/deployment-pattern.md`](../../community/templates/deployment-pattern.md)
- [`community/templates/upgrade-playbook.md`](../../community/templates/upgrade-playbook.md)
- [`community/templates/experience-report.md`](../../community/templates/experience-report.md)
