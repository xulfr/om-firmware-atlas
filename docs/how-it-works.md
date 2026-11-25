# How the Atlas works

The Atlas is a set of files in a GitHub repository, plus a few Python scripts that check those files and turn them into this website. Anyone can propose a change. People and AI agents follow the same route: change the source files, let the checks run, open a pull request and wait for a human to merge it.

This page explains that route for contributors. To send a link or correction, [choose an issue form, copy an agent prompt or prepare a PR](add.md).

**A few terms used below**

- **Repository (repo):** the project's files and their history, hosted on GitHub.
- **Pull request (PR):** a proposed set of changes that others can read, discuss and merge into the main version.
- **Merge:** accept a PR so that its changes become part of the `main` branch, which is what gets published.
- **CI (continuous integration):** checks that GitHub runs automatically on every PR.
- **Artifact:** a file that a CI run saves for you to download, such as a preview of the built site.
- **Schema:** a machine-readable description of which fields a record must have and which values each field may contain.

## Where things live

| Folder or file | What it holds | Notes |
|---|---|---|
| `records/` | **Canonical records**: the facts, in structured YAML. Cameras, firmware, projects, capabilities, evidence, sources, community venues and the technical reference. | Edit these to change a fact |
| `knowledge/` | Explanations of shared research topics, such as firmware identity or emulation. | Edit freely, with sources |
| `docs/` | Site pages like this one: the home page, the evidence guide and contribution help. | Edit freely |
| `views/` | **Generated pages**: the camera, project, firmware, evidence and source pages you browse on this site. | Never edit by hand |
| `agents/` | Instructions for AI agents: jobs, roles, workflows, and reading routes in `agents/routes/`. | `agents/routes/` is generated |
| `AGENTS.md` | The short entry point that every agent reads first. | Kept deliberately small |
| `schemas/`, `taxonomy/` | Rules for record fields, and the allowed topic and feature names. | Policy files |
| `scripts/`, `tests/` | The checker, generator, site builder and their tests. | Tooling |
| `maintenance/` | Record format, decisions and routing test cases. | Maintainer reference |

