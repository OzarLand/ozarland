# ADR-0007: Marked candidates in ozar-ops for lab trials only

- **Status:** Accepted
- **Date:** 2026-10-11
- **Deciders:** @soufian-zaouam
- **Amends:** [ADR-0006](0006-candidate-cases-in-ozar-kb.md): its "Read by `ozar-ops`" column for `candidates/`,
  the mitigation in its options table, the second item of its consequences and its validation. ADR-0006 is not
  edited; everything else in it stands.
- **Upstream check:** no. Kolla Ansible has no notion of a case, a candidate or a qualification. This decides what
  `ozar-ops` may accept as input on a lab; nothing it runs on a platform changes.

## Context

ADR-0006 says that `ozar-ops` reads `candidates/` of `ozar-kb` "Never". It relies on that to mitigate the risk that
a reader takes a candidate for a proven case, and its validation is "`ozar-ops` never loads a file from
`candidates/`".

Two uses now need `ozar-ops` to run on candidates:

- **The qualification loop of `ozar-lab`** (ADR-0005, section 4). A candidate becomes a case only once qualified,
  and qualification runs the investigation of `ozar-ops`. With "Never", no candidate can be qualified, and
  `cases/` stays empty.
- **A lab-only trial** of `ozar-ops` by an operator. While `cases/` is empty, a run checks nothing.

The maintainer decided on 2026-10-10 to allow a lab-only trial on candidates
([OzarLand/ozar-ops#130](https://github.com/OzarLand/ozar-ops/issues/130)), and on 2026-10-11 to take a reduced
path to the qualification loop of `ozar-lab` (its milestone L5) that runs `ozar-ops` on candidates. `ozar-kb`
ADR-0002 is already narrower than ADR-0006: "`ozar-ops` never reads `candidates/` in production".

## Decision

`ozar-ops` never reads `candidates/` in production, never by default and never as shipped: its embedded bundle
holds `cases/` only.

For the qualification loop of `ozar-lab` and for a lab-only trial, `ozar-ops` may load a bundle built from
`candidates/`, on these conditions:

- **Explicit build.** Only an explicit build mode of `ozar-ops` reads `candidates/`. It copies what the normal build
  copies, and never the reproduction or remediation execution parts (ADR-0005, section 6, unchanged).
- **Marked.** The mandatory `COMMIT` file of such a bundle reads `candidates <sha>`. A bundle cannot lose the mark
  without losing a file the loader requires, and a loader that does not know the mark refuses the bundle.
- **Explicit opt-in at run time.** `ozar-ops` refuses a candidates bundle unless the run passes `--lab-trial`.
- **Reported on every output.** A banner in the text report, `bundle_source` set to `candidates` in the JSON report,
  and a warning on standard error.
- **Never embedded.** The embedded bundle never contains a candidate; the build, the loader and the checks of
  `ozar-ops` refuse it.

The details are decided in `ozar-ops`
[ADR 0017](https://github.com/OzarLand/ozar-ops/blob/main/docs/adr/0017-lab-trial-bundle-from-candidates.md)
(being merged at the date of this ADR).

What this changes in ADR-0006:

| ADR-0006 text | Now reads |
|---|---|
| `candidates/`, "Read by `ozar-ops`": Never | Never in production, by default or as shipped; a marked bundle on a lab, with explicit opt-in |
| Mitigation: "`ozar-ops` never reading `candidates/`" | See below |
| "`ozar-ops` reads `cases/` only" | `ozar-ops` reads `cases/` only, except a marked lab-trial bundle; the versioning contract still covers `cases/` only |
| "`ozar-ops` never loads a file from `candidates/`" | See Validation |

The risk that a reader takes a candidate for a proven case is now mitigated by:

1. the warning on every page of `candidates/` (ADR-0006, unchanged);
2. candidates never reaching production: never shipped, never loaded by default;
3. the explicit opt-in, at build time and again at run time;
4. the marking of the bundle and of every output of a run on it.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| **Marked candidates bundle, lab only, explicit opt-in** (chosen) | Candidates can be qualified with the probes that will run them; operators can try `ozar-ops` now; production and the shipped bundle unchanged | The mitigation now rests on marking and opt-in, not on absence; a deliberate hand edit of `COMMIT` can remove the mark |
| Keep "Never" | ADR-0006 unchanged | No candidate can be qualified, so `cases/` stays empty and `ozar-ops` checks nothing |
| `ozar-lab` copies candidates into a fake `cases/` | No change in `ozar-ops` | Unqualified drafts run unmarked: the confusion ADR-0006 guards against |
| Qualify candidates without `ozar-ops` | `ozar-ops` never touches candidates | Qualifies commands, not the probes that will run in production; duplicates the investigation |

## Consequences

- `ozar-lab` can run its qualification loop on candidates, and operators can try `ozar-ops` on a lab.
- `ozar-ops` gains a build mode, a run flag and a report field; their tests guard the rules above.
- **Residual risk:** someone who edits `COMMIT` by hand can turn a candidates bundle into an unmarked one. That is a
  deliberate act, not a mistake; the embedded bundle stays protected by the build, the loader and the checks.
- The bar for `cases/` does not move (ADR-0005, section 3).
- Running remediations, or anything outside the probes, is still out of scope (ADR-0005, section 6).

## Validation

- No file under `cases/` of `ozar-kb` is unqualified (ADR-0006, unchanged).
- `ozar-ops` never loads a file from `candidates/` without the explicit lab-trial opt-in.
- The embedded bundle of `ozar-ops` never contains a file from `candidates/`.
- On the qualification lab, every report of a run on a candidates bundle carries the banner and
  `"bundle_source": "candidates"`.
