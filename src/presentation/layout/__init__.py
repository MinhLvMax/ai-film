import streamlit as st
from src.presentation.components import UIString
from src.presentation.actions import sign_in, export_state
from src.presentation.layout.script_layout import script_layout
from src.presentation.layout.generation_layout import generation_layout
from src.presentation.app_state import AppState


async def main():
    state = AppState().get_state()
    st.set_page_config(
        page_title=UIString.page_title,
        layout="wide"
    )


    sign_in_col, export_col, _ = st.columns(
        [1, 1, 8]
    )

    with sign_in_col:
        sign_in_btn = st.button(
            label=UIString.SIGN_IN,
            use_container_width=True,
        )

    with export_col:
        export_btn = st.button(
            label="Export",
            use_container_width=True,
        )
        if export_btn:
            await export_state(state)

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

    state.save()
