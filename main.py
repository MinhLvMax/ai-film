import sys
import asyncio
from pathlib import Path
from src.presentation.layout import main

PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

asyncio.run(main())

# streamlit run main.py --server.runOnSave true
# streamlit run main.py --server.runOnSave false
