from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile


def capture_url(url: str, dest: Path, timeout_s: int = 20) -> Path:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    dest.parent.mkdir(parents=True, exist_ok=True)
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,720")
    driver = webdriver.Chrome(options=opts)
    try:
        driver.set_page_load_timeout(timeout_s)
        driver.get(url)
        driver.save_screenshot(str(dest))
    finally:
        driver.quit()
    return dest


def capture_domain(domain: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / "console"
        subprocess.run(["virsh", "screenshot", domain, str(raw)], check=True)
        shots = list(Path(tmp).glob("console*"))
        if not shots:
            raise FileNotFoundError(f"virsh screenshot produced no file for {domain}")
        dest.write_bytes(shots[0].read_bytes())
    return dest
