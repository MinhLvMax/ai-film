from pathlib import Path
import subprocess
from src.config import Config


async def login_profile():
    CHROME_PATH = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

    cmd = [
        CHROME_PATH,
        f"--user-data-dir={Config.BROWSER_PROFILES}"
    ]

    subprocess.Popen(cmd)
