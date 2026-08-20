import streamlit as st
from src.presentation.components import UIString, download_excel_btn, select_model, print_data_table
from src.presentation.actions import characters_analyze


async def characters_layout():
    st.text_area(
        label=UIString.characters_prompt_label,
        placeholder=UIString.characters_prompt_placeholder,
        key='characters_extract_prompt'
    )
    select_model(key='characters_model')
    col1, col2 = st.columns(2)
    with col1:
        download_excel_btn(
            label=UIString.EXPORT_DATA_LABEL,
            data=st.session_state.get('characters', None),
            file_name='characters.xlsx',
        )
    with col2:
        extract_chars_btn = st.button(
            UIString.ANALYSIS,
            use_container_width=True,
            disabled=not st.session_state.get('script_content', None),
        )
    if extract_chars_btn:
        await characters_analyze()
        print_data_table(st.session_state['chars'])
