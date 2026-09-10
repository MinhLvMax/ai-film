import json
from pathlib import Path
import pandas as pd
import streamlit as st
from typing import Self
from src.config import Config
from src.presentation.components import create_id


class AppState:
    STATE_FILE = Config.STREAMLIT_UI_STATE_FILE

    def __init__(self):
        self.script_content = None

        self.extract_chars_prompt = None
        self.extract_chars_model = None
        self.extract_chars_model_index: int | None = None
        self.characters: list[dict] | None = None

        self.extract_shots_prompt = None
        self.extract_shots_model = None
        self.extract_shots_model_index: int | None = None
        self.shots: list[dict] | None = None

        self.style_lock = None
        self.prompts: list[dict] | None = None

        # self.project_name: str | None = None
        self.project_url: str | None = None

        # self.image_ratio: str | None = None
        # self.image_gen_model: str | None = None
        # self.image_quality: int | None = None

        # self.video_gen_mode: str | None = None
        # self.video_ratio: str | None = None
        # self.video_gen_model: str | None = None
        # self.video_duration: int | None = None
        # self.video_quality: int | None = None
        # self.max_creating_video: int | float | None = None
        # self.is_downloaded: bool = False

        self.sleeptime = 30
        # self.browser_name = 'msedge'
        self.browser_name = 'chrome'

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

    def export(self):
        """Export các dữ liệu của AppState ra folder state."""
        downloads = Path.home() / "Downloads"
        export_dir = downloads / create_id(
            prefix='state'
        )

        export_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        # =========================
        # TXT
        # =========================

        self._write_txt(
            export_dir / "extract_chars_prompt.txt",
            self.extract_chars_prompt,
        )

        self._write_txt(
            export_dir / "extract_shots_prompt.txt",
            self.extract_shots_prompt,
        )

        self._write_txt(
            export_dir / "style_lock.txt",
            self.style_lock,
        )

        self._write_txt(
            export_dir / 'script_content.txt',
            self.script_content,
        )

        # =========================
        # CSV
        # =========================

        self._write_csv(
            export_dir / "characters.csv",
            self.characters,
        )

        self._write_csv(
            export_dir / "shots.csv",
            self.shots,
        )

        self._write_csv(
            export_dir / "prompts.csv",
            self.prompts,
        )

        print(
            f"[STATE] Exported to: "
            f"{export_dir.resolve()}"
        )
        st.toast("Export thành công")

    @staticmethod
    def _write_txt(
            path: Path,
            content: str | None,
    ):
        if content is None:
            return

        path.write_text(
            content,
            encoding="utf-8",
        )

    @staticmethod
    def _write_csv(
            path: Path,
            data: list[dict] | None,
    ):
        if not data:
            return

        df = pd.json_normalize(data)

        # Chuyển list/dict còn sót lại thành JSON string
        # để CSV đọc đẹp hơn.
        for column in df.columns:
            df[column] = df[column].apply(
                lambda value: json.dumps(
                    value,
                    ensure_ascii=False,
                )
                if isinstance(value, (list, dict))
                else value
            )

        df.to_csv(
            path,
            index=False,
            encoding="utf-8-sig",
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
