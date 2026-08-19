import streamlit as st
from src.presentation.layout.generation_layout.characters_layout import characters_layout
from src.presentation.layout.generation_layout.shots_layout import shots_layout
from src.presentation.layout.generation_layout.prompts_layout import prompts_layout


async def generation_layout():
    characters, shots, prompts = st.columns(
        [1, 1, 1],
        gap="small",
        vertical_alignment="top",
        border=True,
    )

    with characters:
        characters_layout()
    with shots:
        shots_layout()
    with prompts:
        await prompts_layout()
