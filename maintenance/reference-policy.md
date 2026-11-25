# Technical reference: what goes in, what stays upstream

The Atlas keeps a small, shared technical reference so agents and people don't rebuild the same index from every repository each time. It is not a second copy of anyone's research. Detailed notebooks stay with the projects that own them; for most topics the deepest home is [Olympus firmware research](https://github.com/fishcu/oly_fw_analysis).

Reference entries live in `records/reference/` as `reference` records ([record format](record-format.md)). The checker enforces the rules marked **(checked)**.

## In: reusable facts with an identity

An entry is a fact that more than one project or agent is likely to need, and that can be stated in a sentence or two.

| Category | Example |
|---|---|
| `function`, `hook-site`, `data`, `table` | A named stock function, hook site or table at one address in one build |
| `free-space` | An unused range that patches can claim, with its start and end |
| `layout` | A base or offset needed to translate between address spaces |
| `hazard` | A trouble spot: a rule such as "keep patch state out of the loaded image", with its consequence and the `symptoms` it shows on the camera |
| `platform` | One hardware or layout fact about one build, keyed by a `trait` from the taxonomy, with a short `value`: "Image processor generation: TruePic VIII" |
| `native-feature` | Whether the stock build contains a feature, keyed by a taxonomy `feature_id`, with a `presence` (native, dormant, partial, strings-only or absent) and an optional short `value`: "Live ND: native, ND2 to ND16" |

Each entry:

- names **exactly one firmware build** when it has an address **(checked)**. Addresses never transfer between builds or bodies; make a separate entry per build. A hazard can span builds, but has no address of its own **(checked)**.
- for a `hazard`, lists one or more `symptoms` from `taxonomy/topics.yaml` **(checked)**: what an owner or tester sees, such as a slow start or a freeze. The reference index groups hazards by symptom across bodies, so a fault seen on one camera leads to causes recorded on others.
- for `platform` and `native-feature`, names exactly one firmware build, no address, and a known trait or feature **(checked)**. One entry per build and trait or feature **(checked)**. These describe the stock firmware only; what a project adds is a capability, not a native feature.
- records **how it was established** in one or more observations: static analysis, emulator or physical camera, each from a **pinned source** (a commit, release tag or content digest) **(checked)**.
- links the **upstream section** that explains it, in one of the cited sources' repositories **(checked)**.
- keeps its text short: title 90 characters, summary 200, note 600, each observation 300 **(checked)**.

## Out: detail that belongs upstream

- How a fact was found: traces, derivations, test logs and lab-notebook narrative.
- Disassembly, instruction sequences, byte dumps, patch code and long hex runs **(checked)**.
- Vendor firmware or any part of it.
- Explanations longer than a short note. Write them in the project, then link them.
- Project-specific bug lists. Those belong in the project's issue tracker, and release warnings belong in the project record.
- Findings from private channels without permission to publish.
- Speculation without a source. An inference can be recorded, but only from a source that states it, and marked as such in the note.

## Several agents, one record

Agents and people working from different projects should add to the same entry, not make their own:

- **One entry per fact.** Two entries for the same build, address space and address are rejected **(checked)**. Add your finding as another observation.
- **Status is derived, never set by hand:**
  - **Disputed:** a conflicting report is listed.
  - **Camera-confirmed:** at least one physical-camera observation.
  - **Corroborated:** observations from at least two independent repositories.
  - **Single source:** everything else.
- **Disagreement is recorded, not overwritten.** If your result differs, add it to `conflicts` with its source. Compare build, method and date before deciding it is a real conflict.
- **Promotion needs evidence.** A new emulator run does not make an entry camera-confirmed; only a physical-camera observation from a pinned source does.

## Size limits

Each file in `records/reference/` stays under 16,000 bytes **(checked)**; split by build or topic beyond that. Agents read the generated per-camera shards in `agents/routes/reference/`, not the records. Routing tests keep each reading plan within its token budget.

If an entry needs more than a short note to be useful, it probably belongs upstream with a link from here.
