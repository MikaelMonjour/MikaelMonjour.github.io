#!/usr/bin/env python3
"""Capture des screenshots de chaque page du blog avec Playwright."""

import subprocess
import sys
import time
import signal
import os
from pathlib import Path

# Chemins
ROOT = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = Path(__file__).resolve().parent / "screenshots"
SCREENSHOTS_DIR.mkdir(exist_ok=True)

# Port du serveur local
PORT = 5050
BASE_URL = f"http://localhost:{PORT}"

# Pages à capturer : (slug fichier HTML, nom screenshot)
PAGES = [
    ("index.html", "accueil"),
    ("le-module-regex-python-guide-complet.html", "regex"),
    ("tcpdump-guide-complet.html", "tcpdump"),
    ("programmation-socket-python-guide-complet.html", "socket"),
    ("la-signification-de-la-valeur-p-exemple-python.html", "p-value"),
    ("recon-everything-guide-growth-hacker-securite.html", "recon"),
    ("mes-lectures-tech-incontournables-top-10.html", "lectures"),
    ("archives.html", "archives"),
]

# Viewports
VIEWPORTS = {
    "desktop": {"width": 1280, "height": 900},
    "mobile": {"width": 390, "height": 844},
}


def start_server():
    """Lancer un serveur HTTP local en arrière-plan."""
    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT)],
        cwd=str(ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1)
    return proc


def take_screenshots():
    """Prendre les screenshots avec Playwright."""
    from playwright.sync_api import sync_playwright

    server = start_server()
    print(f"✓ Serveur local démarré sur {BASE_URL}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()

            for viewport_name, viewport_size in VIEWPORTS.items():
                context = browser.new_context(
                    viewport=viewport_size,
                    device_scale_factor=2,
                )
                page = context.new_page()

                for html_file, name in PAGES:
                    url = f"{BASE_URL}/{html_file}"
                    filename = f"{name}_{viewport_name}.png"
                    filepath = SCREENSHOTS_DIR / filename

                    try:
                        page.goto(url, wait_until="networkidle", timeout=15000)
                        # Attendre que Mermaid se charge si présent
                        page.wait_for_timeout(1500)
                        page.screenshot(path=str(filepath), full_page=False)
                        print(f"  📸 {filename}")
                    except Exception as e:
                        print(f"  ⚠ {filename} — erreur : {e}")

                context.close()

            browser.close()
            print(f"\n✓ {len(PAGES) * len(VIEWPORTS)} screenshots dans .playwright/screenshots/")

    finally:
        server.terminate()
        server.wait()
        print("✓ Serveur arrêté")


if __name__ == "__main__":
    take_screenshots()