The [CODEOWNERS](https://github.com/xulfr/om-firmware-atlas/blob/main/.github/CODEOWNERS) file names the repository owner as the reviewer for the agent instructions, schemas, taxonomy, scripts, workflows and decisions. It routes review requests; it does not make the owner's approval mandatory.

"Canonical" means this is the one place a fact is stored. Pages that show the fact are built from it, so a correction made once appears everywhere. The [record format](https://github.com/xulfr/om-firmware-atlas/blob/main/maintenance/record-format.md) lists the fields for each kind of record.

## How agents find what to read

The library is larger than an agent should read at once. The entry point is deliberately small, and it points to only what a given task needs.

1. **[AGENTS.md](../AGENTS.md)** sets the ground rules: where facts live, what must not be done, and how changes are submitted.
2. **[agents/start.md](../agents/start.md)** asks the agent to pick a **job**: research a camera, add a source or technical-reference fact, update a test result, refresh sources or add a release, improve a page or find discussion spaces.
3. Each job maps to one **role** and, where needed, one **workflow**. The mapping is in [agents/jobs.yaml](../agents/jobs.yaml).
4. The agent then reads only the **route** for the relevant camera, project or topic. Routes are short generated files in `agents/routes/` that list what to read next, with its size and an estimated token cost.

The optional command `python scripts/atlas.py route` prints the same reading plan. For example, a request to add a release of Caduceus for OM-5:

```text
python scripts/atlas.py route --job ingest --source https://github.com/xulfr/caduceus-om5/releases/tag/v0.1.0-alpha12

AGENTS.md | 1390 bytes | ~348 tokens
agents/start.md | 1279 bytes | ~320 tokens
agents/roles/librarian.md | 904 bytes | ~226 tokens
agents/workflows/ingest-source.md | 1918 bytes | ~480 tokens
agents/routes/projects/caduceus-om5.md | 985 bytes | ~247 tokens
```

The command prints a reading list; it does not answer the question or change any files.

### The three roles

- **[Researcher](../agents/roles/researcher.md)** answers questions. It pins down the exact camera, firmware and task before applying anything. It keeps reports, code findings, emulator runs and real-camera results separate, and checks existing projects before suggesting new work.
- **[Librarian](../agents/roles/librarian.md)** turns sources into records. It extracts only what is new, reuses existing records, and keeps provenance, scope, missing details and failures. It never simply prefers the newest text when sources conflict.
- **[Editor](../agents/roles/editor.md)** improves pages for people. It writes for a camera owner who has not seen the agent's conversation, defines terms and avoids blanket "safe" or "supported" labels.

The roles are written for agents, but they work as a checklist for people too.

## A worked example: from a source URL to the live site

This example is illustrative. It follows the [source ingestion workflow](../agents/workflows/ingest-source.md).

1. **A contributor brings a source.** Someone opens an issue with the source form, or asks an agent to add the URL (see the [prompts below](#copyable-prompts)).
2. **Identify it exactly.** For a repository, the agent or contributor records the specific commit. For a release or comment, they record its URL and date, plus a fingerprint of the text (a SHA-256 digest) where that helps later checks. They look at releases, branches, issues and reports, not just the README. They do not run the project's code or binaries.
3. **Check what already exists.** Follow the project or camera route, read the affected record files, and look for an open PR that already covers the source.
4. **Synthesise the useful part.** Decide whether the source is new, confirms an existing record, corrects one, contradicts one, or adds nothing. Keep the exact camera, firmware and build. Keep limitations and failures. Keep the date of the report separate from the date of the test.
5. **Update records.** Add a `source` record and update or add `evidence`, `capability` or `project` records. For example, an owner report becomes an `evidence` record with `method: physical-camera`, its own `outcome`, and `quality: partial` if steps, hashes or a test date are missing.
6. **Generate.** Run `python scripts/atlas.py generate`. This rewrites the affected pages in `views/` and routes in `agents/routes/`.
7. **Validate.** Run the checks, tests and build listed under [Contributing](#contributing-locally). Then open the built pages and read them as a visitor would.
8. **Open a PR.** Describe the sources and revisions, which claims changed, what is still missing or in conflict, which pages are affected and which checks ran. The [PR template](https://github.com/xulfr/om-firmware-atlas/blob/main/.github/pull_request_template.md) asks for exactly this.
9. **CI and human review.** GitHub runs the same checks and attaches a preview of the built site. A maintainer reviews the PR and decides whether to merge it. Agents never approve or merge.
10. **Publication.** Merging into `main` runs the checks again, rebuilds the site and publishes it to GitHub Pages. The footer of every page shows the commit it was built from.

Sometimes the right outcome is no content change, because the source only repeats what is already recorded. A small record that shows its gaps is better than a guessed result.

## What the checks catch

`python scripts/atlas.py check` runs these checks. CI runs them on every PR.

- **Shape:** every record matches its schema, IDs are unique, and each record sits in the right folder.
- **References:** every ID a record points to exists and is the right kind of record.
- **Scope:** evidence must match the camera, firmware, project and build of the capability it supports. Firmware must belong to the camera it is used with.
- **Honest evidence:** a report cannot be marked `complete` without its package hash, steps and test date. An expected hash from a release manifest cannot stand in for one that was reported or observed. A test date cannot fall after the report date.
- **Sourcing:** every non-source record needs at least one source. GitHub file sources must be pinned to a full commit.
- **Generated pages:** the files in `views/` and `agents/routes/` must match what the generator would produce right now.
- **Links:** local Markdown links must point to real files.
- **Routing:** fixed test cases in [maintenance/routing-cases](https://github.com/xulfr/om-firmware-atlas/blob/main/maintenance/routing-cases/cases.yaml) must produce the expected reading lists. Each list must stay under a token budget and must not pull in bulk or unrelated files.
- **No binaries:** firmware images, archives and research databases are refused in `records/` and `knowledge/`.
- **Technical reference limits:** one entry per build and address, pinned sources, an upstream detail link, short text, and no disassembly, byte dumps or code. See [the reference policy](https://github.com/xulfr/om-firmware-atlas/blob/main/maintenance/reference-policy.md).

`python scripts/atlas.py build` repeats the checks and then builds the site in strict mode, which also fails on broken site structure.

### Examples of rejected changes

These are real messages from the checker:

| Change | Result |
|---|---|
| Editing a generated camera page by hand | `Generated drift: views/cameras/om3.md; run python scripts/atlas.py generate and commit the result.` |
| Moving an original OM-5 failure report onto the OM-5 Mark II | `capability.om5-prealpha1-start: evidence.om5-prealpha1-boot has different camera_id; select matching evidence or narrow the assertion.` |
| Marking a report `complete` when no test date is known | `evidence.om5-prealpha1-boot: complete physical report requires tested_on; mark quality partial if unknown.` |
| Linking a GitHub file on `main` instead of a fixed commit | `source.om3.readme: pin github-file URL and revision to the same full 40-character commit.` |
| Removing the only source from an evidence record | `evidence.om5-prealpha1-boot: add a source_refs entry; do not publish an unsourced assertion.` |
| Adding a link to a page that does not exist | `docs/about.md: broken local link missing.md; fix the target or add its canonical file.` |

### What the checks cannot tell you

- **Passing checks do not make a claim true.** The checker confirms that records are complete, consistent and sourced. It cannot tell whether a source is accurate, whether the prose summarises it fairly, or whether a reporter's account is right.
- **Nothing here establishes that firmware is safe.** A published release, an emulator run and an owner's report are different kinds of information. None of them is a safety guarantee for your camera. Read [how to interpret evidence](evidence.md).
- **Routing tests do not prove that agents behave.** They confirm that the routing script picks the right files for fixed example requests. They cannot make any particular AI agent read those files or follow the instructions. Human review exists for this reason.
- **The catalogue is incomplete.** A missing entry means "not catalogued yet", not "does not exist" or "does not work".

## How generated pages stay in step with records

The camera, project, firmware, capability, evidence, source and community pages under `views/`, and the agent routes under `agents/routes/`, are built from `records/`, `taxonomy/` and the metadata of `knowledge/` guides.

- `generate` is the only supported way to change those files. It refuses to write anywhere else and removes generated files whose records no longer exist.
- `check` re-renders everything in memory and compares it with the committed files. Any difference, including a hand edit or a forgotten `generate`, is reported as **drift** and fails CI.
- Generated changes are committed in the same PR as the record change, so reviewers can see both the data and its effect on the pages.
- At build time, the site builder adds a "Source review due" notice to record pages whose oldest linked source was last checked more than 30 days before publication. This notice exists only in the built site, not in the committed files.
- The site fills in the home page camera finder and the Community page’s maintainer list at build time. The Cameras directory shows recent releases from the project records and links to the TruePic overview.

### Project showcase pages

Each project page is built from its project record. Besides the research fields, a record can carry:

- a one-line **tagline** and a few paragraphs of **description**, written from the project's own documentation;
- **goals**, **maintainers** and useful **links** such as an install guide or web tool;
- **features**, each with the cameras it covers, a status (available, beta, alpha, testing, in development, planned or research) and, where the Atlas holds one, a link to its scoped evidence;
- **releases**, newest first, with highlights and any warning from the release notes;
- **images**, with a caption and credit. Only use images the project's maintainers have agreed to share.

Every feature and release cites a source record. Features are described as the project describes them; the Atlas's own evidence stays separate. The checks reject a feature or release that names a camera the project doesn't cover, releases out of date order, and missing images. Camera pages gather the features of every modification that covers that camera, then list its projects in two groups, mods and ports, and research, tools and references. Each card says what the project has for that camera and where to get it: the newest release naming the camera, or the project's guide. Where that isn't clear from the features and releases, for example a project listed for one failed test build, an optional **camera note** in the project record says it in a sentence or two.

## The weekly freshness check

Every Monday at 06:17 UTC, GitHub runs the Atlas workflow on a schedule.

**What it does automatically:**

- Runs `python scripts/atlas.py freshness --fetch`, which compares each source with its current upstream state without running any upstream code. It reports one of several states for each source, for example:
    - `file-changed`: a pinned repository file differs at the head of its branch (the default branch, or the branch or tag the source names in `tracked_ref`); `file-unchanged` means the repository moved but that file did not, and `file-missing` that it moved or was removed
    - `new-release`: the releases page lists a newer release, including test versions
    - `text-changed`: the notes of the pinned release, or a comment, differ from the recorded fingerprint; `release-missing` means that release is no longer published
    - `thread-updated`: an issue or pull-request thread has had activity since the last check
    - `reachable`: a non-GitHub link answered
    - `check-failed`: the check could not complete
- Compares each project's newest GitHub release with the releases on its showcase page, and flags any that aren't listed yet.
- Writes an **update queue** (`python scripts/atlas.py queue`): new releases to add, changed sources to review and reviews that are due, with a ready-made prompt for an agent.
- Opens a GitHub issue labelled `atlas-update-queue`, or refreshes the one already open, with that queue.
- Saves the report and the queue as a `source-review` artifact, kept for 30 days.
- Revalidates and republishes the current `main` site, so "Source review due" notices reflect the new publication date.

**What it never does:** change records, update review dates, open PRs, call an AI model or contact anyone. A new release puts a project in the queue; it does not appear on the site until someone has read its notes and a PR has been merged.

**What needs an agent or a person:** working through the queue issue. Hand its prompt to an agent, or follow the [freshness workflow](../agents/workflows/review-freshness.md) yourself: read each new release's notes, add it to the project's releases and features, review changed sources, update `last_reviewed` dates only after reviewing the facts, and open a PR. A successful link check alone does not renew a review date.

## Branch rules and review

These are the current rules for `main`:

- **Changes reach `main` through a PR**, including changes by administrators. Force pushes and branch deletion are blocked.
- **The Atlas validation check must pass** before a PR can merge.
- **The PR branch must be up to date with `main`, and review conversations must be resolved.**
- **Another person's approval is not required.** Maintainers, including the repository owner, can review and merge their own PRs.
- **Agents must not approve or merge.** They open PRs and stop there. This is an instruction in `AGENTS.md`, not something GitHub enforces on its own.

Contributors use their own GitHub accounts and choose their own commit name and email. The Atlas has no custom identity checks ([decision 0003](https://github.com/xulfr/om-firmware-atlas/blob/main/maintenance/decisions/0003-contributor-access.md)).

## Inspecting a PR's site preview

Every PR's CI run saves the built site so reviewers can see the result before merging. Pull requests never publish to the live site.

1. Open the PR on GitHub and select the **Checks** tab, then the **Atlas** workflow run.
2. On the run's **Summary** page, scroll to **Artifacts** and download **atlas-preview-…** (the name ends with the commit ID). You must be signed in to GitHub. Previews are kept for 7 days.
3. Unzip it.

Opening the files directly in a browser breaks links and search, so serve the folder locally:

```sh
python -m http.server 8000 --directory path/to/unzipped-preview --bind 127.0.0.1
```

Then visit `http://127.0.0.1:8000/`. The footer shows the commit the preview was built from. Check the pages the PR says it affects, on a narrow window as well as a wide one.

## Copyable prompts

Give these to an AI coding agent that can access the repository. Replace the capitalised placeholder.

**Add a source**

```text
Read AGENTS.md and follow agents/start.md in xulfr/om-firmware-atlas.
Add this source: SOURCE_URL.
Inspect the relevant releases, branches, issues and reports, not only the README, and do not run its code.
Synthesise only the useful change, update the relevant records and human pages, and keep missing details visible.
Regenerate, run the checks, tests and build, inspect the affected pages, and open a focused PR for human review.
Do not approve or merge it.
```

[Use the Atlas with your AI](research-with-ai.md) has a research prompt, a worked example and a follow-up prompt for contributing your findings.

## Contributing locally

You need Python 3.10 or newer. In a virtual environment:

```sh
python -m pip install -r requirements.txt
python scripts/atlas.py generate
python scripts/atlas.py check
python -m unittest discover -s tests -v
python scripts/atlas.py build
```

The built site is in `site/`. The [contribution steps](https://github.com/xulfr/om-firmware-atlas/blob/main/CONTRIBUTING.md) list what a PR should include. Maintainers will find commands and policy detail in [maintenance](https://github.com/xulfr/om-firmware-atlas/blob/main/maintenance/README.md).

## Implemented now, and planned

**Implemented now:** structured records with schemas and scope checks, a per-build technical reference (addresses, hazards, platform facts and built-in features), generated camera and project showcase pages and agent routes, drift detection, fixed routing tests, strict site builds, PR previews, the weekly source and release check with its update-queue issue, and publication from `main`.

**Planned or possible later** (from the [implementation plan](https://github.com/xulfr/om-firmware-atlas/blob/main/maintenance/plan.md); none of these exist yet):

- Deeper feature-level evidence for the OM-3 and E-P7.
- Exact input hashes for firmware entries that currently record only a version.
- More camera bodies and community venues, added through ordinary source PRs.
- Optionally starting an agent automatically from the weekly update-queue issue. Today a maintainer hands the issue's prompt to an agent, or works through it by hand.
