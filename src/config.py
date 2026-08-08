import os
from dotenv import load_dotenv
from pathlib import Path


class Config:
    PROJECT_PATH = Path(__file__).resolve().parents[1]  # Đường dẫn file chính của dự án

    LOGFILES = PROJECT_PATH / "logfiles"  # Đường dẫn đến folder chứa các file log
    LOGFILES.mkdir(exist_ok=True)  # Tạo folder chứa các file log nếu chưa có

    ENV_PATH = Path(PROJECT_PATH) / ".env"
    if not ENV_PATH.exists():
        ENV_PATH.write_text("GROQ_API_KEY=")

    load_dotenv()  # Load các biến môi trường ở file .env
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Load GROQ_API_KEY từ biến môi trường

if __name__ == '__main__':
    print(Config.PROJECT_PATH)
