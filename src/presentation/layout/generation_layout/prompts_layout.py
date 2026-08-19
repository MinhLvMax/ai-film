import streamlit as st
from src.presentation.components import UIString, download_excel_btn
from src.presentation.actions import send_prompts


async def prompts_layout():
    st.write(UIString.prompts_title)

    prompts_data = st.session_state.get('prompts', None)
    download_excel_btn(
        label=UIString.EXPORT_DATA_LABEL,
        data=prompts_data,
        file_name='prompts.xlsx',
        key='prompts_export'
    )

    auto_send_btn = st.button(
        UIString.SEND_ALL,
        use_container_width=True,
        key="prompts_generate_all",
        disabled=not prompts_data,
    )
    if auto_send_btn:
        await send_prompts()
