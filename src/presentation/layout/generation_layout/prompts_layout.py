import streamlit as st
from src.presentation.app_state import AppState
from src.presentation.components import UIString, read_uploaded_file, print_data_table
from src.presentation.actions import create_prompt


async def prompts_layout(state: AppState):
    state.style_lock = st.text_area(
        label=UIString.STYLE_LOCK_LABEL,
        placeholder=UIString.STYLE_LOCK_PLACEHOLDER,
    )
    gen_all_prompts = st.button(
        UIString.GEN_PROMPT,
        use_container_width=True,
        key="gen_all_prompts",
        disabled=not state.characters and not state.shots,
    )
    uploaded_prompt_file = st.file_uploader(
        label=UIString.UPLOAD_PROMPT_LABEL,
        type=["xlsx", 'csv']
    )
    if uploaded_prompt_file is not None:
        state.prompts = read_uploaded_file(uploaded_prompt_file)
    if gen_all_prompts:
        await create_prompt(state)
    if state.prompts:
        print_data_table(state.prompts)
