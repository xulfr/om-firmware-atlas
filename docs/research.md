# Research

For people building new work: guides to the firmware, the evidence catalogue, and how to choose where a change belongs. Looking for what you can install today? See [Cameras](../views/cameras/index.md) and [Projects](../views/projects/index.md).

## Check what exists first

Choose the [exact camera and generation](../views/cameras/index.md). Check the firmware identity, related projects and known gaps. Shared code or a similar model name is a research lead; it does not make an existing patch portable.

## Technical reference

The [technical reference](../views/reference/index.md) holds compact, sourced facts that projects keep needing: named addresses for one exact firmware build, free code space, and known trouble spots such as "keep patch state out of the loaded image". Each entry shows how it was established and whether independent projects agree, and links the upstream section with the full explanation.

The detailed research stays with the projects. [Olympus firmware research](../views/projects/oly-fw-analysis.md) is the deepest home for most topics. [The reference policy](https://github.com/xulfr/om-firmware-atlas/blob/main/maintenance/reference-policy.md) sets out what belongs in the Atlas and what stays upstream.

## Choose a task

| You want to… | Start here |
|---|---|
| Identify or unpack firmware | [Firmware identity and address spaces](../knowledge/platform/identity.md) |
| Understand patch construction | [Patching and scoped validation](../knowledge/methods/patching.md) |
| Learn how one camera's firmware works, step by step | [E-M5 III firmware guides](../views/sources/em5n.guides.md) |
| Trace or decompile code | [Analysis tool profiles](../knowledge/tooling/analysis.md) |
| Exercise firmware outside a camera | [Emulation coverage](../knowledge/emulation/coverage.md) |
| Work on colour, profiles or settings | [Colour and settings research](../knowledge/subsystems/colour.md) |
| Move or add film looks | [Looks and interfaces](../knowledge/interfaces/looks.md) |
| Compare related bodies | [Cross-model reasoning](../knowledge/comparisons/models.md) |

## Browse the catalogue

<div class="explore-grid" markdown="1">

[**Firmware** <span>Stock versions that work starts from</span>](../views/firmware/index.md)
[**Feature claims** <span>Scoped claims per camera, project and build, with their evidence</span>](../views/capabilities/index.md)
[**Observations** <span>Camera, emulator and code findings, with their gaps</span>](../views/evidence/index.md)
[**Sources** <span>Everything cited, with revisions and check dates</span>](../views/sources/index.md)

</div>

Before relying on a status, read [Reading the evidence](evidence.md).

## Choose a contribution home

For an existing mod, use its repository and contribution process. For an emulator/tool defect, use its implementation owner and identify the exact fork/revision. For a shared-interface change, check current consumers and maintainer policy; a consolidation proposal is not automatically an agreement.

Use the Atlas for cross-project explanations, source records and scoped evidence. Before recommending a new repository, inspect existing branches, issues and related attempts and explain why those homes do not fit. The [project directory](../views/projects/index.md) gives starting destinations, not an ownership ruling.

Working with an AI agent? Use the [research prompt](how-it-works.md#copyable-prompts). These routes can be read without installing a firmware toolchain.
