"""Regression cases for scope, evidence integrity, routing and freshness."""
import copy
import datetime as dt
import json
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from atlas_core import Catalogue
from atlas_generate import generated_diff, render
from atlas import expand_nav, freshness, inspect_remote, review_notice, update_queue
from atlas_core import read_yaml, reference_status


class AtlasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = Catalogue(ROOT)

    def setUp(self):
        self.catalogue = copy.deepcopy(self.original)

    def test_canonical_corpus_validates(self):
        self.assertEqual(self.catalogue.validate(), [])

    def test_cross_model_evidence_rejected(self):
        cap = self.catalogue.records["capability.om5-ii-alpha12-overall"]
        cap["evidence_refs"] = ["evidence.om5-prealpha1-boot"]
        self.assertTrue(any("different camera_id" in e for e in self.catalogue.validate()))

    def test_cross_package_evidence_rejected(self):
        self.catalogue.records["capability.om5-ii-alpha12-overall"]["mod_build"] = "v0.1.0-alpha13"
        self.assertTrue(any("different mod_build" in e for e in self.catalogue.validate()))

    def test_firmware_cannot_change_camera(self):
        self.catalogue.records["evidence.om5-prealpha1-boot"]["firmware_id"] = "firmware.om5-ii-1100"
        self.assertTrue(any("belongs to camera.om5-ii" in e for e in self.catalogue.validate()))

    def test_expected_hash_does_not_complete_report(self):
        row = self.catalogue.records["evidence.om5-ii-alpha12-owner"]
        row["quality"] = "complete"
        errors = self.catalogue.validate()
        self.assertTrue(any("requires package_sha256" in e for e in errors))
        self.assertTrue(any("requires procedure" in e for e in errors))

    def test_label_only_cannot_claim_installed_digest(self):
        row = self.catalogue.records["evidence.om5-ii-alpha12-owner"]
        row["package_sha256"] = row["expected_package_sha256"]
        self.assertTrue(any("label-only" in e for e in self.catalogue.validate()))

    def test_synthetic_complete_report_is_accepted(self):
        row = self.catalogue.records["evidence.om5-ii-alpha12-owner"]
        row.update(quality="complete", identity_level="reported-hash", package_sha256="a" * 64, tested_on="2026-11-16",
                   procedure="Synthetic fixture: identify input, install, exercise the stated behaviour and record result.")
        self.assertEqual(self.catalogue.validate(), [])

    def test_posting_date_does_not_fill_unknown_test_date(self):
        row = self.catalogue.records["evidence.om5-prealpha1-boot"]
        self.assertIsNone(row["tested_on"])
        row["quality"] = "complete"
        self.assertTrue(any("requires tested_on" in e for e in self.catalogue.validate()))

    def test_missing_emulator_profile_rejected(self):
        del self.catalogue.records["evidence.om5-ii-image-store-probe"]["emulator"]
        self.assertTrue(any("emulator evidence needs" in e for e in self.catalogue.validate()))

    def test_dependency_cycles_rejected(self):
        row = self.catalogue.articles["guide.platform.identity"]
        row["depends_on"] = [row["id"]]
        self.assertTrue(any("dependency cycle" in e for e in self.catalogue.validate()))

    def test_deep_dependency_chain_rejected(self):
        base = self.catalogue.articles["guide.platform.identity"]
        for i in range(4):
            node = copy.deepcopy(base)
            node["id"] = f"guide.test.{i}"
            node["depends_on"] = [f"guide.test.{i+1}"] if i < 3 else []
            self.catalogue.articles[node["id"]] = node
        self.assertTrue(any("exceeds three guides" in e for e in self.catalogue.validate()))

    def test_ambiguous_family_requires_exact_model(self):
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            self.catalogue.resolve_camera("OM5")
        self.assertEqual(self.catalogue.resolve_camera("camera.om5"), "camera.om5")
        self.assertEqual(self.catalogue.resolve_camera("E148"), "camera.om5-ii")

    def test_look_task_does_not_load_tools(self):
        plan = self.catalogue.reading_plan("research", camera="om5-ii", topic="interfaces")
        self.assertIn("knowledge/interfaces/looks.md", plan)
        self.assertNotIn("knowledge/tooling/analysis.md", plan)
        self.assertEqual(len(plan), len(set(plan)))

    def test_required_base_precedes_tool_profile(self):
        plan = self.catalogue.reading_plan("research", camera="ep7", topic="tooling")
        self.assertLess(plan.index("knowledge/platform/identity.md"), plan.index("knowledge/tooling/analysis.md"))

    def test_release_url_routes_to_sparse_repo(self):
        plan = self.catalogue.reading_plan("ingest", source="https://github.com/azqeurio/om-c-firmware/releases/tag/dbv0.4.1")
        self.assertIn("agents/routes/projects/db-firmware.md", plan)

    def test_generated_human_report_retains_missing_identity(self):
        output = render(self.catalogue)["views/evidence/om5-ii-alpha12-owner.md"]
        self.assertIn("Reported/observed package SHA-256:** not recorded", output)
        self.assertIn("Expected manifest SHA-256:", output)
        self.assertIn("partial report", output)

    def test_generated_drift_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "views").mkdir()
            (root / "views/test.md").write_text("manual edit", encoding="utf-8")
            self.assertIn("views/test.md", generated_diff(root, {"views/test.md": "canonical output"}))

    def test_network_failure_preserves_canonical_sources(self):
        before = copy.deepcopy(self.catalogue.records)

        def unavailable(*args, **kwargs):
            raise urllib.error.URLError("synthetic offline fixture")

        report = freshness(self.catalogue, fetch=True, today=dt.date(2026, 11, 18), fetcher=unavailable)
        self.assertTrue(all(row["state"] == "check-failed" for row in report["sources"]))
        self.assertEqual(before, self.catalogue.records)

    def test_repo_advance_is_not_claim_promotion(self):
        source = self.catalogue.records["source.om5.readme"]
        reviewed = source["last_reviewed"]
        result = inspect_remote(source, lambda *args, **kwargs: [{"sha": "f" * 40}])
        self.assertEqual(result["state"], "upstream-advanced")
        self.assertEqual(source["last_reviewed"], reviewed)

    def test_source_schema_rejects_unknown_fields(self):
        schema = json.loads((ROOT / "schemas/records.schema.json").read_text())
        selected = {"$ref": "#/$defs/source", "$defs": schema["$defs"]}
        row = copy.deepcopy(self.catalogue.records["source.om5.readme"])
        row["verified_safe"] = True
        self.assertTrue(Catalogue.schema_errors(selected, row, "synthetic source"))

    def test_publication_age_does_not_renew_sources(self):
        row = self.catalogue.records["camera.om5-ii"]
        checked = self.catalogue.records["source.om5.readme"]["last_checked"]
        notice = review_notice(self.catalogue, row, dt.date(2027, 1, 1))
        self.assertIn("Source review due", notice)
        self.assertEqual(self.catalogue.records["source.om5.readme"]["last_checked"], checked)

    def test_community_directory_has_direct_venue_links(self):
        output = render(self.catalogue)["views/community/index.md"]
        self.assertIn("https://discord.gg/fKpcKGsNPY", output)
        self.assertIn("https://www.reddit.com/r/M43/", output)

    def test_navigation_lists_every_camera_and_guide(self):
        nav = expand_nav(read_yaml(ROOT / "mkdocs.yml")["nav"], self.catalogue)
        paths = []

        def walk(entries):
            for entry in entries:
                for value in entry.values():
                    walk(value) if isinstance(value, list) else paths.append(value)

        walk(nav)
        for row in self.catalogue.of_type("camera"):
            self.assertIn(f"views/cameras/{row['id'].split('.', 1)[1]}.md", paths)
        for article in self.catalogue.articles.values():
            self.assertIn(article["path"], paths)
        self.assertNotIn("knowledge/README.md", paths)

    def test_camera_page_leads_with_projects_and_support(self):
        output = render(self.catalogue)["views/cameras/om5-ii.md"]
        project = self.catalogue.records["project.caduceus-om5"]
        self.assertLess(output.index("## What you can do with this camera"), output.index("## Projects for this camera"))
        self.assertLess(output.index("## Projects for this camera"), output.index("## Claims and test evidence"))
        self.assertIn(f"[Ask or report issues]({project['contribution_home']})", output)
        self.assertIn("partial report", output)

    def test_new_upstream_release_is_queued_not_applied(self):
        before = copy.deepcopy(self.catalogue.records)

        def newer(*args, **kwargs):
            return [{"tag_name": "v9.9", "html_url": "https://github.com/example/r/releases/tag/v9.9",
                     "published_at": "2026-12-01T00:00:00Z", "prerelease": False}]

        report = freshness(self.catalogue, fetch=True, today=dt.date(2026, 12, 2), fetcher=newer)
        om3 = next(p for p in report["projects"] if p["id"] == "project.caduceus-om3")
        self.assertEqual(om3["state"], "release-not-catalogued")
        self.assertIn("v9.9", update_queue(report))
        self.assertEqual(before, self.catalogue.records)

    def test_showcase_feature_cannot_claim_uncatalogued_camera(self):
        self.catalogue.records["project.caduceus-om3"]["features"][0]["camera_ids"] = ["camera.pen-f"]
        self.assertTrue(any("not in the project's camera_ids" in e for e in self.catalogue.validate()))

    def test_releases_must_be_listed_newest_first(self):
        self.catalogue.records["project.caduceus-om3"]["releases"].reverse()
        self.assertIn("project.caduceus-om3: list releases newest first.", self.catalogue.validate())

    def test_project_page_attributes_features_and_warns_before_install(self):
        output = render(self.catalogue)["views/projects/caduceus-om3.md"]
        self.assertIn("As the project describes them", output)
        self.assertIn("Before you install", output)
        self.assertIn("v0.30.3", output)

    def reference(self, node_id="reference.om3-1100.half-press-hook"):
        return self.catalogue.records[node_id]

    def test_reference_rejects_duplicate_address(self):
        twin = copy.deepcopy(self.reference())
        twin["id"] = "reference.om3-1100.half-press-twin"
        self.catalogue.records[twin["id"]] = twin
        self.assertTrue(any("merge them and add an observation" in e for e in self.catalogue.validate()))

    def test_reference_rejects_disassembly_and_byte_dumps(self):
        self.reference()["note"] = "Hook: call 0x60415343,[d2,d3,a2,a3],36 then resume."
        self.assertTrue(any("contains disassembly" in e for e in self.catalogue.validate()))
        self.reference()["note"] = "Stock bytes f1 ec cd cb f7 f0 38 00 11 at the site."
        self.assertTrue(any("contains byte dumps" in e for e in self.catalogue.validate()))

    def test_reference_address_belongs_to_one_build(self):
        self.reference()["firmware_ids"].append("firmware.ep7-1100")
        self.reference()["camera_ids"].append("camera.ep7")
        self.assertTrue(any("exactly one firmware build" in e for e in self.catalogue.validate()))

    def test_reference_requires_pinned_source_and_upstream_link(self):
        self.catalogue.records["source.om3.devnotes"]["revision"] = None
        self.reference()["upstream_detail"] = "https://example.com/notes"
        errors = self.catalogue.validate()
        self.assertTrue(any("is not pinned" in e for e in errors))
        self.assertTrue(any("upstream_detail must link" in e for e in errors))

    def test_reference_status_is_derived_from_observations(self):
        records = self.catalogue.records
        hazard = records["reference.hazard.section-load-order"]
        self.assertEqual(reference_status(records, hazard), "camera-confirmed")
        self.assertEqual(reference_status(records, records["reference.hazard.logical-flash-writes"]), "corroborated")
        self.assertEqual(reference_status(records, records["reference.em5-iii-1700.section-ready-test"]), "single-source")
        self.assertEqual(reference_status(records, self.reference()), "camera-confirmed")
        hazard["conflicts"] = [{"source_ref": "source.om3.devnotes", "summary": "A different load order."}]
        self.assertEqual(reference_status(records, hazard), "disputed")

    def test_platform_entry_needs_known_trait_and_value(self):
        row = self.reference("reference.em5-iii-1700.main-cpu")
        row["trait"] = "trait.not-in-taxonomy"
        del row["value"]
        errors = self.catalogue.validate()
        self.assertTrue(any("choose a trait" in e for e in errors))
        self.assertTrue(any("needs a value" in e for e in errors))

    def test_native_feature_needs_presence_and_known_feature(self):
        row = self.reference("reference.om5-1200.native-nd")
        del row["presence"]
        row["feature_id"] = "feature.not-in-taxonomy"
        errors = self.catalogue.validate()
        self.assertTrue(any("needs a presence" in e for e in errors))
        self.assertTrue(any("choose a feature_id" in e for e in errors))

    def test_build_facts_belong_to_one_build_without_address(self):
        row = self.reference("reference.om5-1200.native-nd")
        row["firmware_ids"].append("firmware.om5-ii-1100")
        row["camera_ids"].append("camera.om5-ii")
        row["address"] = {"space": "runtime-cached", "value": "0x60021020"}
        errors = self.catalogue.validate()
        self.assertTrue(any("describes exactly one firmware build" in e for e in errors))
        self.assertTrue(any("put addresses in their own entries" in e for e in errors))

    def test_build_fact_fields_rejected_on_other_categories(self):
        self.reference()["presence"] = "native"
        self.assertTrue(any("belong to platform and native-feature entries" in e for e in self.catalogue.validate()))

    def test_duplicate_build_fact_rejected(self):
        twin = copy.deepcopy(self.reference("reference.om5-1200.native-nd"))
        twin["id"] = "reference.om5-1200.native-nd-twin"
        self.catalogue.records[twin["id"]] = twin
        self.assertTrue(any("same build and native-feature fact" in e for e in self.catalogue.validate()))

    def test_feature_matrix_and_platform_tables_are_generated(self):
        outputs = render(self.catalogue)
        index = outputs["views/reference/index.md"]
        self.assertIn("## Built-in features by build", index)
        self.assertIn("## Platform by build", index)
        self.assertIn("Native: ND2 to ND16", index)
        self.assertIn("## Platform and built-in features", outputs["views/cameras/em5-iii.md"])
        self.assertIn("## Built-in features", outputs["views/firmware/om5-1200.md"])
        self.assertIn("platform and built-in features", outputs["agents/routes/reference/om5.md"])


if __name__ == "__main__":
    unittest.main()
