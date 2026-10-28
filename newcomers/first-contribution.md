# Your first contribution

You do not need to be an expert to contribute. Some of the most useful contributions come from people who are
learning: they see what is unclear, what is missing, and which word nobody explained.

## Ten-minute contributions

- **Ask a question** in the Q&A discussions. A good question with context (release, deployment method, what you
  checked) is a contribution. [Start a discussion](start-a-discussion.md) shows how, step by step.
- **Report a gap**: a runbook that did not match what you saw, a command that failed, a word you had to look up.
  Open a *Documentation proposal* issue.
- **Confirm a page**: you ran the read-only checks of a runbook on your platform and they behaved as written. Say so
  on the page's repository with your release and deployment method. This is how pages move towards `validated`.

## Your first pull request, step by step

1. **Pick a task.** Look for issues labelled **`good first contribution`** in the OzarLand repositories. Each says
   what to do, in which file, and what "done" means. Comment on the issue to say you are taking it.
2. **Open the file on GitHub** and use the pencil icon ("Edit this file"). The web editor is enough for every
   `good first contribution` task; no local setup needed. GitHub creates a branch and signs off your commit for you.
3. **Follow the conventions** of the page you edit:
   - metadata block at the top: release, components, deployment method, status
     ([content metadata](../docs/conventions/content-metadata.md));
   - a new page starts from a template in [`community/templates/`](../community/templates/);
   - no secrets, real hostnames, addresses or names ([sensitive data](../docs/conventions/sensitive-data.md));
   - state-changing steps get ⚠️, destructive ones 🛑 ([risk warnings](../docs/conventions/risk-warnings.md)).
4. **Open the pull request.** Fill in the template: what you changed, the release and deployment method you checked
   it on, or "not tested" if you did not. Honest is better than complete.
5. **Review.** An operator reviewer (an AI agent, with the maintainer behind it) reads every pull request, usually within a few
   days, and says what is fine and
   what needs changing; maintainers and other contributors may comment too. Changes requested are normal and are not
   a judgement on you: push a fix, or reply if you think the reviewer is wrong.
6. **Merge.** Clear and safe content pull requests are merged once the review passes. Your name stays in the history
   of the page.

If you prefer the command line: fork or clone, branch, edit, `git commit -s`, push, and open the pull request. You can
run the same checks as the reviewer before pushing:

```bash
python3 tools/check_content.py --root <your clone> <files you changed>
```

(The script is in the `ozarland` repository.)

## If you get stuck

Comment on the issue or the pull request and say where you are stuck. Someone will answer. Nobody is expected to know
how everything works, including the people who wrote the runbooks.

## Go further

- [Start a discussion](start-a-discussion.md): ask, share an experience or compare approaches.
- Open tasks: [`good first contribution` across OzarLand](https://github.com/search?q=org%3AOzarLand+label%3A%22good+first+contribution%22+state%3Aopen&type=issues).
- [openstack-vm-runbooks](https://github.com/OzarLand/openstack-vm-runbooks): confirm a runbook, add a variant for your deployment method, or share a problem you solved.
- [kolla-ansible-deployment-patterns](https://github.com/OzarLand/kolla-ansible-deployment-patterns): describe how you deploy.
- [CONTRIBUTING.md](../CONTRIBUTING.md): the full rules, short on purpose.
