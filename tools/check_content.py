#!/usr/bin/env python3
"""Check OzarLand community pages against the shared content conventions.

Usage:
    python3 check_content.py --root <repository> [file ...]

Without files, every page of the repository is checked. With files (paths relative to the root, for
example the files changed by a pull request), only those are checked. Exit code 1 if any error is found.

Checks: front matter fields and values, required sections per kind, risk markers consistent with the
declared risk, validated pages carrying confirmations, relative links, and sensitive data (IP and MAC
addresses outside the documentation ranges, secrets). It does not judge technical accuracy: that is
the reviewer's job.
"""
import argparse
import ipaddress
import os
import re
import sys

# Files that are not community pages.
NON_PAGES = {"README.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "LICENSE", "CHANGELOG.md"}
NON_PAGE_DIRS = {".github", ".claude", "templates", "tools", "docs", "community"}

KINDS = {"runbook", "pattern", "playbook", "experience-report", "diagnostic", "comparison"}
STATUSES = {"draft", "lab-verified", "validated", "experimental"}
RISKS = {"read-only", "state-changing", "destructive"}
REQUIRED_FIELDS = {
    "runbook": ["title", "kind", "status", "openstack_releases", "components", "deployment_methods", "risk", "confirmed_by", "last_verified"],
    "diagnostic": ["title", "kind", "status", "openstack_releases", "components", "deployment_methods", "risk", "last_verified"],
    "pattern": ["title", "kind", "status", "openstack_releases", "components", "deployment_methods", "confirmed_by", "last_verified"],
    "playbook": ["title", "kind", "status", "openstack_releases", "components", "deployment_methods", "risk", "confirmed_by", "upstream_refs", "last_verified"],
    "comparison": ["title", "kind", "status", "openstack_releases", "components", "deployment_methods", "last_verified"],
    "experience-report": ["title", "kind", "openstack_releases", "components", "deployment_methods", "last_verified"],
}
REQUIRED_SECTIONS = {
    "runbook": ["Symptom", "Impact", "Quick checks", "Diagnosis", "Possible causes", "Resolution", "Verification", "Validity and limits"],
    "diagnostic": ["Validity and limits"],
    "pattern": ["Context", "Key choices and their consequences", "Lessons learned", "Validity and limits"],
    "playbook": ["Upgrade path", "Prerequisites and pre-checks", "Procedure", "Rollback", "Validity and limits"],
    "comparison": ["Validity and limits"],
    "experience-report": ["Context", "What happened", "What we learned"],
}
DOC_NETS = [ipaddress.ip_network(n) for n in ("192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24", "2001:db8::/32")]
ALLOWED_IPS = {"0.0.0.0", "127.0.0.1", "255.255.255.255", "169.254.169.254"}  # metadata service address is generic
SECRET_PATTERNS = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key block"),
    (re.compile(r"(?i)\b(password|passwd|secret|token)\s*[:=]\s*['\"]?(?!<)[A-Za-z0-9+/_\-]{8,}"), "credential-looking assignment"),
    (re.compile(r"\bgAAAAA[A-Za-z0-9_\-]{40,}"), "Fernet token"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key"),
    (re.compile(r"\bAQ[A-Za-z0-9+/]{36,}==?"), "Ceph keyring secret"),
]
IPV4 = re.compile(r"(?<![\w.])(\d{1,3}(?:\.\d{1,3}){3})(?:/\d{1,2})?(?![\w.])")
MAC = re.compile(r"\b([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5})\b")


def parse_front_matter(text):
    """Return (fields, body). Fields maps top-level keys to raw values (str or list of str)."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    block, body = text[4:end], text[end + 4:]
    try:
        import yaml  # optional
        data = yaml.safe_load(block)
        if isinstance(data, dict):
            return data, body
    except Exception:
        pass
    fields, key = {}, None
    for line in block.splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2).split(" #")[0].strip()
            if value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                fields[key] = [v.strip() for v in inner.split(",")] if inner else []
            else:
                fields[key] = value if value else []
        elif key and re.match(r"^\s+-\s", line) and isinstance(fields.get(key), list):
            fields[key].append(line.strip()[2:])
    return fields, body


def is_page(rel):
    parts = rel.split(os.sep)
    if not rel.endswith(".md") or parts[-1] in NON_PAGES:
        return False
    return not any(p in NON_PAGE_DIRS for p in parts[:-1])


def code_free(body):
    return re.sub(r"```.*?```", "", body, flags=re.S)


def check_page(root, rel):
    errors, warnings = [], []
    text = open(os.path.join(root, rel), encoding="utf-8").read()
    fields, body = parse_front_matter(text)
    if fields is None:
        return [f"{rel}: no front matter (see docs/conventions/content-metadata.md)"], []

    kind = str(fields.get("kind", ""))
    if kind not in KINDS:
        errors.append(f"{rel}: kind '{kind}' is not one of {sorted(KINDS)}")
        kind = "runbook"
    for f in REQUIRED_FIELDS[kind]:
        if f not in fields:
            errors.append(f"{rel}: front matter field '{f}' is missing")
    status = str(fields.get("status", ""))
    if "status" in fields and status not in STATUSES:
        errors.append(f"{rel}: status '{status}' is not one of {sorted(STATUSES)}")
    risk = str(fields.get("risk", ""))
    if "risk" in fields and risk not in RISKS:
        errors.append(f"{rel}: risk '{risk}' is not one of {sorted(RISKS)}")
    for f in ("openstack_releases", "components", "deployment_methods"):
        if f in fields and not fields[f]:
            errors.append(f"{rel}: '{f}' is empty")
    releases = [str(r) for r in (fields.get("openstack_releases") or [])]
    if any(r.strip().lower() in ("latest", "master", "any") for r in releases):
        errors.append(f"{rel}: openstack_releases must name releases, not 'latest', 'master' or 'any'")
    if any(r.strip().lower() == "unrecorded" for r in releases):
        warnings.append(f"{rel}: openstack_releases is 'unrecorded'; add the release when known")
    confirmed = fields.get("confirmed_by") or []
    if status == "validated" and not confirmed:
        errors.append(f"{rel}: status is 'validated' but confirmed_by is empty; a page is validated by someone other than its author")
    def entry_type(e):
        return str(e.get("type", "operator")) if isinstance(e, dict) else ("lab" if "type: lab" in str(e) else "operator")
    types = [entry_type(e) for e in confirmed]
    if status == "lab-verified" and "lab" not in types:
        errors.append(f"{rel}: status is 'lab-verified' but no confirmed_by entry has type: lab")
    if status == "validated" and confirmed and all(t == "lab" for t in types):
        errors.append(f"{rel}: status is 'validated' but every confirmation is a lab check; validated needs an operator confirmation")

    headings = {h.strip() for h in re.findall(r"^##\s+(.+)$", body, flags=re.M)}
    for section in REQUIRED_SECTIONS[kind]:
        if not any(h == section or h.startswith(section) for h in headings):
            errors.append(f"{rel}: required section '## {section}' is missing for kind '{kind}'")

    if risk == "destructive" and "🛑" not in body:
        errors.append(f"{rel}: risk is 'destructive' but no 🛑 warning appears in the page")
    if risk == "state-changing" and "⚠️" not in body and "🛑" not in body:
        errors.append(f"{rel}: risk is 'state-changing' but no ⚠️ warning appears in the page")
    if "🛑" in body and risk != "destructive":
        errors.append(f"{rel}: the page contains a 🛑 warning, so risk must be 'destructive' (it is '{risk}')")
    if "⚠️" in body and risk == "read-only":
        errors.append(f"{rel}: the page contains a ⚠️ warning, so risk cannot be 'read-only'")

    prose = code_free(body).lower()
    if re.search(r"officially supported|is supported upstream|supported upgrade path", prose) and "http" not in prose:
        warnings.append(f"{rel}: claims an upgrade path or behaviour is supported without any upstream link")
    return errors, warnings


def check_sensitive(root, rel):
    errors = []
    text = open(os.path.join(root, rel), encoding="utf-8", errors="replace").read()
    for n, line in enumerate(text.splitlines(), 1):
        if "http://" in line or "https://" in line:
            line = re.sub(r"https?://\S+", "", line)
        for m in IPV4.finditer(line):
            ip = m.group(1)
            try:
                addr = ipaddress.ip_address(ip)
            except ValueError:
                continue  # version strings such as 1.2.3.4567 are not addresses
            if ip in ALLOWED_IPS or any(addr in net for net in DOC_NETS):
                continue
            errors.append(f"{rel}:{n}: IP address {ip} is not in a documentation range (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24)")
        for m in MAC.finditer(line):
            mac = m.group(1).lower()
            if not mac.startswith("fa:16:3e:00:00"):
                errors.append(f"{rel}:{n}: MAC address {mac} looks real; use fa:16:3e:00:00:NN")
        for pattern, label in SECRET_PATTERNS:
            if pattern.search(line):
                errors.append(f"{rel}:{n}: possible secret ({label})")
    return errors


def check_links(root, rel):
    errors = []
    text = open(os.path.join(root, rel), encoding="utf-8").read()
    for target in re.findall(r"\]\(([^)\s]+)\)", text):
        path = target.split("#")[0]
        if not path or path.startswith(("http://", "https://", "mailto:")):
            continue
        if not os.path.exists(os.path.normpath(os.path.join(root, os.path.dirname(rel), path))):
            errors.append(f"{rel}: relative link '{target}' does not resolve")
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".", help="repository root")
    ap.add_argument("files", nargs="*", help="files to check, relative to the root (default: all)")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    if args.files:
        files = [f for f in args.files if os.path.exists(os.path.join(root, f))]
    else:
        files = []
        for d, dirs, names in os.walk(root):
            dirs[:] = [x for x in dirs if x != ".git"]
            files += [os.path.relpath(os.path.join(d, n), root) for n in names]

    errors, warnings, pages = [], [], 0
    for rel in sorted(files):
        if rel.endswith((".md", ".yml", ".yaml", ".txt", ".cfg", ".conf", ".ini", ".sh", ".py", ".j2")):
            errors += check_sensitive(root, rel)
        if rel.endswith(".md"):
            errors += check_links(root, rel)
        if is_page(rel):
            pages += 1
            e, w = check_page(root, rel)
            errors += e
            warnings += w

    for line in errors:
        print(f"ERROR   {line}")
    for line in warnings:
        print(f"WARNING {line}")
    print(f"\n{pages} page(s) and {len(files)} file(s) checked: {len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
