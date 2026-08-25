import streamlit as st
from src.presentation.layout.generation_layout.characters_layout import characters_layout
from src.presentation.layout.generation_layout.shots_layout import shots_layout
from src.presentation.layout.generation_layout.prompts_layout import prompts_layout
from src.presentation.layout.generation_layout.generate_layout import generate_layout
from src.presentation.app_state import AppState


async def generation_layout(state: AppState):
    characters_tab, shots_tab, prompts_tab, generate_tab = st.tabs(
        [
            "Characters",
            "Shots",
            "Prompts",
            'Generate'
        ]
    )

    with characters_tab:
        await characters_layout(state)
    with shots_tab:
        await shots_layout(state)
    with prompts_tab:
        await prompts_layout(state)
    with generate_tab:
        await generate_layout(state)
