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

# Login profile nick đăng kí flow
from src.auto_gen.setup_user_data_dir import USER_DATA_DIR, login_profile

if not USER_DATA_DIR.exists():
    login_profile()

# Chạy giao diện
from src.presentation.ui_streamlit import run

run()

if __name__ == '__main__':
    # from src.presentation.file_ui import main
    # main()

    # from nicegui import ui
    # from src.presentation.ui_nicegui_test import create_ui
    # from src.bootstrap import build_app
    #
    # def main():
    #     # 1. Khởi tạo toàn bộ dependency/use case
    #     app = build_app()
    #
    #     # 2. Truyền đối tượng bootstrap vào UI
    #     create_ui(app)
    #
    #     # 3. Chạy NiceGUI
    #     ui.run(
    #         title='AI Film Prompt Studio',
    #         reload=False,
    #     )
    # main()
    pass
