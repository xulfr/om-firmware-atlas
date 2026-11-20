---
schema_version: 1
id: guide.methods.patching
title: Patching and scoped validation
summary: Reuse existing builders and keep container correctness distinct from runtime evidence.
load_when: [choosing a patch workflow, interpreting a validation result]
topics: [patching]
camera_ids: []
project_ids: [project.caduceus-om5, project.oly-fw-analysis, project.em5-iii-notes]
depends_on: [guide.platform.identity]
source_refs: [source.om5.builder, source.fishcu.validation, source.ep7.guide, source.em5n.patching]
last_reviewed: '2026-11-17'
---
# Reuse the builder that owns the target

The examined workflows identify stock input, decode it, apply bounded changes, rebuild and check the result. Some developer paths assemble/link MN103 source; user paths apply recorded changes locally. The [OM-5 strict builder](../../views/sources/om5.builder.md) uses a declarative definition and expected hashes. Other projects have their own implementations. The Atlas documents these methods; it does not own a new patch engine.

Correct checksums and unchanged-container round trips establish container properties. They do not establish successful startup or image processing. The [validation reference](../../views/sources/fishcu.validation.md) distinguishes placement, ABI/alignment, pipeline, physical and recovery checks. A fixture can conceal behaviour the camera exposes.

Keep a reported recovery scoped to its failed state and target. Record negative outcomes and assumptions rather than weakening checks to make a build look successful. Use [the evidence model](../../docs/evidence.md) for Atlas records and upstream instructions for actual build/test procedures.

# Start from a technique that was shown on a camera

The [E-M5 III modification techniques](../../views/sources/em5n.patching.md) list each method with its pitfalls and a table of the cameras and firmware it has been shown on, crediting other projects' results. A row for one body is a lead for another, not a result: addresses, tables and load order differ per build, so each body needs its own evidence.
