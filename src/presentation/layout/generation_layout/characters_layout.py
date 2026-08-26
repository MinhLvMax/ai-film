import streamlit as st
from src.presentation.components import UIString, read_uploaded_file, select_model, print_data_table
from src.presentation.actions import characters_analyze
from src.presentation.app_state import AppState


async def characters_layout(state: AppState):
    state.extract_chars_prompt = st.text_area(
        label=UIString.characters_prompt_label,
        placeholder=UIString.characters_prompt_placeholder,
        key='characters_extract_prompt',
        value=state.extract_chars_prompt or '',
    )
    select_model(key='characters_model')
    uploaded_char_file = st.file_uploader(
        label=UIString.UPLOAD_CHAR_LABEL,
        type=["xlsx", 'csv']
    )
    extract_chars_btn = st.button(
        UIString.ANALYSIS,
        use_container_width=True,
        disabled=not state.script_content or not state.extract_chars_prompt or uploaded_char_file is not None
    )
    # Bên trên trình bày bên dưới xử lý sự kiện
    if extract_chars_btn:
        with st.spinner(UIString.ANALYZING):
            await characters_analyze(state)
    if uploaded_char_file is not None:
        state.characters = read_uploaded_file(uploaded_char_file)
    if state.characters:
        print_data_table(state.characters)
