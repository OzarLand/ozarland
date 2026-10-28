#!/usr/bin/env python3
"""Regenerate the page-status badges, progress bars and counts in the OzarLand READMEs.

Usage:
    python3 status_blocks.py [--write] --hub <ozarland checkout> <repo-name>=<checkout path> [...]

Example, from a directory holding the three checkouts:
    python3 ozarland/tools/status_blocks.py --write --hub ozarland \\
        openstack-vm-runbooks=openstack-vm-runbooks \\
        kolla-ansible-deployment-patterns=kolla-ansible-deployment-patterns

Counts every page of each content repository by its `status:` front matter and by top-level folder, then
rewrites the blocks between `<!-- status-<name>:start -->` and `<!-- status-<name>:end -->` markers:
`badges` and `progress` in each content repository's README, `badges` and `progress` in the hub README, and
`summary` in the hub's docs/knowledge-lifecycle.md. Without --write, it only reports stale blocks and exits
with code 1, so it can run as a check. Text outside the markers is never touched.
"""
import argparse
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_content import is_page, parse_front_matter  # noqa: E402

STATUSES = ("lab-verified", "validated", "experimental", "draft")
SQUARES = {"validated": "🟦", "lab-verified": "🟩", "experimental": "🟧", "draft": "⬜"}
BADGE_COLORS = {"lab-verified": "16a34a", "draft": "9ca3af", "validated": "2563eb", "experimental": "d97706"}
PIE_COLORS = {"draft": "#d1d5db", "lab-verified": "#16a34a", "validated": "#2563eb", "experimental": "#d97706"}

# Display name of each repository in the hub, and of each folder in its own README.
REPOS = {
    "openstack-vm-runbooks": {
        "label": "🔧 VM runbooks",
        "what": "in the VM runbooks (runbooks and log-reading guides)",
        "short": "runbook",
        "folders": {"lifecycle": "🔄 Lifecycle", "scheduling": "📅 Scheduling", "migration": "🚚 Migration",
                    "networking": "🌐 Networking", "volumes": "💾 Volumes", "diagnostics": "🩺 Diagnostics",
                    "logs": "📜 Logs", "recovery": "🚑 Recovery"},
    },
    "kolla-ansible-deployment-patterns": {
        "label": "🏗️ Deployment patterns",
        "what": "in the deployment patterns",
        "short": "deployment-pattern",
        "folders": {"topologies": "🏗️ Topologies", "networking": "🌐 Networking", "storage": "💾 Storage",
                    "configuration": "🧾 Configuration", "services": "🧩 Services",
                    "deployment-errors": "🧯 Deployment errors", "operations": "⚙️ Operations",
                    "version-notes": "📌 Version notes", "comparisons": "⚖️ Comparisons"},
    },
}
# Sentences that hold only while no page is validated: flagged once a page is.
NONE_VALIDATED_CLAIMS = ("None is `validated` yet", "Nothing here has been confirmed on a production platform")


def count_pages(root):
    """Return {folder: Counter(status)} for every community page under root."""
    folders = defaultdict(Counter)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for name in sorted(filenames):
            rel = os.path.relpath(os.path.join(dirpath, name), root).replace(os.sep, "/")
            if not is_page(rel):
                continue
            with open(os.path.join(root, rel), encoding="utf-8") as f:
                fields, _ = parse_front_matter(f.read())
            status = (fields or {}).get("status")
            if status in STATUSES:
                folders[rel.split("/")[0]][status] += 1
    return folders


def total(counter_by_folder):
    t = Counter()
    for c in counter_by_folder.values():
        t.update(c)
    return t


def bar(c):
    """Ten squares, best status first; rounding is cumulative so the squares always add up to ten."""
    n, out, cumulative, used = sum(c.values()), "", 0, 0
    for status in ("validated", "lab-verified", "experimental"):
        cumulative += c[status]
        k = round(10 * cumulative / n) - used
        out += SQUARES[status] * k
        used += k
    return out + SQUARES["draft"] * (10 - used)


def verified(c):
    return c["lab-verified"] + c["validated"]


def legend(t, unit):
    names = {"validated": "validated", "lab-verified": "lab-verified", "experimental": "experimental", "draft": "draft"}
    shown = [f"{SQUARES[s]} {names[s]}" for s in ("validated", "lab-verified", "experimental", "draft") if t[s]]
    return f"<sub>{' · '.join(shown)} · one square is about 10 % of the {unit}'s pages</sub>"


def progress_table(rows, first_col):
    lines = [f"| {first_col} | Progress | Lab-verified or validated |", "|---|---|---:|"]
    for label, c in rows:
        lines.append(f"| {label} | {bar(c)} | {verified(c)} / {sum(c.values())} |")
    return "\n".join(lines)


