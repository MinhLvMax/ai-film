import streamlit as st
from src.presentation.components import UIString
from src.presentation.app_state import AppState
from src.presentation.actions import send_prompts_video_only


async def generate_layout(state: AppState):
    state.project_name = st.text_input(
        label=UIString.PROJECT_NAME_LABEL,
        placeholder=UIString.PROJECT_NAME_PLACEHOLDER,
        value=UIString.DEFAULT_PROJECT_NAME
    )
    image_config, video_config = st.columns(
        [1, 1],
        gap="small",
        vertical_alignment="top",
        border=True,
    )
    auto_send_btn = st.button(
        UIString.SEND_ALL,
        use_container_width=True,
        key="prompts_generate_all",
        disabled=not state.prompts,
    )
    if auto_send_btn:
        await send_prompts_video_only(state)

    with image_config:
        state.image_gen_model = st.selectbox(
            UIString.IMAGE_GEN_MODEL_LABEL,
            options=UIString.IMAGE_GEN_MODELS,
            key="image_gen_model",
            format_func=lambda x: x.value,
        )
        state.image_ratio = st.selectbox(
            UIString.RATIO_LABEL,
            options=UIString.RATIOS,
            key="image_ratio",
            format_func=lambda x: x.value,
        )
        state.image_quality = st.selectbox(
            UIString.QUANTITY_LABEL,
            options=UIString.QUANTITYS,
            key="image_quantity",
            format_func=lambda x: str(x.value),
        )

        with video_config:
            state.video_gen_model = st.selectbox(
                UIString.VIDEO_GEN_MODEL_LABEL,
                options=UIString.VIDEO_GEN_MODELS,
                key="video_gen_model",
                index=4,
                format_func=lambda x: x.value,
            )
            state.video_ratio = st.selectbox(
                UIString.RATIO_LABEL,
                options=UIString.RATIOS,
                key="video_ratio",
                format_func=lambda x: x.value,
            )
            state.video_quality = st.selectbox(
                UIString.QUANTITY_LABEL,
                options=UIString.QUANTITYS,
                key="video_quantity",
                format_func=lambda x: str(x.value) )
            state.video_duration = st.selectbox(
                UIString.DURATION_LABEL,
                options=UIString.DURATIONS,
                key='video_duration',
                index=2,
                format_func=lambda x: x.value, )
            state.video_gen_mode = st.selectbox(
                UIString.VIDEO_GEN_MODE_LABEL,
                options=UIString.VIDEO_GEN_MODES,
                key="video_gen_modes",
                format_func=lambda x: x.value,
            )
