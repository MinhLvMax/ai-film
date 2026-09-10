import streamlit as st
import pandas as pd
from src.presentation.app_state import AppState
from src.presentation.components import UIString, read_uploaded_file, print_data_table
from src.presentation.actions import create_prompt
from src.presentation.actions import send_prompt_sequentiallys

async def prompts_layout(state: AppState):
    state.style_lock = st.text_area(
        label=UIString.STYLE_LOCK_LABEL,
        placeholder=UIString.STYLE_LOCK_PLACEHOLDER,
        value=state.style_lock or ''
    )

    gen_all_prompts = st.button(
        UIString.GEN_PROMPT,
        use_container_width=True,
        key="gen_all_prompts",
        disabled=not state.characters and not state.shots,
    )

    if gen_all_prompts:
        await create_prompt(state)

    uploaded_prompt_file = st.file_uploader(
        label=UIString.UPLOAD_PROMPT_LABEL,
        type=["xlsx", 'csv']
    )

    if uploaded_prompt_file is not None:
        state.prompts = read_uploaded_file(uploaded_prompt_file)

    table = st.empty()

    edited_df = table.data_editor(
        pd.json_normalize(state.prompts),
        key="prompts_editor",
        width='stretch',
    )

    # Update ngược lại vào state
    new_prompts = edited_df.to_dict("records")
    if new_prompts != state.prompts:  # Nếu dữ liệu khác trước đó thì lưu
        state.prompts = new_prompts
        state.save()

    auto_send_btn = st.button(
        UIString.SEND_ALL,
        use_container_width=True,
        key="prompts_generate_all",
        disabled=not state.prompts,
    )

    if auto_send_btn:
        # await send_prompts_video_only(state, table)
        await send_prompt_sequentiallys(state, table)

    # if state.prompts:
    #     print_data_table(state.prompts)
