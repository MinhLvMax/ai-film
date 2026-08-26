import streamlit as st
from src.presentation.components import UIString, read_uploaded_file, select_model, print_data_table
from src.presentation.actions import shots_analyze
from src.presentation.app_state import AppState


async def shots_layout(state: AppState):

    state.extract_shots_prompt = st.text_area(
        label=UIString.shots_prompt_label,
        placeholder=UIString.shots_prompt_placeholder,
        value=state.extract_shots_prompt or ''
    )

    state.extract_shots_model = select_model(key='shots_model')
    uploaded_shots_file = st.file_uploader(
        label=UIString.UPLOAD_SHOT_LABEL,
        type=["xlsx", 'csv']
    )

    extract_shots_btn = st.button(
        UIString.ANALYSIS,
        use_container_width=True,
        key="shots_analyze",
        disabled=not state.script_content or not state.characters or uploaded_shots_file is not None,
    )

    if extract_shots_btn:
        with st.spinner(UIString.ANALYZING):
            await shots_analyze(state=state)
    if uploaded_shots_file is not None:
        state.shots = read_uploaded_file(uploaded_shots_file)
    if state.shots:
        print_data_table(state.shots)
