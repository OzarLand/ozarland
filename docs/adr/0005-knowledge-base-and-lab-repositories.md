# ADR-0005: Reproducible knowledge base and lab repositories

- **Status:** Superseded by [ADR-0008](0008-community-knowledge-sharing-space.md). Kept unchanged for the record; the content below describes the operator toolkit OzarLand was before it became a knowledge-sharing community.
- **Date:** 2026-10-07
- **Deciders:** @soufian-zaouam
- **Amends:** ADR-0004, item 5 (the lab repository was deferred; this ADR creates it).
- **Upstream check:** partly. Kolla Ansible provides the remediation commands (`mariadb-recovery`,
  `rabbitmq-reset-state`, `reconfigure`…), a `check` command and its documentation. Its CI runs one
  fault-and-recover test: a clean stop of the whole MariaDB cluster followed by `kolla-ansible mariadb-recovery`
  (`tests/test-mariadb.sh`), without diagnosis or functional checks. No upstream project keeps a catalogue of
  Kolla Ansible failures with an investigation, a fix and a reproduction for each. Prior art to evaluate for reuse
  in `ozar-lab`: os-faults, Rally, Tempest, Chaos Toolkit, and Kolla Ansible's own `check` and
  `tests/check-failure.sh`.

## Context

The scoping of `ozar-ops` (OzarLand/ozar-ops#3) concluded that its value is **encoded operational knowledge**: how
to investigate a failure on a Kolla Ansible platform, what causes it, and what to do about it. Two problems follow:

1. **Who writes and maintains that knowledge.** It comes from operators, and changes at a different pace from the
   engine that runs it. Keeping it inside `ozar-ops` would mix contributors who write investigations with
   contributors who write engine code, and tie every knowledge change to an engine release.
2. **How to know it is still true.** Log formats, API fields and even Kolla Ansible commands change between
   OpenStack series. Knowledge that is not tested becomes silently wrong. A diagnosis checked only against recorded
   data says nothing about whether the proposed fix works.

If every known failure can be **reproduced** on a lab, both the diagnosis and the fix can be checked
automatically, and checked again on every new series.

ADR-0004 requires an ADR for any new repository, showing a distinct audience, release cadence or trust level, and
it deferred a lab repository on purpose. This ADR makes that case for two repositories.

## Decision

### 1. Terms

| Term | Meaning |
|---|---|
| Case | One known failure, kept in one directory of `ozar-kb`: investigation, reproduction, remediation, verification |
| Investigation | The part of a case that `ozar-ops` runs: a path from a symptom to a conclusion, using probes only |
| Probe | A read-only, bounded observation implemented and reviewed as code in `ozar-ops` (container state, Galera status, tail of a log file within a time window…) |
| Result states | What an investigation returns, as defined by the `ozar-ops` roadmap: problem found, no problem found, unknown, not applicable |
| Qualification lab | A throw-away Kolla Ansible platform built by `ozar-lab` from versioned steps. Anyone with an OpenStack test environment can rebuild it; it does not depend on a specific company's infrastructure. It is not the operator's own lab or pre-production environment |
| Qualification | The automated loop of section 4, which proves a case on a given platform configuration |

### 2. The case is the unit of knowledge

A case is reviewed in one pull request and contains:

| Part | What it is | Where it may run |
|---|---|---|
| Investigation | From a symptom to a conclusion, through probes | Production and qualification lab, read-only |
| Reproduction | How to inject the failure on the qualification lab, and how to undo it | Qualification lab only |
| Remediation | The corrective action, preferably a Kolla Ansible command or a link to upstream documentation | Qualification lab: run automatically. Production: shown to a human, never run by OzarLand |
| Verification | What proves the failure is fixed (section 4) | Production and qualification lab, read-only |

Requirements on every case, which the case format decided in `ozar-kb` must meet:

- **Readable by a human as a runbook** (symptom, cause, action, links to upstream documentation), so the knowledge
  stays useful without `ozar-ops`.
- **Testable without a lab**, from recorded observations.
- **No free commands** in the investigation or the verification: only probes. Contributing a case is contributing
  data. A case that needs a new probe waits for that probe to be reviewed and merged in `ozar-ops`.
- **A remediation declares** its preconditions (for example "every MariaDB node is stopped"), whether it destroys
  data and what, its blast radius (one node, the whole cluster), and the points where a human must decide.

### 3. Reproduction is mandatory

A case enters `ozar-kb` only if its failure can be reproduced on the qualification lab, and its reproduction has
passed several runs in a row (the number is set by `ozar-lab`). A failure that nobody knows how to reproduce yet
stays an open issue, with its evidence, until a reproduction is found.

A case is merged only after review by a maintainer and a passing qualification.

### 4. Qualification

```text
known baseline ─► baseline checks ─► investigation ─► expected: no problem found  (no false finding)
                                         │
                                         ▼ reproduction
                            investigation ─► expected: this case's conclusion, with its evidence
                                         │
                                         ▼ remediation
                            verification ─► expected: fixed and stable (see below)
                                         │
                                         ▼ lab reset to the known baseline
```

- **Isolation.** Every qualification starts from a known baseline, checked by the first step. A case's own undo is
  never what guarantees isolation between cases; the reset mechanism is an `ozar-lab` decision.
- **"Unknown" fails.** On the healthy lab, "unknown" is not accepted as "no problem found".
- **Fixed means:** after a bounded wait, the investigation no longer concludes and stays so for a stated time; the
  service works (functional checks); resources created before the fault still exist and work; and no other case
  concludes. `ozar-kb` sets the numbers per case.
- **Three outcomes:** pass, fail, inconclusive. A failed baseline makes the run inconclusive, not the case.
  A case is marked as not valid only after repeated, reproducible failures, and a human reviews that marking.
- **Validity** is recorded per OpenStack series, Kolla Ansible version, image tag, base distribution, container
  engine and lab topology (for example Open vSwitch or OVN). `ozar-ops` runs a case only on a configuration where it
  is qualified, and returns "unknown: not qualified for this version" elsewhere.
- **When:** qualification runs when a case changes and when a new series is added; the schedule is an `ozar-lab`
  decision.
- **What it proves:** the automatic path, on a small lab. It does not prove behaviour at production scale, nor the
  other paths a human might choose at a decision point. The answers used at each decision point are recorded with
  the result.

### 5. Repositories

| Repository | Role | Audience | Release cadence | Trust level |
|---|---|---|---|---|
| `ozar-ops` | The engine: probes, investigation runner, report, verification | Operators running it | Engine releases | Runs in production, read-only |
| `ozar-kb` | The knowledge base: the cases | Operators who write and review cases | Whenever cases are added or re-qualified, independent of the engine | Data only; contains destructive reproductions that never reach production |
| `ozar-lab` | The qualification lab as code, execution of reproductions and remediations, qualification and its results | Contributors who maintain the lab and qualification | Follows OpenStack series and Kolla Ansible releases | Destructive by design; runs only against a qualification lab |

`ozar-lab` may also be used by `ozar-deploy` for its own tests; that is a possibility, not a commitment.
Each repository is created by an organization owner once this ADR is accepted, then bootstrapped like the existing
ones.

### 6. Trust levels

- **What `ozar-ops` receives** from `ozar-kb` leaves out the reproduction and remediation execution parts; it is
  not enough that `ozar-ops` does not load them. In production, `ozar-ops` shows the remediation to a human, with
  its declared preconditions and destructive effects, and, once the human has acted, runs the verification,
  read-only.
- **`ozar-lab` fails closed.** It runs reproductions and remediations only against a target it positively
  identifies as a qualification lab (an explicit lab marker and credentials valid only there), never by guessing
  from names. The same rule applies if `ozar-deploy` uses it.
- A contributed case cannot make `ozar-ops` run anything outside its probes.
- Running a remediation automatically in production is out of scope. Changing that requires a new ADR.

### 7. Not decided here

The case format, the probe vocabulary, the versioning contract between `ozar-ops` and `ozar-kb`, the lab
technology, the reset mechanism, the fault injection and functional verification tools, where results are
published, languages and tools. Each is decided by ADR in the repository concerned.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| Knowledge inside `ozar-ops` | One repository, no versioning contract | Mixes contributors and release rhythms; the knowledge base cannot be reused or contributed to on its own |
| **Separate `ozar-kb` and `ozar-lab` (chosen)** | Knowledge contributed and released on its own; destructive lab tooling kept apart from both the engine and the data | Three repositories for one maintainer; a versioning contract between engine and knowledge |
| `ozar-kb` and `ozar-lab` in one repository | One fewer repository | Mixes case authors with lab maintainers, the cadence of cases with the cadence of OpenStack series, and data with destructive tooling |
| Reproductions in their own repository | Strictest separation of destructive content | A case and its proof are split and reviewed separately |
| Reproduction optional, with qualification levels | Accepts failures that are hard to reproduce | Unproven knowledge in the base; no automatic re-qualification on a new series |
| Recorded evidence only, no lab | Cheap | Cannot prove that a fix works; cannot re-qualify a case on a new series |
| Improve upstream documentation only | No new repository | Documentation is not executable or tested against real failures; OzarLand still reports generic gaps upstream |

## Consequences

Positive:

- Every case in `ozar-kb` is proven: the diagnosis finds the failure, and the fix restores service without losing
  what existed before the fault.
- Keeping cases valid across series becomes an automated result, reviewed by a human, instead of manual
  maintenance.
- Remediations that rely on Kolla Ansible commands also qualify those commands series by series; failures found
  this way are reported upstream.
- Operators can contribute knowledge without writing engine code and without being able to run arbitrary commands
  in production.

Negative:

- `ozar-kb` will be smaller: failures that cannot be reproduced on a lab (hardware faults, kernel bugs, slow leaks,
  effects of scale) stay out until someone finds a reproduction.
- Mandatory reproduction biases the catalogue toward failures that are easy to break. Cases must be chosen from
  real incidents first, and the reproduction found second.
- The qualification lab is a prerequisite for any case. It needs an OpenStack test environment; without nested
  virtualisation, cases involving instances fall back to slow emulation. A multinode deployment takes long to
  rebuild, and snapshots of clustered services across several VMs are only consistent if the VMs are stopped or
  quiesced first. `ozar-lab` must solve this within the isolation rule of section 4.
- Timing-dependent failures (partitions, split-brain) are hard to reproduce reliably; some may never meet the
  "several runs in a row" rule.
- A single maintainer now has three repositories to keep consistent, and a versioning contract between `ozar-ops`
  probes and `ozar-kb` cases.
- Automating remediation in the lab will create pressure to automate it in production; section 6 and a new ADR are
  the answer.

Follow-ups, in order:

1. An organization owner creates `ozar-kb` and `ozar-lab`; each gets a bootstrap pull request.
2. `ozar-ops` decides the probe vocabulary and the versioning contract with `ozar-kb` by ADR.
3. `ozar-kb` decides the case format and the contribution rules by ADR.
4. `ozar-lab` decides the lab technology, lab target identification, the reset mechanism, and the fault injection
   and functional verification tools, after checking the prior art listed above.
5. The `ozar-ops` roadmap (OzarLand/ozar-ops#4) relies on this ADR and points to those ADRs; it is merged after
   this ADR is accepted. Roadmaps for `ozar-kb` and `ozar-lab` follow.
6. The README of this repository lists the new projects once the repositories exist.

## Validation

- The first 3 to 5 cases pass qualification end to end on one OpenStack series.
- Within one release cycle, the same cases are qualified on the next series; those that no longer pass are marked
  automatically, and a human confirms the marking.
- At least one case written by someone other than the maintainer passes qualification without any change to
  `ozar-ops`.
