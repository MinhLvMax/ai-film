import streamlit as st
from src.presentation.components import UIString
from src.presentation.actions import sign_in
from src.presentation.layout.script_layout import script_layout
from src.presentation.layout.generation_layout import generation_layout
from src.presentation.app_state import AppState


async def main():
    state = AppState().get_state()
    st.set_page_config(
        page_title=UIString.page_title,
        layout="wide"
    )
    sign_in_btn = st.button(
        label=UIString.SIGN_IN,
    )
    st.caption(UIString.page_caption)

    script_workspace, generation_workspace = st.columns(
        [1, 3],
        gap="small",
        vertical_alignment="top",
        border=True,
    )

    with script_workspace:
        await script_layout(state)

    with generation_workspace:
        await generation_layout(state)


    if sign_in_btn:
        await sign_in()