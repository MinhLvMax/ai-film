import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import pandas as pd
from src.presentation.app_state import AppState
from src.bootstrap import uicapabilities


# async def send_prompts_video_only(state: AppState, table: DeltaGenerator):
#     '''Lặp lấy kết quả mỗi lần trả ra của hàm gửi ở dưới'''
#     status = st.empty()
#
#     async for prompts in uicapabilities.send_prompts(
#             state.prompts,
#             state.video_gen_mode,
#             state.video_ratio,
#             state.video_quality,
#             state.video_duration,
#             state.video_gen_model,
#             state.max_creating_video,
#             state.project_name,
#     ):
#         state.prompts = prompts
#
#         sent_count = sum(
#             1 for prompt in prompts
#             if prompt.get("is_sent", False)
#         )
#
#         status.write(
#             f"Đã gửi {sent_count}/{len(prompts)} prompts"
#         )
#         table.dataframe(pd.json_normalize(state.prompts))
#         state.save()


async def send_prompt_sequentiallys(state: AppState, table: DeltaGenerator):
    status = st.empty()

    async for prompts in uicapabilities.send_prompt_sequentiallys(
            state.prompts,
            state.project_url,
            state.sleeptime,
            state.browser_name,
    ):
        state.prompts = prompts

        sent_count = sum(
            1 for prompt in prompts
            if prompt.get("is_sent", False)
        )

        status.write(
            f"Đã gửi {sent_count}/{len(prompts)} prompts"
        )
        table.dataframe(pd.json_normalize(state.prompts))
        state.save()


async def create_prompt(state: AppState):
    prompts = await uicapabilities.build_prompt(
        state.style_lock,
        state.characters,
        state.shots,
    )
    state.prompts = prompts
    state.save()


async def characters_analyze(state: AppState, table):
    prompt = state.extract_chars_prompt
    model = state.extract_chars_model
    content = state.script_content

    chars_extracted = await uicapabilities.extract_chars(
        prompt=prompt,
        content=content,
        model=model,
    )
    state.characters = chars_extracted
    table.dataframe(state.characters)
    state.save()
    return chars_extracted


# async def shots_analyze(state: AppState, table):
#     new_shots = []
#     async for shots in uicapabilities.extract_shots(
#             prompt=state.extract_shots_prompt,
#             model=state.extract_shots_model,
#             content=state.script_content,
#             chars=state.characters,
#     ):
#         new_shots.extend(shots)
#         table.dataframe(pd.json_normalize(new_shots))
#     state.shots = new_shots
#     state.save()


async def shots_analyze(state: AppState, table):
    shots = await uicapabilities.extract_shots(
        prompt=state.extract_shots_prompt,
        model=state.extract_shots_model,
        content=state.script_content,
        chars=state.characters,
    )
    table.dataframe(pd.json_normalize(shots))
    state.shots = shots
    state.save()


async def sign_in(browser_name):
    await uicapabilities.sign_in_google(browser_name)


async def export_state(state: AppState):
    state.export()
