from pathlib import Path
import subprocess
from src.config import Config


def run_cli(*command, workdir=Config.PROJECT_PATH, **kwargs):
    print('[RUN]', command)
    return subprocess.run(
        [str(c) for c in command],
        cwd=Path(workdir),
        text=True,
        check=True,
        **kwargs,
    )
