"""Exercise owner and developer journeys against a built Atlas served over HTTP."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import re
from pathlib import Path
from threading import Thread

from playwright.sync_api import expect, sync_playwright


class SiteHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def open_search(page):
    # A URL assertion passes when navigation commits; the deferred atlas.js binds "/" by DOMContentLoaded.
    page.wait_for_load_state("domcontentloaded")
    page.keyboard.press("/")


def owner_journey(page, base, phone):
    page.goto(base)
    finder = page.get_by_label("Find your camera")
    finder.fill("OM-5")
    matches = page.locator(".finder-results a:visible")
    expect(matches).to_have_count(2)
    finder.press("Enter")
    expect(page).to_have_url(base)
    finder.fill("E148")
    finder.press("Enter")
    expect(page).to_have_url(base + "views/cameras/om5-ii/")
    expect(page.locator("#primary-nav").get_by_text("For camera owners", exact=True)).to_have_attribute(
        "aria-current", "true")
    project = page.locator(".model-panel:has(> #caduceus-om5)")
    guide = project.get_by_role("link", name="Install guide")
    expect(guide).to_be_in_viewport()
    expect(project.get_by_role("link", name="Full project details")).to_have_attribute(
        "href", re.compile(r"caduceus-om5/#for-om5-ii$"))
    # Click the actual link with pointer hit testing. Do not fetch upstream.
    destination = guide.evaluate("a => a.href")
    page.route(destination, lambda route: route.fulfill(content_type="text/plain", body="Install guide"))
    guide.click()
    expect(page).to_have_url(destination)
    page.go_back()

    project.locator("summary").click()
    expect(project.get_by_role("img")).to_have_attribute("src", re.compile(r"picture-mode-look\.png$"))

    page.goto(base + "views/showcases/om5-ii/#omkit")
    expect(page).to_have_url(base + "views/cameras/om5-ii/#omkit")
    page.get_by_role("link", name="Developer research for this camera").click()
    expect(page).to_have_url(base + "views/research/om5-ii/")
    page.get_by_role("link", name="Mods & installation for this camera").click()
    expect(page).to_have_url(base + "views/cameras/om5-ii/")

    open_search(page)
    search = page.get_by_role("searchbox", name="Search terms")
    expect(search).to_be_focused()
    search.fill("OM-5")
    expect(page.locator(".search-models article:visible")).to_have_count(2)
    search.press("Enter")
    expect(page).to_have_url(base + "views/cameras/om5-ii/")
    search.fill("OM-5 Mark II")
    expect(page.locator(".search-models article:visible")).to_have_count(1)
    search.press("Enter")
    expect(page).to_have_url(base + "views/cameras/om5-ii/")

    page.goto(base + "views/cameras/om5/")
    expect(page.get_by_role("link", name="Install guide", exact=True)).to_have_count(0)
    expect(page.get_by_role("link", name="Read release notes")).to_be_visible()
    expect(page.get_by_role("heading", name="In development")).to_be_visible()

    if phone:
        menu = page.locator("[data-menu-toggle]")
        menu.focus()
        page.keyboard.press("Enter")
        expect(page.locator("#primary-nav a").first).to_be_focused()
        page.keyboard.press("Escape")
        expect(menu).to_be_focused()
        expect(menu).to_have_attribute("aria-expanded", "false")


def truepic_journey(page, base):
    page.goto(base + "views/cameras/")
    page.get_by_role("link", name="Browse cameras by TruePic generation").click()
    expect(page).to_have_url(base + "truepic-generations/")
    expect(page.get_by_role("heading", name="Cameras by TruePic generation")).to_be_visible()
    artwork = page.get_by_role("img", name=re.compile(r"^TruePic generations at a glance"))
    expect(artwork).to_be_visible()
    expect(artwork).to_have_js_property("naturalWidth", 1200)
    expect(page.locator("main").get_by_role("heading", level=2, name=re.compile(r"^TruePic "))).to_have_count(6)
    page.get_by_role("link", name="E-PM2", exact=True).click()
    expect(page).to_have_url(base + "views/cameras/epm2/")


def developer_journey(page, base, phone):
    page.goto(base + "views/evidence/om5-ii-v020-alpha1-owner/")
    if phone:
        page.locator("[data-menu-toggle]").click()
    page.locator("#primary-nav").get_by_role("link", name="For developers").click()
    expect(page).to_have_url(base + "research/")
    expect(page.get_by_role("heading", name="Recent research findings")).to_be_visible()
    page.get_by_role("link", name="By topic", exact=True).click()
    page.get_by_role("link", name="Display and drawing").click()
    expect(page).to_have_url(base + "knowledge/subsystems/display/")
    expect(page.get_by_role("link", name="Drawing to the screen")).to_be_visible()

    page.goto(base + "research/")
    finder = page.get_by_label("Find your camera")
    finder.fill("E148")
    finder.press("Enter")
    expect(page).to_have_url(base + "views/research/om5-ii/")
    page.get_by_role("link", name="Firmware & platform").click()
    expect(page).to_have_url(base + "views/research/om5-ii/#platform")
    page.get_by_role("link", name="File identity, platform and stock features").click()
    expect(page).to_have_url(base + "views/firmware/om5-ii-1100/")

    open_search(page)
    search = page.get_by_role("searchbox", name="Search terms")
    search.press_sequentially("Ghidra MN103")
    page.wait_for_function("""() => {
        if (document.querySelector('.search-results article:not([hidden]) .search-kind')) return true;
        document.querySelector('#mkdocs-search-query').dispatchEvent(new KeyboardEvent('keyup'));
        return false;
    }""", polling=200)
    result = page.locator('.search-results article:not([hidden])').first
    expect(result.locator('.search-kind')).to_have_text('Project or tool')
    expect(result.get_by_role('link')).to_have_attribute('href', re.compile(r'views/projects/ghidra-mn103/'))

    page.goto(base + "research/")
    page.get_by_role("link", name="Test evidence", exact=True).filter(visible=True).last.click()
    expect(page).to_have_url(base + "views/evidence/")
    expect(page.get_by_text("Camera test · reported working", exact=False).first).to_be_visible()
    expect(page.get_by_text("Emulator test ·", exact=False).first).to_be_visible()
    page.get_by_role("link", name="Use with AI").click()
    expect(page).to_have_url(base + "research-with-ai/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--executable", help="Optional path to an existing Chromium binary")
    parser.add_argument("--browser-arg", action="append", default=[])
    args = parser.parse_args()
    site = Path(__file__).resolve().parents[1] / "site"
    if not (site / "index.html").exists():
        parser.error("Build the Atlas before running the browser checks.")
    with ThreadingHTTPServer(("127.0.0.1", 0), partial(SiteHandler, directory=site)) as server:
        Thread(target=server.serve_forever, daemon=True).start()
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(executable_path=args.executable, args=args.browser_arg)
                for width, height in ((1440, 900), (390, 844)):
                    page = browser.new_page(viewport={"width": width, "height": height})
                    owner_journey(page, f"http://127.0.0.1:{server.server_port}/", width == 390)
                    developer_journey(page, f"http://127.0.0.1:{server.server_port}/", width == 390)
                    truepic_journey(page, f"http://127.0.0.1:{server.server_port}/")
                    print(f"Owner, developer and TruePic journeys passed at {width} x {height}")
                browser.close()
        finally:
            server.shutdown()
