import streamlit as st
from src.presentation.components import UIString, download_excel_btn


def characters_layout():
    st.text_area(
        label=UIString.characters_prompt_label,
        placeholder=UIString.characters_prompt_placeholder,
    )

    characters_data = st.session_state.get('characters', None)
    download_excel_btn(
        label=UIString.EXPORT_DATA_LABEL,
        data=characters_data,
        file_name='characters.xlsx',
        key='characters_export'
    )
