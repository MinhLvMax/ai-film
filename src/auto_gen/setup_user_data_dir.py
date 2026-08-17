import subprocess
from pathlib import Path
from src.config import Config

USER_DATA_DIR = Config.PROJECT_PATH / r'src\auto_gen\profiles\user0'


def login_profile():
    CHROME_PATH = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    USER_DATA_DIR.mkdir(parents=True, exist_ok=True)

    cmd = [
        CHROME_PATH,
        f"--user-data-dir={USER_DATA_DIR}"
    ]

    subprocess.Popen(cmd)
