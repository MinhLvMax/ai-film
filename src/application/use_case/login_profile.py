from pathlib import Path
import subprocess
from src.config import Config
import os

BROWSER_PATHS = {
    "chrome": Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    "chrome-beta": Path(r"C:\Program Files\Google\Chrome Beta\Application\chrome.exe"),
    "chrome-dev": Path(r"C:\Program Files\Google\Chrome Dev\Application\chrome.exe"),
    "chrome-canary": Path(
        r"%LOCALAPPDATA%\Google\Chrome SxS\Application\chrome.exe"
    ),

    "msedge": Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    "msedge-beta": Path(r"C:\Program Files (x86)\Microsoft\Edge Beta\Application\msedge.exe"),
    "msedge-dev": Path(r"C:\Program Files (x86)\Microsoft\Edge Dev\Application\msedge.exe"),
    "msedge-canary": Path(r"C:\Program Files (x86)\Microsoft\Edge Canary\Application\msedge.exe"),

    "coc_coc": Path(
        r"C:\Program Files\CocCoc\Browser\Application\browser.exe"
    ),

    "opera": Path(
        r"%LOCALAPPDATA%\Programs\Opera\launcher.exe"
    ),
}

async def login_profile(browser: str | None = None):
    browser = browser or "chrome"
    browser_path = os.path.expandvars(BROWSER_PATHS[browser])

    if not Path(browser_path).exists():
        raise FileNotFoundError(
            f"Không tìm thấy browser: {browser_path}"
        )

    cmd = [
        browser_path,
        f"--user-data-dir={Config.BROWSER_PROFILES}",
    ]

    subprocess.Popen(cmd)
