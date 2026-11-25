# Cross-body research

Compare firmware across models, find shared tools and read research methods.

<div class="explore-grid research-start" markdown="1">

[**Guides** <span>Platform, patching, emulation and firmware analysis.</span>](../knowledge/README.md)
[**Projects and tools** <span>Repositories, emulators and active investigations.</span>](../views/projects/index.md)
[**Technical reference** <span>Platform comparisons and shared pitfalls.</span>](../views/reference/index.md)
[**Diagnose by symptom** <span>Known causes of a restart, slow start or freeze, on any body.</span>](../views/reference/index.md#diagnose-by-symptom)

</div>

[Research by camera](../views/research/index.md) · [How the Atlas works](how-it-works.md)

## From update file to working camera

1. **Identify the file.** The Olympus update files studied here package several components. Record the model, version and file fingerprint before comparing them. A position in the file can refer to a different place once the camera loads it. [Firmware identity and address spaces](../knowledge/platform/identity.md).
2. **Follow the card update.** On the documented bodies, the camera's updater reads a prepared card and writes the firmware. Recovery uses the same route with official firmware, provided the updater can still run. [Card recovery and owner reports](before-you-install.md#if-the-camera-will-not-start).
3. **Trace start-up for this build.** The camera loads and prepares parts of the program in stages. The E-M5 III notes show which parts are ready early. The E-P7 guide covers its own layout and loader. [E-M5 III start-up](../views/sources/em5n.boot.md) · [E-P7 firmware guide](../views/sources/ep7.guide.md).

## Risk by type of change

| What changes | What could go wrong | What the Atlas records |
|---|---|---|
| Bootloader (the first program to run) or card updater | Damage here could prevent the camera from reaching a recovery update. | On OM-5 Mark II 1.1 the project located the card updater in section 7. It recommends preserving that section. This is an inferred risk. The record attributes no failure to it. [Updater finding](../views/reference/hazard.updater-section-stock.md). |
| Code that runs on every start | A fault can repeat each time the camera starts. The route back depends on how the project loads its changes. | OMKit on OM-5 Mark II 1.1 adds a loader late in start-up. Its developers report that holding OK or removing the card bypasses their card-loaded code. Caduceus separately records an intermittent restart loop on this model. [OMKit report](../views/evidence/om5-ii-omkit-loader.md) · [Caduceus report](../views/evidence/om5-ii-dev0565-boot.md). |
| Code reached through a menu or shooting feature | A fault may only appear when that feature runs. Installing a changed firmware image still carries the risks above. | The original E-M10 project om10mi-mods records a freeze reported with filters enabled. The report lacks the body and build details needed to reproduce it. [Project and open reports](../views/projects/om10mi-mods.md). |

A feature name alone cannot establish that a release touches only later code, or that it changes the bootloader. Where the project gives no boundary, treat it as unknown. [Compare a flashed feature with a card-loaded module](../knowledge/methods/patching.md).

## Common pitfalls

- **Requested and ready are different states.** Calling a section too early can reach code before it is initialised. The reference preserves differing interpretations of the readiness signal. [Start-up observations](../views/reference/hazard.ready-not-requested.md).
- **Apparently empty space may be used later.** Firmware can overwrite a patch's working data as sections load. Check the build-specific observations and project development notes. [Loaded-image hazard](../views/reference/hazard.state-in-loaded-image.md) · [Shared trouble spots](../views/reference/index.md#trouble-spots).
- **A quick restart is not a cold start.** RAM kept across a short power-off can still hold code that a fresh start has not loaded yet. On the E-PM2 this hid a hook into a late segment that made cold starts take about 10 s, and the emulator could not show it either. Test start-up changes after a long power-off. [Cold-start hazard](../views/reference/hazard.kept-ram-hides-cold-start.md) · [Check the built image](../views/reference/hazard.check-built-image.md).
- **A hook runs on every path through its routine.** On the E-M1 Mark III, HDR takes an early exit from the sharpening routine that skips the setup a Sharpness hook relied on, and the camera rebooted. [Early-exit hazard](../views/reference/hazard.hook-early-out-paths.md).
- **A passing check has a scope.** On the original OM-5, one tester reported an unusable start followed by restoration of official 1.2 from the card. Retain both outcomes when investigating later builds. [Failed start](../views/evidence/om5-prealpha1-boot.md) · [Recovery report](../views/evidence/om5-prealpha1-restore.md) · [Validation methods](../knowledge/methods/patching.md).

## Architecture by hardware family

The [platform comparison by firmware build](../views/reference/index.md#platform-by-build) lines up the image processor, main CPU, co-processor, memory and update-file layout. Each populated cell links to its source. A blank means the Atlas lacks that fact.

- **TruePic VI.** The E-PM2 1.6 record describes two MN103 cores and no ARM co-processor. [E-PM2 platform](../views/research/epm2.md#platform).
- **TruePic VIII.** E-M5 Mark III 1.7 combines MN103 cores with a Cortex-A9 co-processor. [E-M5 Mark III platform](../views/research/em5-iii.md#platform).
- **TruePic IX.** OM-5 1.2 and OM-5 Mark II 1.1 share an image processor generation, main CPU family and image memory layout. Their co-processors run different Linux versions and their update files have different identifiers. [OM-5 platform](../views/research/om5.md#platform) · [Mark II platform](../views/research/om5-ii.md#platform).

An overlap suggests a comparison to try. **Addresses and results never transfer automatically** between bodies or builds. [Cross-model reasoning](../knowledge/comparisons/models.md).

## Choose a task

| You want to… | Start here |
|---|---|
| Identify or unpack firmware | [Firmware identity and address spaces](../knowledge/platform/identity.md) |
| Understand patch construction | [Patching and scoped validation](../knowledge/methods/patching.md) |
| Learn how one camera's firmware works, step by step | [E-M5 III firmware guides](../views/sources/em5n.guides.md) |
| Draw your own screens or graphics | [Display and drawing](../knowledge/subsystems/display.md) · [Drawing your own graphics](../views/sources/em5n.guide-own-graphics.md) · [Drawing with the vector GPU](../views/sources/em5n.guide-vector-gpu.md) |
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

Working with an AI agent? Use the [research and contribution prompts](research-with-ai.md). These routes can be read without installing a firmware toolchain.
