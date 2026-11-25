"""Atlas documentation CLI. Run from any directory with the environment active."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

import yaml

from atlas_core import Catalogue, LINK_RE, REPO, cost, markdown_links, read_yaml, routing_checks
from atlas_generate import atlas_counts, camera_finder, camera_research_path, generated_diff, people_markdown, recent_findings, render, showcase, view_path, write_generated

ROOT = Path(__file__).resolve().parents[1]


def checked(catalogue, generated=True, links=True):
    errors = catalogue.validate()
    if errors:
        return errors
    if generated:
        for path in generated_diff(catalogue.root, render(catalogue)):
            errors.append(f"Generated drift: {path}; run python scripts/atlas.py generate and commit the result.")
    if links:
        errors.extend(markdown_links(catalogue.root))
        errors.extend(routing_checks(catalogue))
    for directory in ("records", "knowledge"):
        for path in (catalogue.root / directory).rglob("*"):
            if path.is_file() and path.suffix.lower() in (".bin", ".exe", ".gpr", ".gz", ".zip"):
                errors.append(f"{path.relative_to(catalogue.root)}: keep firmware, research binaries and dumps upstream.")
    return errors


def review_notice(catalogue, row, day):
    sources = [row] if row.get("type") == "source" else [catalogue.records[s] for s in row.get("source_refs", [])]
    if not sources:
        return ""
    oldest = min(source["last_checked"] for source in sources)
    age = (day - dt.date.fromisoformat(oldest)).days
    if age <= 30:
        return ""
    return f"\n\n> **Source review due:** the oldest linked source check was {oldest} ({age} days before this publication). Historical observations are retained; review current upstream state before relying on a current-status claim.\n"


def stage_site(catalogue, revision=None, timestamp=None):
    root = catalogue.root
    stage = (root / ".build/docs").resolve()
    if stage != root / ".build/docs" or not stage.is_relative_to(root):
        raise ValueError("Refusing site staging cleanup outside the resolved checkout .build/docs directory.")
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    publication_day = dt.datetime.fromisoformat(timestamp).date() if timestamp else dt.datetime.now(dt.timezone.utc).date()
    record_pages = {view_path(row): row for row in catalogue.records.values()}
    record_pages.update({camera_research_path(row): row for row in catalogue.of_type("camera")})
    mapping = {}
    for directory in ("docs", "knowledge", "views"):
        for source in (root / directory).rglob("*"):
            if source.is_file():
                relative = source.relative_to(root)
                target_relative = source.relative_to(root / "docs") if directory == "docs" else relative
                mapping[source.resolve()] = stage / target_relative
    for source, destination in mapping.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix != ".md":
            shutil.copyfile(source, destination)
            continue
        text = source.read_text(encoding="utf-8")
        origin = source.relative_to(root).as_posix()
        record = record_pages.get(origin)
        if record:
            text += review_notice(catalogue, record, publication_day)
            if origin == view_path(record):
                metadata = yaml.safe_dump({"title": record["title"]}, allow_unicode=True)
                text = f"---\n{metadata}---\n\n{text}"
        if "<!-- atlas:camera-finder -->" in text:
            text = text.replace("<!-- atlas:camera-finder -->", camera_finder(catalogue, origin))
        if "<!-- atlas:research-finder -->" in text:
            text = text.replace("<!-- atlas:research-finder -->", camera_finder(catalogue, origin, research=True))
        if "<!-- atlas:recent-findings -->" in text:
            text = text.replace("<!-- atlas:recent-findings -->", recent_findings(catalogue, origin))
        if "<!-- atlas:showcase -->" in text:
            text = text.replace("<!-- atlas:showcase -->", showcase(catalogue, origin))
        if "<!-- atlas:counts -->" in text:
            text = text.replace("<!-- atlas:counts -->", atlas_counts(catalogue))
        if "<!-- atlas:people -->" in text:
            text = text.replace("<!-- atlas:people -->", people_markdown(catalogue, source.relative_to(root).as_posix()))

        def rewrite(match):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                return match.group(0)
            path, separator, fragment = target.partition("#")
            resolved = (source.parent / path).resolve()
            if resolved in mapping:
                rewritten = os.path.relpath(mapping[resolved], destination.parent).replace(os.sep, "/")
            elif resolved.is_relative_to(root):
                rewritten = f"{REPO}/blob/main/{resolved.relative_to(root).as_posix()}"
            else:
                raise ValueError(f"{source}: link leaves checkout: {target}")
            return match.group(0).replace(target, rewritten + (separator + fragment if separator else ""), 1)

        # Code examples are not links; preserve fenced blocks byte-for-byte.
        chunks = re.split(r"(```.*?```)", text, flags=re.S)
        text = "".join(chunk if chunk.startswith("```") else LINK_RE.sub(rewrite, chunk) for chunk in chunks)
        if source.relative_to(root).as_posix() not in {"docs/404.md", "docs/index.md"}:
            text += f"\n\n---\n[View this page's source]({REPO}/blob/main/{source.relative_to(root).as_posix()})\n"
        destination.write_text(text, encoding="utf-8", newline="\n")
    if revision is None:
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    timestamp = timestamp or dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    config = read_yaml(root / "mkdocs.yml")
    config.update(docs_dir=str(stage), site_dir=str(root / "site"))
    config["theme"]["custom_dir"] = str(root / "overrides")
    config["extra"] = dict(config.get("extra", {}), atlas_revision=revision, atlas_built_at=timestamp)
    config["extra"]["atlas_cameras"] = [
        {"title": row["title"], "codes": row["model_codes"], "aliases": row["aliases"],
         "owner": view_path(row).removesuffix(".md") + "/", "research": camera_research_path(row).removesuffix(".md") + "/"}
        for row in catalogue.of_type("camera")
    ]
    config_path = root / ".build/mkdocs.yml"
    config_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
    return config_path


def get_remote(url, json_response=False):
    headers = {"User-Agent": "OM-Firmware-Atlas-source-check/1"}
    if url.startswith("https://api.github.com/"):
        headers["Accept"] = "application/vnd.github+json"
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = "Bearer " + token
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=12) as response:
        payload = response.read(4 * 1024 * 1024 + 1)
        if len(payload) > 4 * 1024 * 1024:
            raise ValueError("Source response exceeds the bounded 4 MiB check; inspect it manually.")
        return json.loads(payload) if json_response else response.status


def inspect_remote(source, fetcher=get_remote, cache=None):
    cache = cache if cache is not None else {}

    def fetch(url, as_json=True):
        if url not in cache:
            cache[url] = fetcher(url, json_response=as_json)
        return cache[url]

    try:
        repo = source.get("upstream_repo")
        kind = source["source_kind"]
        if kind == "github-file":
            data = fetch(f"https://api.github.com/repos/{repo}/commits?per_page=1")
            head = data[0]["sha"]
            return dict(state="revision-match" if head == source["revision"] else "upstream-advanced", observed_revision=head,
                        note="Repository-head comparison only; inspect the scoped file before changing assertions.")
        if kind == "github-release":
            # Newest release including pre-releases, so test versions are noticed too.
            listing = fetch(f"https://api.github.com/repos/{repo}/releases?per_page=1")
            if not listing:
                return dict(state="no-releases", note="The repository lists no releases.")
            data = listing[0]
            digest = hashlib.sha256((data.get("body") or "").encode()).hexdigest()
            changed = data["tag_name"] != source["revision"]
            state = "new-release" if changed else ("text-changed" if source.get("content_sha256") and digest != source["content_sha256"] else "tag-match-text-untracked" if not source.get("content_sha256") else "unchanged")
            return dict(state=state, observed_revision=data["tag_name"], content_sha256=digest,
                        note="No source record or substantive review date was modified.")
        if kind == "github-comment":
            comment = source["url"].split("issuecomment-", 1)[1]
            data = fetch(f"https://api.github.com/repos/{repo}/issues/comments/{comment}")
            digest = hashlib.sha256((data.get("body") or "").encode()).hexdigest()
            state = "text-untracked" if not source.get("content_sha256") else "unchanged" if digest == source["content_sha256"] else "text-changed"
            return dict(state=state, content_sha256=digest, note="Comment text may change; record a reviewed baseline to compare it.")
        status = fetch(source["url"], False)
        return dict(state="reachable", http_status=status, note="Reachability only; activity and content were not validated.")
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, KeyError, IndexError, AttributeError, TypeError) as exc:
        return dict(state="check-failed", note=f"{type(exc).__name__}: {exc}. Previous evidence and dates remain unchanged.")


def github_repo(url):
    match = re.match(r"https://github\.com/([^/]+/[^/#?]+)", url or "")
    return match.group(1).removesuffix(".git") if match else None


def project_releases(project, fetcher, cache):
    """Compare a project's newest upstream release with the newest one recorded in its showcase."""
    repo = github_repo(project["url"])
    recorded = [r["tag"] for r in project.get("releases", [])]
    row = dict(id=project["id"], title=project["title"], recorded_latest=recorded[0] if recorded else None)
    if not repo:
        return dict(row, state="not-github")
    url = f"https://api.github.com/repos/{repo}/releases?per_page=1"
    try:
        if url not in cache:
            cache[url] = fetcher(url, json_response=True)
        listing = cache[url]
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
        return dict(row, state="check-failed", note=f"{type(exc).__name__}: {exc}")
    if not listing:
        return dict(row, state="no-releases-upstream")
    newest = listing[0]
    row.update(upstream_latest=newest.get("tag_name"), upstream_url=newest.get("html_url"),
               upstream_published=(newest.get("published_at") or "")[:10], upstream_prerelease=bool(newest.get("prerelease")))
    row["state"] = "releases-current" if newest.get("tag_name") in recorded else "release-not-catalogued"
    return row


