"""Render sciaga-fabric.html to a one-page A4 PDF and a PNG preview.

Usage: python render.py            # needs: pip install playwright && playwright install chromium
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=2)
    page.goto((HERE / "sciaga-fabric.html").as_uri())
    page.wait_for_load_state("networkidle")
    page.evaluate("document.fonts.ready")
    overflow = page.evaluate("(() => { const m = document.querySelector('main'); return m.scrollHeight - m.clientHeight; })()")
    print("main overflow px:", overflow)
    page.pdf(path=str(HERE / "sciaga-fabric.pdf"), format="A4", print_background=True, prefer_css_page_size=True)
    page.screenshot(path=str(HERE / "sciaga-fabric-podglad.png"), full_page=False)
    browser.close()
