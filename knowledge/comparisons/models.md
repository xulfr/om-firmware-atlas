---
schema_version: 1
id: guide.comparisons.models
title: Reason across models without inventing compatibility
summary: Use shared code as a research lead while retaining model, build and method boundaries.
load_when: [planning a port, comparing firmware families]
topics: [platform]
camera_ids: []
project_ids: [project.caduceus-ep7, project.caduceus-om5, project.om-emu, project.em5-iii-notes]
depends_on: [guide.platform.identity]
source_refs: [source.ep7.bodies, source.emu.cores, source.om5.readme, source.em5n.comparison]
last_reviewed: '2026-11-17'
---
# Similarity is a set of observations

A shared container, processor family, matching instruction sequence, common UI subsystem and compatible physical device are different kinds of similarity. Do not collapse them into a single port score.

The E-P7 [body survey](../../views/sources/ep7.bodies.md) reports signature matches under its particular method and revision, while retaining missing screens/hooks and camera-testing gaps. Those percentages do not measure how safe or complete a port is.

The original OM-5 and Mark II have separate identities and projects can take different approaches to them. Follow the exact [camera record](../../views/cameras/index.md), not the broad “OM-5” family label. Processor-role observations are also model-specific; the [OM-1 analysis](../../views/sources/emu.cores.md) is not a universal hardware specification.

# Where to start looking on another body

The [E-M5 III body comparison](../../views/sources/em5n.comparison.md) has a table of items whose strings or constants appear in six main programs (E-M5 III, OM-5, OM-5 II, E-M1 III, OM-1, PEN-F): debug shell commands, the card updater folder, the settings save, the setting-to-property table, the RGB histogram path and the loader's access monitor. Presence is a lead, not a result: it says where to look, not that an item behaves the same or sits at the same address.

A second table on the same page takes each E-M5 III feature (Live ND, HHHR, Starry Sky AF, any-lens focus stacking, menu rows with saved values, the profile editor, webcam, Wi-Fi shell, card console) and says per body whether it is already native or whether the parts the port uses are there, marking each cell as a string check, a code match or an earlier finding. For example, the any-lens focus stacking branch has the same shape at a per-body address on the OM-5, OM-5 II, E-M1 III, OM-1 and OM-1 II; none of these was tried on those cameras.