def freshness(catalogue, fetch=False, today=None, fetcher=get_remote):
    today = today or dt.datetime.now(dt.timezone.utc).date()
    cache = {}
    rows = []
    for source in catalogue.of_type("source"):
        age = (today - dt.date.fromisoformat(source["last_checked"])).days
        row = dict(id=source["id"], url=source["url"], last_checked=source["last_checked"], age_days=age,
                   review_due=age > 30, state="not-fetched")
        if fetch:
            row.update(inspect_remote(source, fetcher, cache))
        rows.append(row)
    projects = [project_releases(p, fetcher, cache) if fetch else dict(id=p["id"], title=p["title"], state="not-fetched")
                for p in catalogue.of_type("project")]
    return dict(checked_on=today.isoformat(), network_used=fetch, sources=rows, projects=projects)


QUEUE_PROMPT = """Read AGENTS.md and follow agents/start.md in xulfr/om-firmware-atlas, using the freshness job.
Work through this update queue: for each new release, read its notes and add it to the project's releases
(and features, if it adds or changes one); for each changed source, review it and update the records it supports.
Keep claims attributed and scoped, regenerate, run the checks, tests and build, and open one focused PR.
Do not approve or merge it."""


def update_queue(report):
    """Markdown for the weekly update-queue issue. It lists work; it changes nothing."""
    lines = [f"Weekly source and release check, {report['checked_on']}. Generated by `python scripts/atlas.py queue`; "
             "nothing in the Atlas has been changed.", ""]
    releases = [p for p in report.get("projects", []) if p["state"] == "release-not-catalogued"]
    changed = [s for s in report["sources"] if s["state"] in ("upstream-advanced", "new-release", "text-changed")]
    failed = [s for s in report["sources"] if s["state"] == "check-failed"] + \
             [p for p in report.get("projects", []) if p["state"] == "check-failed"]
    due = [s for s in report["sources"] if s.get("review_due")]
    lines += ["## New releases to add", ""]
    lines += [f"- [ ] **{p['title']}**: [{p['upstream_latest']}]({p['upstream_url']})"
              f"{' (pre-release)' if p.get('upstream_prerelease') else ''}, published {p['upstream_published']}. "
              f"Newest recorded: {p['recorded_latest'] or 'none'}." for p in releases] or ["None."]
    lines += ["", "## Changed sources to review", ""]
    lines += [f"- [ ] `{s['id']}` ({s['state']}): {s['url']}" for s in changed] or ["None."]
    lines += ["", "## Reviews due (last checked more than 30 days ago)", ""]
    lines += [f"- [ ] `{s['id']}`, last checked {s['last_checked']}" for s in due] or ["None."]
    if failed:
        lines += ["", "## Checks that failed", ""]
        lines += [f"- `{row['id']}`: {row.get('note', 'see the report artifact')}" for row in failed]
    lines += ["", "## Hand this to an agent", "", "```text", QUEUE_PROMPT, "```", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["validate", "generate", "check", "build", "route", "freshness", "queue"])
    parser.add_argument("--job", default="research")
    parser.add_argument("--camera")
    parser.add_argument("--topic")
    parser.add_argument("--project")
    parser.add_argument("--source")
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()
    catalogue = Catalogue(ROOT)
    errors = catalogue.validate()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    if args.command == "generate":
        outputs = render(catalogue)
        write_generated(ROOT, outputs)
        print(f"Generated {len(outputs)} views/routes from {len(catalogue.records)} records and {len(catalogue.articles)} guides.")
    elif args.command in ("validate", "check", "build"):
        errors = checked(catalogue, generated=args.command != "validate", links=args.command != "validate")
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        print(f"Atlas validation passed: {len(catalogue.records)} records, {len(catalogue.articles)} guides.")
        if args.command == "build":
            config = stage_site(catalogue)
            return subprocess.call([sys.executable, "-m", "mkdocs", "build", "--strict", "--config-file", str(config)], cwd=ROOT)
    elif args.command == "route":
        try:
            plan = catalogue.reading_plan(args.job, args.camera, args.topic, args.project, args.source)
        except ValueError as exc:
            print(exc, file=sys.stderr)
            return 2
        for path in plan:
            size, tokens = cost(ROOT / path)
            print(f"{path} | {size} bytes | ~{tokens} tokens")
        print("Approximate cost uses ceil(UTF-8 bytes / 4); read only what the route requires.")
    elif args.command == "queue":
        report_path = ROOT / ".build/freshness.json"
        if not report_path.exists():
            print("Run python scripts/atlas.py freshness --fetch first.", file=sys.stderr)
            return 1
        queue_path = ROOT / ".build/update-queue.md"
        queue_path.write_text(update_queue(json.loads(report_path.read_text(encoding="utf-8"))), encoding="utf-8")
        print(f"Wrote {queue_path.relative_to(ROOT)}.")
    else:
        report = freshness(catalogue, fetch=args.fetch)
        path = ROOT / ".build/freshness.json"
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        from collections import Counter
        print(json.dumps(dict(Counter(row["state"] for row in report["sources"])), sort_keys=True))
        print(f"Review report: {path}. No canonical records or dates changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
