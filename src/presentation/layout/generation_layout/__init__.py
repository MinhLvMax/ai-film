import streamlit as st
from src.presentation.layout.generation_layout.characters_layout import characters_layout
from src.presentation.layout.generation_layout.shots_layout import shots_layout
from src.presentation.layout.generation_layout.prompts_layout import prompts_layout


async def generation_layout():
    characters_tab, shots_tab, prompts_tab = st.tabs(
        [
            "Characters",
            "Shots",
            "Prompts",
        ]
    )

    with characters_tab:
        await characters_layout()
    with shots_tab:
        await shots_layout()
    with prompts_tab:
        await prompts_layout()
