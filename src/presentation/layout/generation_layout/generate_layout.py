import streamlit as st
from src.presentation.components import UIString
from src.presentation.app_state import AppState
from src.domain import ImageModel, VideoModels, VideoGenerationMode, Ratio, Durations, Quantity


async def generate_layout(state: AppState):
    '''Giao diện cài đặt tự động gen'''
    state.project_url = st.text_input(
        label=UIString.PROJECT_URL_LABEL,
        placeholder=UIString.PROJECT_URL_LABEL,
        value=state.project_url or '',
    )

    state.sleeptime = st.number_input(
        label="Thời gian nghỉ (giây)",
        value=state.sleeptime or 30,
        min_value=0,
        step=1,
    )
    state.save()

    # state.project_name = st.text_input(
    #     label=UIString.PROJECT_NAME_LABEL,
    #     placeholder=UIString.PROJECT_NAME_PLACEHOLDER,
    #     value=state.project_name or UIString.DEFAULT_PROJECT_NAME
    # )
    #
    # image_config, video_config = st.columns(
    #     [1, 1],
    #     gap="small",
    #     vertical_alignment="top",
    #     border=True,
    # )
    #
    # state.max_creating_video = st.number_input(
    #     label=UIString.MAXIMUM_AT_THE_MOMENT_LABEL,
    #     min_value=1,
    #     max_value=5,
    #     step=1,
    #     value=state.max_creating_video or 1
    # )
    #
    # is_download = st.toggle(
    #     label=UIString.IS_DOWNLOAD_LABEL,
    #     value=state.is_downloaded
    # )
    #
    # if is_download:
    #     st.toast('Chưa thiết kế logic tải')
    #
    # with image_config:
    #     state.image_gen_model = st.selectbox(
    #         UIString.IMAGE_GEN_MODEL_LABEL,
    #         options=UIString.IMAGE_GEN_MODELS,
    #         key="image_gen_model",
    #         format_func=lambda x: x.value,
    #     )
    #     state.image_ratio = st.selectbox(
    #         UIString.RATIO_LABEL,
    #         options=UIString.RATIOS,
    #         key="image_ratio",
    #         format_func=lambda x: x.value,
    #     )
    #     state.image_quality = st.selectbox(
    #         UIString.QUANTITY_LABEL,
    #         options=UIString.QUANTITYS,
    #         key="image_quantity",
    #         format_func=lambda x: str(x.value),
    #         help=UIString.QUANTITY_HELP,
    #     )
    #
    # with video_config:
    #     state.video_gen_model = st.selectbox(
    #         UIString.VIDEO_GEN_MODEL_LABEL,
    #         options=UIString.VIDEO_GEN_MODELS,
    #         key="video_gen_model",
    #         index=4,
    #         format_func=lambda x: x.value,
    #     )
    #     state.video_ratio = st.selectbox(
    #         UIString.RATIO_LABEL,
    #         options=UIString.RATIOS,
    #         key="video_ratio",
    #         format_func=lambda x: x.value,
    #     )
    #     state.video_quality = st.selectbox(
    #         UIString.QUANTITY_LABEL,
    #         options=UIString.QUANTITYS,
    #         key="video_quantity",
    #         format_func=lambda x: str(x.value),
    #         help=UIString.QUANTITY_HELP,
    #     )
    #     state.video_duration = st.selectbox(
    #         UIString.DURATION_LABEL,
    #         options=UIString.DURATIONS,
    #         key='video_duration',
    #         index=2,
    #         format_func=lambda x: x.value, )
    #     state.video_gen_mode = st.selectbox(
    #         UIString.VIDEO_GEN_MODE_LABEL,
    #         options=UIString.VIDEO_GEN_MODES,
    #         key="video_gen_modes",
    #         format_func=lambda x: x.value,
    #     )
