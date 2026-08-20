import streamlit as st
from src.presentation.components import UIString, get_uploaded_text
from src.presentation.actions import analysis_script


async def script_layout():
    uploaded_script_file = st.file_uploader(
        label=UIString.UPLOAD_LABEL,
        type=["csv", "txt"]
    )

    st.session_state['script_content'] = st.text_area(
        label=UIString.SCRIPT_CONTENT_LABEL,
        placeholder=UIString.SCRIPT_PLACE_HOLDER,
        value=get_uploaded_text(uploaded_script_file),
        height='content'
    )

    analysis_btn = st.button(
        UIString.SCRIPT_ANALYSIS_LABEL,
        use_container_width=True,
        help=UIString.SCRIPT_ANALYZE_HELP,
        key="script_analyze",
    )

    if analysis_btn:
        await analysis_script()
