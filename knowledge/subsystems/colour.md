---
schema_version: 1
id: guide.subsystems.colour
title: Colour, profiles and persistence
summary: Find existing colour work and separate preview, saved output and settings persistence.
load_when: [investigating HSL or film looks, choosing a colour-research home]
topics: [colour, capture]
camera_ids: []
project_ids: [project.caduceus-ep7, project.caduceus-om3, project.caduceus-om5, project.oly-fw-analysis, project.em5-iii-notes]
depends_on: []
source_refs: [source.ep7.readme, source.om3.readme, source.om5.readme, source.fishcu.readme, source.db.release041, source.em5n.guide-settings, source.em5n.profiles]
last_reviewed: '2026-11-20'
---
# Several layers of colour work

The reviewed projects cover HSL, profiles, tone, effects and storing looks. Their feature sets and implementation homes differ. Begin at the camera's project list rather than assuming that a feature in one Caduceus port exists in another.

Live preview, saved JPEG output, movie output and persistence across switching profiles or powering off are separate behaviours. A report that shows a UI control does not establish every downstream effect. Use a separate scoped observation when a test checks one of these paths.

For detailed mechanisms use the original project: [PEN-F research](../../views/projects/oly-fw-analysis.md), [E-P7](../../views/projects/caduceus-ep7.md), [OM-3](../../views/projects/caduceus-om3.md), or [OM-5 generations](../../views/projects/caduceus-om5.md). The [db firmware release](../../views/sources/db.release041.md) is a further research source, with release-level claims and caveats. The Atlas's initial feature entries are starting points, not an exhaustive matrix.

# Settings that survive power-off

On the E-M5 III 1.7, a [settings and menus guide](../../views/sources/em5n.guide-settings.md) follows one setting from its menu row to the saved settings image, and shows how native rows with saved values were added. Its per-camera table marks which steps were checked on other bodies; treat the rest as unchecked.

# Hidden profile modes on bodies without the dial

Some bodies without the PEN-F / E-P7 creative dial still carry the Color Profile and Monochrome Profile settings and processing. The Caduceus OM-5 II port restored the hidden slots on that body. On the E-M5 III 1.7, [test builds](../../views/sources/em5n.profiles.md) made both modes selectable and added an on-camera wheel editor using the E-M1 III's own wheel routines; the notes separate what was seen in live view, in photos and after power-off. A body's own wheel routines may be stubs even when the settings are complete, so check the drawing code, not only the settings.

