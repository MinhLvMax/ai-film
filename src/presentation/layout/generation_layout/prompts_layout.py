import streamlit as st
import pandas as pd
from src.presentation.app_state import AppState
from src.presentation.components import UIString, read_uploaded_file, print_data_table
from src.presentation.actions import create_prompt
from src.presentation.actions import send_prompts_video_only


async def prompts_layout(state: AppState):
    state.style_lock = st.text_area(
        label=UIString.STYLE_LOCK_LABEL,
        placeholder=UIString.STYLE_LOCK_PLACEHOLDER,
        value=state.style_lock or ''
    )

    gen_all_prompts = st.button(
        UIString.GEN_PROMPT,
        use_container_width=True,
        key="gen_all_prompts",
        disabled=not state.characters and not state.shots,
    )

    if gen_all_prompts:
        await create_prompt(state)

    uploaded_prompt_file = st.file_uploader(
        label=UIString.UPLOAD_PROMPT_LABEL,
        type=["xlsx", 'csv']
    )

    if not state.prompts and uploaded_prompt_file is not None:
        state.prompts = read_uploaded_file(uploaded_prompt_file)

    auto_send_btn = st.button(
        UIString.SEND_ALL,
        use_container_width=True,
        key="prompts_generate_all",
        disabled=not state.prompts,
    )
    table = st.empty()
    if auto_send_btn:
        await send_prompts_video_only(state, table)

    table.dataframe(pd.json_normalize(state.prompts))

    # if state.prompts:
    #     print_data_table(state.prompts)
