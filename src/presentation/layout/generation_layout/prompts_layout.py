import streamlit as st
from src.presentation.components import UIString, download_excel_btn, print_data_table
from src.presentation.actions import send_prompts


async def prompts_layout():
    style_lock = st.text_area(
        label=UIString.STYLE_LOCK_LABEL,
        placeholder=UIString.STYLE_LOCK_PLACEHOLDER,
    )
    uploaded_prompt_file = st.file_uploader(
        label=UIString.UPLOAD_PROMPT_LABEL,
        type=["xlsx", 'csv']
    )
    prompts_data = st.session_state.get('prompts', None)
    col1, col2 = st.columns(2)
    with col1:
        download_excel_btn(
            label=UIString.EXPORT_DATA_LABEL,
            data=prompts_data,
            file_name='prompts.xlsx',
        )
    with col2:
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
