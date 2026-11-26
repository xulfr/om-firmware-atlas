# Canonical record format

Collections in `records/<type>/` contain `schema_version: 1` and a non-empty `records` list. Each row has `type`, a stable prefixed `id`, `title`, `summary`, `last_reviewed`, and source/topic references. Keep related source/observation rows together; split a costly batch by investigation or period without changing IDs. Full definitions are in [records.schema.json](../schemas/records.schema.json).

| Kind | Required scope beyond the common fields |
|---|---|
| camera | Aliases, model codes, project IDs and catalogue depth |
| firmware | Camera, advertised/internal version, full hash or explicit null, identity limitations |
| project | URL/kind, catalogued cameras, contribution destination, attributed state and related work. Optional showcase: tagline, description, goals, maintainers, links, features, releases, images |
| capability | Camera, firmware/project/build, feature ID, availability, implementation basis, evidence/contradiction refs and limits |
| evidence | Target/build, method/provenance, identity strength, separate expected and reported/observed hashes, result, procedure/coverage, dates, completeness and assumptions |
| source | URL, source kind, repository/revision where relevant, locator, retrieval/check date, publication scope and reuse note |
| reference | Category, cameras, firmware builds, optional address (one build only), or for platform/native-feature entries a taxonomy trait or feature, value and presence (one build only), short note, consequence and taxonomy `symptoms` for hazards, observations with method and pinned source, conflicts and an upstream detail link. See the [reference policy](reference-policy.md) |
| community | URL/platform, audience/scope, listing basis, access, project links and precise link-check state/date |

Use `null` for an unknown nullable field, not an invented value. A null firmware hash still permits an honest discovery entry but cannot support byte-exact work. Referenced firmware and evidence must match the capability's camera/project/build. Shared method does not authorise transferring a result.

Physical evidence marked `complete` requires target/build, package hash from the report or observation, steps and explicit test date. `quality: partial` preserves a useful but incomplete account. `identity_level: release-label-only` cannot carry a reported package digest. Keep a manifest's expected digest in `expected_package_sha256`.

Repository file sources use the same full commit in `revision` and `/blob/<commit>/` URL. A file source that follows a side branch, or release notes pinned at a tag, names that branch or tag in `tracked_ref`, so freshness checks compare with it rather than the default branch. Release descriptions and comments are mutable; a reviewed body digest can provide a baseline for future checks. The freshness checker reports missing baselines rather than claiming unchanged content.

## Project showcase fields

Release records may include `camera_limits`, mapping cameras named in that release to `reported-not-working` (the project explicitly reports failure) or `features-unspecified` (the release names the camera without identifying its features). Cite the release through its existing source reference. An omitted entry means no such limitation is recorded. It makes no claim about successful testing. The latest release is the first matching entry in the project's newest-first release list, including pre-releases. Records determine the order for tags on the same date.

A release may include an `installation` mapping from a camera ID to `firmware_id` and `url`. Use the project's guide or release instructions reviewed for that release, camera and stock firmware. The camera must be in the release's `camera_ids` and have no `camera_limits` entry. With no matching installation entry, the camera showcase links to the release notes. Review the guide separately when adding another release.

A project work item may name a `tester_camera_id` when the linked project explicitly asks for a volunteer with that camera. It must be one of the project's cameras. Open and needs-evidence items with this field appear as testing requests. Leave it out for ordinary evidence gaps or bugs awaiting confirmation.

Project pages, the projects directory, camera showcases and owner release summaries use these optional fields. `description` is a list of plain paragraphs written from the project's own documentation. Each `features` entry has `name`, `summary`, `camera_ids` (a subset of the project's), `status` (`released`, `beta`, `alpha`, `testing`, `in-development`, `planned` or `research`, in the project's own terms), optional `since`, `capability_id` and `spotlight_until` (a date at most 31 days after the project's `last_reviewed`, which highlights the feature on the home page until then; see [decision 0009](decisions/0009-feature-spotlight.md)), and a `source_ref`. Each `releases` entry has `tag`, `title`, `date`, `url`, `prerelease`, `camera_ids`, `highlights`, an optional `warning` and a `source_ref`; list them newest first. Optional `camera_notes` entries (`camera_id`, `note`) say in a sentence or two what the project has for one of its cameras and how to get it; the camera showcase shows them under the project. Write one whenever a project is listed for a camera it offers little or nothing for. `images` live under `docs/assets/projects/<project>/` with `alt`, `caption` and `credit`, and need the maintainers' agreement. An optional `camera_id` identifies the model shown. A multi-model project image without this field stays on the general project pages. Feature status is the project's claim, not Atlas evidence; link a capability for the evidence.

## Guides and dependencies

Subject guides under `knowledge/` have the metadata in [article.schema.json](../schemas/article.schema.json): ID, title, summary, load conditions, topic/camera/project coverage, required guide dependencies, sources and substantive-review date. Dependencies must resolve without cycles and use at most three guides along a path. A specialised guide explains its delta; it does not repeat the base.

Update `last_reviewed` after checking the facts. A move, reformat or successful HTTP response does not renew it. Historical observations preserve event dates; source check, publication, report and test dates have different meanings.

Add taxonomy IDs when a useful new concept needs them. Keep existing IDs/aliases stable. Generated `views/` and `agents/routes/` compose these records and metadata; `python scripts/atlas.py generate` is their only editing interface.

Examples to inspect: [camera](../records/cameras/om5-ii.yaml), [firmware](../records/firmware/ep7/ep7-1100.yaml), [project](../records/projects/caduceus-om3.yaml), [capability](../records/capabilities/om5-ii/om5-ii-alpha12-overall.yaml), [observations](../records/evidence/caduceus-om5.yaml), [sources](../records/sources/om5.yaml), [community](../records/community/venues.yaml), [reference](../records/reference/om5-ii-1100.yaml), [platform reference](../records/reference/om5-ii-1100-platform.yaml).
