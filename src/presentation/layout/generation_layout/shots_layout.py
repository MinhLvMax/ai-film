import streamlit as st
from src.presentation.components import UIString, download_excel_btn, select_model, print_data_table
from src.presentation.actions import shots_analyze


async def shots_layout():
    prompt = st.text_area(
        label=UIString.shots_prompt_label,
        placeholder=UIString.shots_prompt_placeholder,
    )
    model = select_model(key='shots_model')
    shots_data = st.session_state.get('shots', None)
    col1, col2 = st.columns(2)
    with col1:
        download_excel_btn(
            label=UIString.EXPORT_DATA_LABEL,
            data=shots_data,
            file_name='shots.xlsx',
        )
    with col2:
        extract_shots_btn = st.button(
            UIString.ANALYSIS,
            use_container_width=True,
            key="shots_analyze",
        )
    if extract_shots_btn:
        await shots_analyze(model=model, prompt=prompt, content=shots_data)
    if shots_data:
        print_data_table(data=shots_data)