def badges(t, extra=""):
    n = sum(t.values())
    out = [f'  <img src="https://img.shields.io/badge/pages-{n}-informational.svg" alt="{n} pages">']
    for status in ("lab-verified", "draft", "validated", "experimental"):
        if status in ("lab-verified", "draft", "validated") or t[status]:
            label = status.replace("-", "--")
            out.append(f'  <img src="https://img.shields.io/badge/{label}-{t[status]}-{BADGE_COLORS[status]}.svg" '
                       f'alt="{t[status]} {"page" if t[status] == 1 else "pages"} {status}">')
    return "\n".join(out) + extra


def status_sentence(t):
    present = [f"{t[s]} `{s}`" for s in STATUSES if t[s]]
    absent = [f"`{s}`" for s in ("validated", "experimental") if not t[s]]
    text = f"{sum(t.values())} pages, " + ", ".join(present)
    if absent:
        text += ", none " + " or ".join(absent)
    return text + "."


def pie(t):
    shown = sorted((s for s in STATUSES if t[s]), key=lambda s: -t[s])
    theme = ", ".join(f'"pie{i}": "{PIE_COLORS[s]}"' for i, s in enumerate(shown, 1))
    slices = "\n".join(f'    "{s}" : {t[s]}' for s in shown)
    return (f'```mermaid\n%%{{init: {{"theme": "base", "themeVariables": {{{theme}}}}}}}%%\n'
            f"pie showData\n    title Published pages by status\n{slices}\n```")


def repo_blocks(name, folders):
    conf = REPOS[name]
    order = list(conf["folders"]) + sorted(f for f in folders if f not in conf["folders"])
    rows = [(conf["folders"].get(f, f"📁 {f.replace('-', ' ').capitalize()}"), folders[f]) for f in order
            if folders.get(f)]
    t = total(folders)
    return {
        "badges": badges(t),
        "progress": (f"**Where things stand:** {status_sentence(t)}\n\n{progress_table(rows, 'Folder')}\n\n"
                     f"{legend(t, 'folder')}"),
    }


def hub_blocks(counts):
    t = Counter()
    for folders in counts.values():
        t.update(total(folders))
    n = sum(t.values())
    parts = [f"{sum(total(f).values())} {REPOS[name]['what']}" for name, f in counts.items()]
    rows = [(REPOS[name]["label"], total(f)) for name, f in counts.items()]
    statuses = ", ".join(f"{t[s]} {s}" for s in ("validated", "lab-verified", "draft", "experimental"))
    breakdown = " and ".join(f"{REPOS[name]['short']} ({sum(total(f).values())})"
                             for name, f in counts.items())
    return {
        "README.md": {
            "badges": badges(t),
            "progress": (f"{n} pages are published: {' and '.join(parts)}.\n\n{pie(t)}\n\n"
                         f"{progress_table(rows, 'Repository')}\n\n{legend(t, 'repository')}"),
        },
        "docs/knowledge-lifecycle.md": {
            "summary": (f"Today (counted from each page's `status:` field by `tools/status_blocks.py`): "
                        f"**{statuses}**, out of the {n} pages of the {breakdown} repositories."),
        },
    }


def apply(path, blocks, write, problems, validated):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    new = text
    for name, body in blocks.items():
        start, end = f"<!-- status-{name}:start -->", f"<!-- status-{name}:end -->"
        pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
        if not pattern.search(new):
            problems.append(f"{path}: missing markers {start} ... {end}")
            continue
        replacement = f"{start}\n{body}\n{end}"
        new = pattern.sub(lambda _, r=replacement: r, new)
    if validated:
        for claim in NONE_VALIDATED_CLAIMS:
            if claim in new:
                problems.append(f"{path}: says '{claim}' while {validated} page(s) are validated; update it by hand")
    if new != text:
        if write:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)
            print(f"updated: {path}")
        else:
            problems.append(f"{path}: status blocks are stale (run with --write)")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--hub", required=True, help="path of the ozarland checkout")
    parser.add_argument("--write", action="store_true", help="rewrite stale blocks instead of reporting them")
    parser.add_argument("repos", nargs="+", help="<repo-name>=<checkout path>")
    args = parser.parse_args()
    counts, problems = {}, []
    for spec in args.repos:
        name, _, path = spec.partition("=")
        if name not in REPOS or not path:
            parser.error(f"unknown repository or missing path: {spec} (known: {', '.join(REPOS)})")
        counts[name] = count_pages(path)
        validated = total(counts[name])["validated"]
        apply(os.path.join(path, "README.md"), repo_blocks(name, counts[name]), args.write, problems, validated)
    all_validated = sum(total(f)["validated"] for f in counts.values())
    for rel, blocks in hub_blocks(counts).items():
        apply(os.path.join(args.hub, rel), blocks, args.write, problems, all_validated)
    for p in problems:
        print(f"ERROR {p}")
    if not problems:
        print("status blocks up to date")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
