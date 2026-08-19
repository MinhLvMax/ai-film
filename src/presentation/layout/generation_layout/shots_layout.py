import streamlit as st
from src.presentation.components import UIString, download_excel_btn


def shots_layout():
    st.text_area(
        label=UIString.shots_prompt_label,
        placeholder=UIString.shots_prompt_placeholder,
    )

    shots_data = st.session_state.get('shots', None)
    download_excel_btn(
        label=UIString.EXPORT_DATA_LABEL,
        data=shots_data,
        file_name='shots.xlsx',
        key='shots_export'
    )
