# Shared community files

Everything a new OzarLand community repository needs, ready to copy. Keeping these files in one place keeps the
repositories consistent without a heavy process.

| Directory | Content | How to use |
|---|---|---|
| [`repo-template/`](repo-template/) | README skeleton, short CONTRIBUTING pointer, GitHub issue forms, pull request template, discussion category forms | Copy the whole directory into a new repository, then fill the README placeholders |
| [`templates/`](templates/) | Document templates: runbook, deployment pattern, upgrade playbook, experience report | Copy the one you need to start a new page |
| [`blueprints/`](blueprints/) | Initial README, directory layout and first-content list for each planned repository | Use when creating the repository; the README is meant to ship as is |

## Creating a repository from these files

```bash
# from a fresh clone of the new, empty repository
cp -r <ozarland>/community/repo-template/. .
cp -r <ozarland>/community/blueprints/<repo-name>/. .      # overwrites README.md with the blueprint's
cp <ozarland>/LICENSE .                                     # Apache-2.0 for code
cp <ozarland>/CODE_OF_CONDUCT.md <ozarland>/SECURITY.md .
mkdir -p templates && cp <ozarland>/community/templates/<relevant templates> templates/
git add . && git commit -s -m "Bootstrap <repo-name> from the OzarLand community template"
```

Then, on GitHub: enable Discussions, create the categories listed in
[docs/github-conventions.md](../docs/github-conventions.md), apply the shared labels, set the description and topics
from the blueprint, and add the repository to the directory in the main README.

When these shared files change, the change is proposed here first and then propagated to the other repositories.
A public `.github` organization repository can later host the issue and discussion forms centrally, which removes
the need to copy them.
