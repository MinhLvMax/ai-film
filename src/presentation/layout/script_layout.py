import streamlit as st

from src.presentation.app_state import AppState
from src.presentation.components import UIString, get_uploaded_text


async def script_layout(state: AppState):
    uploaded_script_file = st.file_uploader(
        label=UIString.UPLOAD_LABEL,
        type=["csv", "txt"]
    )

    state.script_content = st.text_area(
        label=UIString.SCRIPT_CONTENT_LABEL,
        placeholder=UIString.SCRIPT_PLACE_HOLDER,
        value=state.script_content or get_uploaded_text(uploaded_script_file),
        height='content'
    )

    # analysis_btn = st.button(
    #     UIString.SCRIPT_ANALYSIS_LABEL,
    #     use_container_width=True,
    #     help=UIString.SCRIPT_ANALYZE_HELP,
    #     key="script_analyze",
    # )
    #
    # if analysis_btn:
    #     await analysis_script(state)
