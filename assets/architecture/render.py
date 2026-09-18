"""Render architektura.html (full view plus one focused view per exercise) and konteksty.html to PNG files.

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
    # context graphics for exercises 1 and 2 (height follows the content)
    for name, view in {"dane-cw1.png": "dane1", "dane-cw2.png": "dane2", "bronze-landing.png": "bronze"}.items():
        page.goto((HERE / "konteksty.html").as_uri() + f"?view={view}")
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready")
        page.locator(".stage.show").screenshot(path=str(HERE / name), omit_background=True)
        print("rendered", name)
    browser.close()
