import streamlit as st
from src.presentation.components import UIString, download_excel_btn, select_model, print_data_table
from src.presentation.actions import characters_analyze
from src.presentation.app_state import AppState


async def characters_layout(state: AppState):
    state.extract_chars_prompt = st.text_area(
        label=UIString.characters_prompt_label,
        placeholder=UIString.characters_prompt_placeholder,
        key='characters_extract_prompt'
    )
    select_model(key='characters_model')
    extract_chars_btn = st.button(
        UIString.ANALYSIS,
        use_container_width=True,
        disabled=not state.script_content or not state.extract_chars_prompt
    )

    if extract_chars_btn:
        with st.spinner(UIString.ANALYZING):
            await characters_analyze(state)

    if state.characters:
        print_data_table(state.characters)
