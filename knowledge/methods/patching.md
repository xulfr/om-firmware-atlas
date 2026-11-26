---
schema_version: 1
id: guide.methods.patching
title: Patching and scoped validation
summary: Reuse existing builders and keep container correctness distinct from runtime evidence.
load_when: [choosing a patch workflow, interpreting a validation result, deciding where mod code lives]
topics: [patching]
camera_ids: []
project_ids: [project.caduceus-om5, project.oly-fw-analysis, project.em5-iii-notes, project.omkit, project.fenykl, project.caduceus-om3]
depends_on: [guide.platform.identity]
source_refs: [source.om5.builder, source.fishcu.validation, source.ep7.guide, source.em5n.patching, source.omkit.patch, source.omkit.architecture, source.fenykl.sdk, source.fenykl.loader-source, source.om3.film-rolls-roadmap, source.om3.v041-beta3]
last_reviewed: '2026-11-26'
---
# Reuse the builder that owns the target

The examined workflows identify stock input, decode it, apply bounded changes, rebuild and check the result. Some developer paths assemble/link MN103 source; user paths apply recorded changes locally. The [OM-5 strict builder](../../views/sources/om5.builder.md) uses a declarative definition and expected hashes. Other projects have their own implementations. The Atlas documents these methods; it does not own a new patch engine.

Correct checksums and unchanged-container round trips establish container properties. They do not establish successful startup or image processing. The [validation reference](../../views/sources/fishcu.validation.md) distinguishes placement, ABI/alignment, pipeline, physical and recovery checks. A fixture can conceal behaviour the camera exposes.

Keep a reported recovery scoped to its failed state and target. Record negative outcomes and assumptions rather than weakening checks to make a build look successful. Use [the evidence model](../../docs/evidence.md) for Atlas records and upstream instructions for actual build/test procedures.

# Start from a technique that was shown on a camera

The [E-M5 III modification techniques](../../views/sources/em5n.patching.md) list each method with its pitfalls and a table of the cameras and firmware it has been shown on, crediting other projects' results. A row for one body is a lead for another, not a result: addresses, tables and load order differ per build, so each body needs its own evidence.

# Flash the feature, or flash a loader

Most projects here put their code into the firmware image, so each code change is a new patched update file and another flash. Some read look data from the card, but the code that uses it is flashed.

[OMKit](../../views/projects/omkit.md) flashes only a [loader](../../views/sources/omkit.patch.md) on the OM-5 Mark II 1.1. One hook late in startup creates a low-priority task. The task reads `OMKIT\CORE.BIN` from the card, checks it and jumps into it; core then checks the firmware and loads the modules named in `OMKIT.INI`. Updating means copying files. Without the card or file, or with OK held, the camera runs as stock. The developers report this on their camera since 2026-10-30 ([evidence](../../views/evidence/om5-ii-omkit-loader.md)).

[fenykl](../../views/projects/fenykl.md) does the same on the E-M10 Mark II 1.4 with one plugin file, `FENYKL.BIN`, started as a task from the [end of startup stage Usr3](../../views/reference/em10-ii-1400.usr3-end.md). On this body the OK-held card update never reaches that point, so card reflashing does not depend on the loader.

Caduceus for OM-3 takes a middle path for [Film Rolls](../../views/capabilities/om3-film-rolls.md). The flashed firmware carries the loader, small sockets that each ask whether the card file is loaded and otherwise run as stock, and the table entries of Picture Mode's row; `OM3MOD/FILMROLL/FILMROLL.BIN` carries the feature's code and installs any further hooks itself when it loads at the first half-press, never at start-up. Its [design notes](../../views/sources/om3.film-rolls-roadmap.md) describe each runtime hook as a 5-byte jump written through the uncached view under the firmware lock, after checking the stock bytes, never across a 16-byte cache line, following OMKit's method. The card file is built for one firmware build: [v0.41-beta3](../../views/sources/om3.v041-beta3.md) does not load beta2's. The owner reports camera tests; there is no independent report yet.

The trade-offs are different, not smaller. A fault in core or a module loops on every start until the card is removed or OK is held. Modules are not isolated from the firmware. An official update removes the loader, and each firmware build needs its own loader and driver. OMKit's loader waits on a section word that a Caduceus finding says marks only the load request; the [reference shard](../../agents/routes/reference/om5-ii.md) keeps both readings.
