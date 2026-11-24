# Maintain the Atlas

The scripts maintain documentation only. Python 3.10+ and `requirements.txt` are the complete application dependencies. Use an isolated environment. No vendor firmware, camera access or upstream development toolchain is needed.

Contributors use their own GitHub accounts and commit identities through GitHub's normal repository permissions. The Atlas has no custom author allowlist or authentication hooks. Choose your preferred public name and email in your own Git configuration.

## Making the next change easier

Before changing a shared rule, trace one real example from its canonical record through validation, generation and the pages that consume it. Read the decision that established the boundary. Ask what the next camera, release or conflicting report would require someone to edit.

Prefer an improvement that removes a real source of error in the current task. If two pages disagree about a release, make them use the same model-specific selection rule. If a record correction solves the problem for every page, the correction is enough. Introduce a new abstraction when actual callers share the same rule and its exceptions can be tested.

In the PR, explain which future change is easier or which mistake is now caught. Show the example and the check that demonstrates it. Record a lasting architectural trade-off in a decision when it changes a repository boundary. If a wider improvement needs a separate decision, describe it briefly with evidence and keep the current change focused.

## Commands

```sh
python scripts/atlas.py generate
python scripts/atlas.py check
python -m unittest discover -s tests -v
python scripts/atlas.py build
python scripts/atlas.py route --job research --camera om5-ii --topic emulation
python scripts/atlas.py freshness --fetch
```

`check` validates schemas, identity/reference semantics, dependencies, local links, generated drift and fixed routing cases. `build` validates and builds MkDocs strictly from an ignored staging tree. The generator builds the camera directories, owner showcases and per-camera research pages. The site also fills the camera finders, the recent research list and the homepage counts and project showcase from the records. The showcase takes each project's first image for one camera (its `camera_id`, or the project's only camera), newest release first. [Navigation decision](decisions/0007-direct-owner-and-developer-routes.md). `generate` writes only Atlas-owned `views/` and `agents/routes/`; do not edit those files manually. Costs are UTF-8 bytes and `ceil(bytes / 4)` approximate tokens, not measured model usage.

Read [record format](record-format.md) for canonical data and [the implementation plan](plan.md) for scope and remaining improvements. [Decisions](decisions/0001-foundation.md) record why the library is built this way.

## Publication and review

PR checks use read-only repository access. The main workflow validates, tests, builds and publishes GitHub Pages using the `github-pages` environment. The site displays its source commit and publication time. Only `main` and manual runs on `main` can publish. Scheduled freshness checks create a report and update-queue artifact, open or refresh one `atlas-update-queue` issue (the job's only write permission), and rebuild the main site so age notices advance; they never change factual records.

The initial setup was explicitly authorised to push to main. Normal agent contributions raise PRs; humans review and merge. Agents never approve or merge. Main requires a PR, passing **Atlas validation**, an up-to-date branch and resolved conversations, including for administrators. Another person's approval is not required, so maintainers can merge their own PRs after reviewing them. Force pushes and branch deletion are blocked. CODEOWNERS provides ownership and review routing without mandatory code-owner approval. Branch protection is a repository setting, not something AGENTS.md can enforce. [How the Atlas works](../docs/how-it-works.md) explains this for contributors.

## Scope of verification

Routing cases verify deterministic selection, order, excluded bulk reads and estimated cost. They do not prove that every external coding agent obeys the instructions. Perform representative client smoke checks when changing the entry contract. Site builds validate links/structure, not the truth of free prose. Inspect rendered pages when changing content/layout and attach preview evidence to a PR.

Freshness reports distinguish unchanged, changed, unavailable and unsupported comparison. They do not mutate review dates. Keep reports in CI artifacts or `.build/`, not as edited historical logs. Substantive changes still need an agent/human review and a PR.


On pull requests, Atlas validation also opens the built site in Chromium at desktop and phone widths. To run the same journeys locally, build the site, install the optional test dependency with `python -m pip install playwright==1.62.0`, run `python -m playwright install chromium`, then `python tests/browser_smoke.py`. The install-guide click is intercepted locally.
