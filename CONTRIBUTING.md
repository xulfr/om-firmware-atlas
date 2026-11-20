# Contribute to the Atlas

Bring a useful source, correction, project or test result. You can open an issue using the intake forms, or ask an agent to read [AGENTS.md](AGENTS.md), follow the ingestion workflow and raise a PR. [How the Atlas works](docs/how-it-works.md) explains the whole route, with a worked example and copyable agent prompts.

## Steps

1. Create a branch from `main`, using your own GitHub account and commit identity.
2. Change facts in `records/`, explanations in `knowledge/` and site pages in `docs/`. Never hand-edit the generated `views/` or `agents/routes/`.
3. Regenerate, check, test and build (commands below). Read the affected pages in `site/`.
4. Commit the generated changes with your edits and open a PR using the template.
5. Wait for the **Atlas validation** check to pass, keep the branch up to date with `main` and resolve review conversations. A maintainer reviews and merges. Agents must not approve or merge.

## What belongs here

Sourced camera/project records, precise observations, explanations of shared research, tool setup references, contribution destinations and community discovery links. Contribute implementation changes to their upstream project. The Atlas does not host firmware, decoded images, executable research tools or whole chat transcripts.

**No repositories that distribute firmware.** The Atlas does not list, cite or link a repository that publishes camera firmware: a stock or modified update file, a decoded or expanded firmware image, or a dump of part of one, on any branch or tag or as a release asset. Card data files (looks, settings), hashes, edit lists, and builders that download the official file on the user's own machine are fine. Check before writing any records; if a listed project starts publishing firmware, remove its listing. See [decision 0008](maintenance/decisions/0008-no-firmware-repos.md).

Read [the record format](maintenance/record-format.md) before changing data. Record what a source establishes, its target and its limitations. Missing evidence means unknown, not failure. A new version does not inherit an older package's camera results. Preserve failures when later packages succeed.

For a source URL, inspect the relevant release, branch, issue/comment or report; a README alone may miss the work. Compare with existing records before adding content. Pin repository sources to a commit; identify mutable comments/releases by URL, date and content digest when useful. Attribute interpretations and proposals to their authors.

## Community information

Add venues to `records/community/` with their scope, public link, listing basis, sources and last check. Keep broad photography forums distinct from project-specific spaces. A venue's existence or invite does not establish the activity, endorsement or claims of its members. Use a particular post or message as the source of a technical finding.

Private discussions require explicit permission for the information being published. Summarise the useful finding with provenance; do not copy personal details or entire conversations. No unsolicited contact is part of the agent workflow.

## Validate and submit

```sh
python scripts/atlas.py generate
python scripts/atlas.py check
python -m unittest discover -s tests -v
python scripts/atlas.py build
```

Inspect affected pages in `site/`, or download the PR's `atlas-preview` artifact ([how](docs/how-it-works.md#inspecting-a-prs-site-preview)). A PR includes sources/revisions, changed assertions, gaps/conflicts, human pages affected and checks performed. Generated diffs belong in the same PR. Changes to schemas, routing or policy include appropriate regression cases and a decision record when consequential.

PRs and a passing **Atlas validation** check are required to change `main`. Another person's approval is not required: maintainers can review and merge their own PRs. Agents never approve or merge. Avoid unrelated formatting or importing an entire upstream knowledge base. Original contributions follow [LICENSE](LICENSE); linking to an external work does not change its terms.
