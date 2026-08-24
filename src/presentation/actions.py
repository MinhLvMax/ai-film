import streamlit as st
from src.presentation.app_state import AppState
from src.presentation.components import UIString, print_data_table
from src.bootstrap import uicapabilities


# async def analysis_script(state: AppState):
#     content = state.script_content
#     pass


async def send_prompts(state: AppState):
    await uicapabilities.send_prompts(state.prompts)
    pass


async def create_prompt(state: AppState):
    prompts = await uicapabilities.build_prompt(
        state.style_lock,
        state.characters,
        state.shots,
    )
    state.prompts = prompts


async def characters_analyze(state: AppState):
    prompt = state.extract_chars_prompt
    model = state.extract_chars_model
    content = state.script_content

    chars_extracted = await uicapabilities.extract_chars(
        prompt=prompt,
        content=content,
        model=model,
    )

    state.characters = chars_extracted
    return chars_extracted


async def shots_analyze(state: AppState):
    if state.shots is None:
        state.shots = []
    table = st.empty()
    async for shots in uicapabilities.extract_shots(
            prompt=state.extract_shots_prompt,
            model=state.extract_shots_model,
            content=state.script_content,
            chars=state.characters,
    ):
        state.shots.extend(shots)
        with table.container():
            print_data_table(state.shots)

async def sign_in():
    await uicapabilities.sign_in_google()
