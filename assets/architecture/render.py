"""Render architektura.html to PNG files (full view plus one focused view per exercise).

Usage: python render.py            # needs: pip install playwright && playwright install chromium
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
VIEWS = {"architektura.png": "", **{f"architektura-cw{n}.png": f"?focus={n}" for n in range(0, 7)}}

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1600, "height": 900}, device_scale_factor=1.5)
    for name, query in VIEWS.items():
        page.goto((HERE / "architektura.html").as_uri() + query)
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready")
        page.locator(".stage").screenshot(path=str(HERE / name), omit_background=True)
        print("rendered", name)
    browser.close()
