# A source URL to a PR

Preconditions: Atlas checkout, applicable entry contract, documentation dependencies, source read access and GitHub branch/PR access. Use [CONTRIBUTING.md](../../CONTRIBUTING.md) and only the schemas relevant to the edit. Establish permission before publishing private material.

1. Resolve the source and its revision/release/comment identity. For a repo inspect the relevant README/index, releases, branches, reports and open PRs. Fetch bounded sections. Do not execute its tools. Before any record work, check every branch, tag and release asset for published firmware (stock or modified update files, decoded images, dumps; by name, size and location, not by running anything). If found, stop: no records, no PR, and report what was found. Card data files, hashes, edit lists and download-and-patch builders are allowed.
2. Use project/camera/topic routes and search the affected record shards. Check whether this source or change already has an open PR.
3. Extract useful deltas. Separate observations, inference and proposals. Match exact target/build; retain limitations, negative outcomes, report-date versus test-date and expected versus reported/observed hashes.
4. Add sources and update existing records/topics. Schema examples: [record format](../../maintenance/record-format.md), [templates](../../templates/README.md). Only create new IDs/topics when needed. For a project or release, also update the project's showcase fields (description, features, releases; see the record format). Community listings are separate from technical evidence.
5. Run generate, check, tests and build as listed in AGENTS.md. Inspect the affected human pages. Keep generated outputs in the diff.
6. Raise a PR with sources/revisions, changed claims, missing evidence/conflicts, affected pages and validation. If access is missing, preserve the concrete diff and state the unfinished step. Do not claim a PR exists until creation succeeds. Do not approve or merge.

Redundant information may justify no content change. Insufficient evidence may justify a small source/project entry with visible gaps; never invent missing results. Recommend upstream contributions without contacting maintainers or posting there unless separately authorised.
