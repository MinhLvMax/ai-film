import sys
import asyncio
from pathlib import Path
from src.presentation.layout import main

PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Login profile nick đăng kí flow
from src.auto_gen.setup_user_data_dir import USER_DATA_DIR, login_profile

if not USER_DATA_DIR.exists():
    login_profile()

asyncio.run(main())
