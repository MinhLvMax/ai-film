import streamlit as st
from src.presentation.components import UIString, download_excel_btn, select_model, print_data_table
from src.presentation.actions import shots_analyze
from src.presentation.app_state import AppState


async def shots_layout(state: AppState):
    state.extract_shots_prompt = st.text_area(
        label=UIString.shots_prompt_label,
        placeholder=UIString.shots_prompt_placeholder,
    )
    state.extract_shots_model = select_model(key='shots_model')
    col1, col2 = st.columns(2)
    with col1:
        extract_shots_btn = st.button(
            UIString.ANALYSIS,
            use_container_width=True,
            key="shots_analyze",
            disabled=not state.script_content or not state.characters,
        )
    with col2:
        gen_all_prompts = st.button(
            UIString.GEN_PROMPT,
            use_container_width=True,
            key="gen_all_prompts",
            disabled=not st.session_state.get('script_content', None),
        )
    if extract_shots_btn:
        with st.spinner(UIString.ANALYZING):
            await shots_analyze(state=state)
