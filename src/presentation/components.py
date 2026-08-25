import streamlit as st
import pandas as pd
import io
from io import BytesIO
import uuid
from pathlib import Path
from src.domain import ImageModel, VideoModels, Ratio, Quantity, VideoGenerationMode, Durations


# :material/settings:
# :material/home:
# :material/search:
# :material/add:
# :material/delete:
# :material/edit:
# :material/download:
# :material/upload:
# :material/play_arrow:
# :material/pause:
# :material/close:
# :material/check:
# :material/warning:
# :material/info:
# :material/folder:
# :material/movie:
# :material/send:

class UIString:
    DURATIONS = list(Durations)
    QUANTITYS = list(Quantity)
    RATIOS = list(Ratio)
    VIDEO_GEN_MODES = list(VideoGenerationMode)
    VIDEO_GEN_MODELS = list(VideoModels)
    IMAGE_GEN_MODELS = list(ImageModel)

    PROJECT_NAME_LABEL = 'PROJECT NAME'
    DEFAULT_PROJECT_NAME = 'Default project name'
    PROJECT_NAME_PLACEHOLDER = 'Nhập tên dự án'
    IMAGE_GEN_MODEL_LABEL = 'Image generation model'
    VIDEO_GEN_MODEL_LABEL = 'Video generation model'
    RATIO_LABEL = 'Ratio'
    QUANTITY_LABEL = 'Quantity'
    DURATION_LABEL = 'Duration'
    VIDEO_GEN_MODE_LABEL = 'Video generation mode'

    SIGN_IN = 'Sign In'
    ANALYZING = 'Analyzing...'
    UPLOAD_SHOT_LABEL = '**Upload shot file**'
    UPLOAD_CHAR_LABEL = '**Upload chars file**'
    UPLOAD_PROMPT_LABEL = '**Upload prompt file**'
    STYLE_LOCK_LABEL = '**Style lock**'
    STYLE_LOCK_PLACEHOLDER = "Cinematic, photorealistic visual style with natural lighting, realistic textures, consistent color grading, ..."
    SELECT_MODEL_LABEL = "**Select a model:**"
    ANALYSIS = 'Trích xuất'

    # Page
    page_title = "Minh Prompt"
    page_caption = "Phân tích và tạo prompt từ kịch bản"

    # Script
    UPLOAD_LABEL = "**Tải kịch bản**"
    SCRIPT_CONTENT_LABEL = "**Nội dung kịch bản**"
    SCRIPT_PLACE_HOLDER = "Nhập hoặc dán nội dung kịch bản tại đây..."
    SCRIPT_ANALYSIS_LABEL = "Phân tích kịch bản"
    SCRIPT_ANALYZE_HELP = (
        "Phân tích kịch bản để xác định nhân vật, "
        "các cảnh quay và tạo prompt tương ứng."
    )

    # Characters
    characters_prompt_label = "**Prompt phân tích nhân vật**"
    characters_prompt_placeholder = (
        "Nhập prompt dùng để trích xuất thông tin nhân vật..."
    )
    EXPORT_DATA_LABEL = ":material/download: Download"

    # Shots
    shots_prompt_label = "**Prompt phân tích cảnh quay**"
    shots_prompt_placeholder = (
        "Nhập prompt dùng để phân tích và trích xuất các cảnh quay..."
    )

    # Prompts
    prompts_title = "**Danh sách prompt**"
    SEND_ALL = ":material/send: Gửi toàn bộ"
    GEN_PROMPT = 'Tạo prompts'

    LIST_MODEL = [
        'gpt-4.1-nano',
        'gpt-4.1-mini',
        'gpt-5-nano',
        'gpt-5-mini',
        'gpt-4',
        'gpt-3.5-turbo',
        'gpt-3.5-turbo-0125',
        'gpt-5.6-luna',
        'gpt-5.6-terra',
        'gpt-5.6-sol',
    ]


def download_excel_btn(label, data, file_name):
    st.download_button(
        label=label,
        data=create_excel_data(data) if data else b"",
        file_name=file_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        disabled=not data,
    )


def get_uploaded_text(uploaded_file) -> str:
    if not uploaded_file:
        return ""

    return uploaded_file.getvalue().decode("utf-8")


def create_excel_data(data: list[dict]) -> bytes:
    '''Hàm tạo dữ liệu excel để có thể tải'''
    df = pd.DataFrame(data)

    buffer = BytesIO()
    df.to_excel(buffer, index=False, engine="openpyxl")

    return buffer.getvalue()


def create_id(prefix: str = ''):
    '''

    :param prefix:
    :return:
    '''
    return f"{prefix}_{str(uuid.uuid4())}"


def print_data_table(data: list[dict]):
    '''Dùng để hiển thị dữ liệu dạng bảng'''
    df = pd.json_normalize(data)
    st.dataframe(df)


def select_model(key: str, list_model: list[str] | None = None):
    if list_model is None:
        list_model = UIString.LIST_MODEL
    st.selectbox(
        label=UIString.SELECT_MODEL_LABEL,
        options=list_model,
        key=key
    )


def read_uploaded_file(uploaded_file) -> list[dict]:
    """Đọc file CSV/XLSX của Streamlit thành list[dict]."""

    suffix = Path(uploaded_file.name).suffix.lower()
    content = uploaded_file.getvalue()

    if suffix == ".csv":
        df = pd.read_csv(
            io.BytesIO(content),
            encoding="utf-8-sig"
        )

    elif suffix == ".xlsx":
        df = pd.read_excel(
            io.BytesIO(content)
        )

    else:
        raise ValueError(f"Unsupported file format: {suffix}")

    # Bỏ các cột index thừa do pandas/Excel export tạo ra
    df = df.loc[:, ~df.columns.str.match(r"^Unnamed")]

    # NaN -> None
    df = df.astype(object).where(pd.notna(df), None)

    # Chuyển NaN của pandas thành None
    df = df.where(pd.notna(df), None)

    data = df.to_dict(orient="records")

    # Khôi phục subject_ids về list[str]
    for row in data:
        if "subject_ids" not in row:
            continue

        subject_ids = row["subject_ids"]

        if subject_ids is None:
            row["subject_ids"] = []

        elif isinstance(subject_ids, str):
            row["subject_ids"] = [
                subject_id.strip()
                for subject_id in subject_ids.split(",")
                if subject_id.strip()
            ]

    return data

# def text_area(key_session, **kwargs):
#
#     st.text_area(
#         label=label,
#         placeholder=UIString.shots_prompt_placeholder,
#     )
#     st.session_state[key_session] =
