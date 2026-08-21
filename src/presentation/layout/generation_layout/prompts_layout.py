import streamlit as st

from src.presentation.app_state import AppState
from src.presentation.components import UIString, download_excel_btn, print_data_table
from src.presentation.actions import send_prompts


async def prompts_layout(state: AppState):
    style_lock = st.text_area(
        label=UIString.STYLE_LOCK_LABEL,
        placeholder=UIString.STYLE_LOCK_PLACEHOLDER,
    )

    prompts_data = st.session_state.get('prompts', None)

    uploaded_prompt_file = st.file_uploader(
        label=UIString.UPLOAD_PROMPT_LABEL,
        type=["xlsx", 'csv']
    )

    auto_send_btn = st.button(
        UIString.SEND_ALL,
        use_container_width=True,
        key="prompts_generate_all",
        disabled=not prompts_data,
    )
    if prompts_data is not None:
        print_data_table(prompts_data)

    if auto_send_btn:
        await send_prompts(prompts_data)
