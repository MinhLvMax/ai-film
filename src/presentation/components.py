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
    # Mock data
    CHARACTERS_MOCK_DATA = [
        {
            "id": "con_cho",
            "name": "Con chó",
            "description": "Một con chó lông đen, kích thước trung bình, đôi mắt nâu và chiếc vòng cổ màu đỏ.",
        },
        {
            "id": "nguyen_anh",
            "name": "Nguyễn Anh",
            "description": "Một người đàn ông khoảng 30 tuổi, tóc đen ngắn, dáng người cao, thường mặc áo sơ mi trắng.",
        },
        {
            "id": "co_gai",
            "name": "Cô gái",
            "description": "Một cô gái trẻ khoảng 25 tuổi, tóc dài màu nâu, khuôn mặt thanh tú và thường mặc váy xanh.",
        },
    ]
    SHOTS_MOCK_DATA = [
        {
            "shot_id": "shot_001",
            "subject_ids": ["con_cho", "nguyen_anh"],
            "action": "Nguyễn Anh bước chậm về phía con chó và cúi xuống vuốt ve nó.",
            "environment": "Một con hẻm yên tĩnh vào buổi chiều, ánh nắng nhẹ chiếu qua những tán cây.",
            "camera": "Medium shot, camera đặt ngang tầm mắt, chuyển động dolly chậm theo nhân vật.",
            "subjects": [
                {
                    "id": "con_cho",
                    "name": "Con chó",
                    "description": "Một con chó lông đen, kích thước trung bình, đôi mắt nâu và chiếc vòng cổ màu đỏ.",
                },
                {
                    "id": "nguyen_anh",
                    "name": "Nguyễn Anh",
                    "description": "Một người đàn ông khoảng 30 tuổi, tóc đen ngắn, dáng người cao, mặc áo sơ mi trắng.",
                },
            ],
        },
        {
            "shot_id": "shot_002",
            "subject_ids": ["con_cho"],
            "action": "Con chó ngẩng đầu nhìn Nguyễn Anh rồi vẫy đuôi.",
            "environment": "Con hẻm yên tĩnh với những bức tường cũ và ánh nắng vàng dịu.",
            "camera": "Close-up shot tập trung vào khuôn mặt và chiếc đuôi của con chó.",
            "subjects": [
                {
                    "id": "con_cho",
                    "name": "Con chó",
                    "description": "Một con chó lông đen, kích thước trung bình, đôi mắt nâu và chiếc vòng cổ màu đỏ.",
                },
            ],
        },
        {
            "shot_id": "shot_003",
            "subject_ids": ["nguyen_anh"],
            "action": "Nguyễn Anh đứng dậy, mỉm cười và nhìn về cuối con hẻm.",
            "environment": "Con hẻm vào lúc hoàng hôn, ánh sáng vàng phủ lên các bức tường và mặt đường.",
            "camera": "Wide shot từ phía sau nhân vật, camera từ từ kéo ra để mở rộng khung cảnh.",
            "subjects": [
                {
                    "id": "nguyen_anh",
                    "name": "Nguyễn Anh",
                    "description": "Một người đàn ông khoảng 30 tuổi, tóc đen ngắn, dáng người cao, mặc áo sơ mi trắng.",
                },
            ],
        },
    ]
    PROMPT_MOCK_DATA = [

    ]

    UPLOAD_PROMPT_LABEL = '**Upload prompt file**'
    STYLE_LOCK_LABEL = '**Style lock**'
    STYLE_LOCK_PLACEHOLDER = "Cinematic, photorealistic visual style with natural lighting, realistic textures, consistent color grading, ..."
    SELECT_MODEL_LABEL = "**Select a model:**"
    ANALYSIS = 'Phân tích'

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


def print_data_table(data: dict):
    '''Dùng để hiển thị dữ liệu dạng bảng'''
    df = pd.DataFrame(data)
    st.dataframe(df)


def select_model(key: str, list_model: list[str] | None = None):
    if list_model is None:
        list_model = UIString.LIST_MODEL
    st.selectbox(
        label=UIString.SELECT_MODEL_LABEL,
        options=list_model,
        key=key
    )

# def text_area(key_session, **kwargs):
#
#     st.text_area(
#         label=label,
#         placeholder=UIString.shots_prompt_placeholder,
#     )
#     st.session_state[key_session] =
