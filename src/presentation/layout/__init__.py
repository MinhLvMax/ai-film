import streamlit as st
from src.presentation.components import UIString
from src.presentation.layout.script_layout import script_layout
from src.presentation.layout.generation_layout import generation_layout


async def main():
    st.set_page_config(
        page_title=UIString.page_title,
        layout="wide"
    )

    st.caption(UIString.page_caption)

    script_workspace, generation_workspace = st.columns(
        [1, 2],
        gap="small",
        vertical_alignment="top",
        border=True,
    )

    with script_workspace:
        await script_layout()

    with generation_workspace:
        await generation_layout()
