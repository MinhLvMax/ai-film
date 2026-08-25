import streamlit as st
from typing import Self


class AppState:
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

    @classmethod
    def get_state(cls) -> Self:
        if "app_state" not in st.session_state:
            st.session_state["app_state"] = cls()
        return st.session_state["app_state"]
