#!/usr/bin/env python3
"""Report which topics the OzarLand community repositories cover.

Usage:
    python3 coverage_report.py --topics docs/topics.yml <repo-name>=<checkout path> [...]
        [--pending <repo-name>=<checkout path of a pull request head> ...] [--format markdown|json]

For each repository: pages per topic with their status, components and releases mentioned, topics with no
page yet. Pages found only in --pending checkouts are reported as "in review".
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_content import is_page, parse_front_matter  # noqa: E402

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def load_topics(path):
    if yaml is None:
        sys.exit("PyYAML is required to read the topics file")
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def scan(root):
    pages = {}
    for d, dirs, names in os.walk(root):
        dirs[:] = [x for x in dirs if x != ".git"]
        for n in names:
            rel = os.path.relpath(os.path.join(d, n), root)
            if not is_page(rel):
                continue
            fields, _ = parse_front_matter(open(os.path.join(root, rel), encoding="utf-8").read())
            fields = fields or {}
            def as_list(v):
                return [str(x) for x in v] if isinstance(v, list) else ([str(v)] if v else [])
            pages[rel] = {
                "path": rel,
                "topic": rel.split(os.sep)[0] if os.sep in rel else "(root)",
                "title": str(fields.get("title", rel)),
                "kind": str(fields.get("kind", "")),
                "status": str(fields.get("status", "")),
                "risk": str(fields.get("risk", "")),
                "components": as_list(fields.get("components")),
                "releases": as_list(fields.get("openstack_releases")),
                "confirmations": len(fields.get("confirmed_by") or []),
            }
    return pages


def parse_pairs(values):
    out = {}
    for v in values or []:
        name, _, path = v.partition("=")
        out.setdefault(name, []).append(path)
    return out


def build(topics, repos, pending):
    report = {}
    for name, paths in repos.items():
        merged = {}
        for p in paths:
            merged.update(scan(p))
        in_review = {}
        for p in pending.get(name, []):
            for rel, page in scan(p).items():
                if rel not in merged:
                    page["status"] = "in review"
                    in_review[rel] = page
        allpages = list(merged.values()) + list(in_review.values())
        repo_topics = topics.get(name, {})
        rows = []
        for tid, t in repo_topics.items():
            tp = sorted([p for p in allpages if p["topic"] == tid], key=lambda p: p["title"])
            rows.append({"topic": tid, "label": t.get("label", tid), "pages": tp})
        extra = sorted({p["topic"] for p in allpages} - set(repo_topics))
        for tid in extra:
            rows.append({"topic": tid, "label": tid, "pages": [p for p in allpages if p["topic"] == tid]})
        statuses = {}
        for p in allpages:
            statuses[p["status"]] = statuses.get(p["status"], 0) + 1
        report[name] = {
            "pages": len(merged),
            "in_review": len(in_review),
            "statuses": statuses,
            "components": sorted({c for p in allpages for c in p["components"]}),
            "releases": sorted({r for p in allpages for r in p["releases"]}),
            "topics": rows,
            "uncovered": [r["label"] for r in rows if not r["pages"]],
        }
    return report


def markdown(report):
    out = []
    for name, r in report.items():
        out.append(f"## {name}\n")
        st = ", ".join(f"{k}: {v}" for k, v in sorted(r["statuses"].items())) or "none"
        out.append(f"{r['pages']} published page(s), {r['in_review']} in review. Status: {st}.\n")
        out.append("| Topic | Pages | Titles (status) |\n|---|---|---|")
        for t in r["topics"]:
            titles = "<br>".join(f"{p['title']} ({p['status']})" for p in t["pages"]) or "none yet"
            out.append(f"| {t['label']} | {len(t['pages'])} | {titles} |")
        out.append("")
        if r["components"]:
            out.append(f"Components covered: {', '.join(r['components'])}.\n")
        if r["releases"]:
            out.append(f"Releases mentioned: {', '.join(r['releases'])}.\n")
        if r["uncovered"]:
            out.append("Not covered yet: " + "; ".join(r["uncovered"]) + ".\n")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--topics", required=True)
    ap.add_argument("--pending", action="append", default=[])
    ap.add_argument("--format", choices=["markdown", "json"], default="markdown")
    ap.add_argument("repos", nargs="+", help="<repo-name>=<checkout path>")
    a = ap.parse_args()
    report = build(load_topics(a.topics), parse_pairs(a.repos), parse_pairs(a.pending))
    print(json.dumps(report, indent=2, ensure_ascii=False) if a.format == "json" else markdown(report))


if __name__ == "__main__":
    main()
