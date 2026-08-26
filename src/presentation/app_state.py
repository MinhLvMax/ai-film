import json
import streamlit as st
from typing import Self
from src.config import Config


class AppState:
    STATE_FILE = Config.STREAMLIT_UI_STATE_FILE

    def __init__(self):
        self.script_content = None

        self.extract_chars_prompt = None
        self.extract_chars_model = None
        self.characters: list[dict] | None = None

        self.extract_shots_prompt = None
        self.extract_shots_model = None
        self.shots: list[dict] | None = None

        self.style_lock = None
        self.prompts: list[dict] | None = None

        self.project_name: str | None = None

        self.image_ratio: str | None = None
        self.image_gen_model: str | None = None
        self.image_quality: int | None = None

        self.video_gen_mode: str | None = None
        self.video_ratio: str | None = None
        self.video_gen_model: str | None = None
        self.video_duration: int | None = None
        self.video_quality: int | None = None
        self.max_creating_video: int | float | None = None

    def save(self):
        """Lưu trạng thái ứng dụng xuống file."""
        print(f"[STATE] File path: {self.STATE_FILE}")
        print(f"[STATE] Absolute path: {self.STATE_FILE.resolve()}")
        with open(self.STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(
                self.__dict__,
                f,
                ensure_ascii=False,
                indent=2,
            )

    @classmethod
    def get_state(cls) -> Self:
        if "app_state" not in st.session_state:

            state = cls()

            if cls.STATE_FILE.exists():
                with open(cls.STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)

                for key, value in data.items():
                    if hasattr(state, key):
                        setattr(state, key, value)

            st.session_state["app_state"] = state

        return st.session_state["app_state"]
