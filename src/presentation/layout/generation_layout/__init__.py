import streamlit as st

from src.presentation.app_state import AppState
from src.presentation.layout.generation_layout.characters_layout import characters_layout
from src.presentation.layout.generation_layout.shots_layout import shots_layout
from src.presentation.layout.generation_layout.prompts_layout import prompts_layout
from src.presentation.app_state import AppState

async def generation_layout(state: AppState):
    characters_tab, shots_tab, prompts_tab = st.tabs(
        [
            "Characters",
            "Shots",
            "Prompts",
        ]
    )

    with characters_tab:
        await characters_layout(state)
    with shots_tab:
        await shots_layout(state)
    with prompts_tab:
        await prompts_layout(state)
