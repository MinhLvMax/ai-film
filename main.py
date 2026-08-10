import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

print("CWD =", os.getcwd())
print("MAIN =", __file__)
print("PYTHON =", sys.executable)
print("SYS.PATH =")

for path in sys.path:
    print("  ", path)

from src.presentation.file_ui import main

if __name__ == '__main__':
    main()
