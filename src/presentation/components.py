import streamlit as st
import pandas as pd
from io import BytesIO
import uuid


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


def download_excel_btn(label, data, file_name, key):
    st.download_button(
        label=label,
        data=create_excel_data(data) if data else b"",
        file_name=file_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        key=key,
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


def print_df(data: dict):
    '''Dùng để hiển thị dữ liệu dạng bảng'''
    df = pd.DataFrame(data)
    st.dataframe(df)
