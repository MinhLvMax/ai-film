import streamlit as st

st.set_page_config(
    page_title="AI Film Workspace",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# MOCK DATA
# =========================================================

SEGMENT_TITLES = [
    "Introduction",
    "Daily Life",
    "Culture",
    "Conflict",
    "Village Life",
    "Family",
    "Education",
    "Work",
    "Travel",
    "Tradition",
    "Turning Point",
    "Challenge",
    "Recovery",
    "Discovery",
    "Collaboration",
    "Momentum",
    "Reflection",
    "Resolution",
    "Future",
    "Conclusion",
]

SCENES_PER_SEGMENT = 15


def segment_id(index: int) -> str:
    return f"{index + 1:02d}"


def segment_label(index: int) -> str:
    return f"Segment {segment_id(index)} — {SEGMENT_TITLES[index]}"


def make_segment_text(index: int) -> str:
    seg_id = segment_id(index)
    title = SEGMENT_TITLES[index]

    paragraph = (
        f"{title} is mock long-form documentary content for Segment {seg_id}. "
        "This text is intentionally longer than a normal UI placeholder so the page "
        "behaves more like a real production workspace. The final application may keep "
        "roughly one thousand tokens in each segment, with the editor reviewing wording, "
        "structure, factual notes, visual cues, transitions, and continuity before moving "
        "into media prompt production."
    )

    return "\n\n".join(
        [
            paragraph,
            (
                "The segment continues with a second paragraph containing narrative detail, "
                "possible human activity, environmental context, camera opportunities, and "
                "production notes. Everything here is editable so the Streamlit prototype "
                "can be tested with realistic scrolling and text editing."
            ),
            (
                "A final paragraph adds more text volume. In the real workflow, edits made "
                "here should become the source material for scene breakdowns and image/video "
                "prompts in the Media Generation workspace."
            ),
        ]
    )


def make_image_prompt(segment_index: int, scene_index: int) -> str:
    return (
        f"Cinematic documentary image for {segment_label(segment_index)}, "
        f"Scene {scene_index + 1:02d}. Local people engaged in daily life, "
        "natural lighting, realistic environment, strong composition, "
        "production-ready framing, documentary realism."
    )


def make_video_prompt(segment_index: int, scene_index: int) -> str:
    return (
        f"Cinematic video for {segment_label(segment_index)}, "
        f"Scene {scene_index + 1:02d}. Slow controlled camera movement, "
        "natural human activity, environmental motion, realistic lighting, "
        "documentary continuity and believable movement."
    )


# =========================================================
# SESSION STATE
# =========================================================

def init_state() -> None:
    if "content_keyword" not in st.session_state:
        st.session_state.content_keyword = "Living in Suriname"

    if "content_description" not in st.session_state:
        st.session_state.content_description = (
            "A documentary about daily life, culture, work, communities, "
            "landscapes and the relationship between people and their environment."
        )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": (
                    "Tôi đang ở cạnh workspace. Bạn có thể thử ra lệnh như: "
                    "“Viết lại segment 3 và 5” hoặc “Tạo lại prompt của scene 4”."
                ),
            }
        ]

    if "content_segments" not in st.session_state:
        st.session_state.content_segments = {
            segment_id(i): make_segment_text(i)
            for i in range(len(SEGMENT_TITLES))
        }

    if "selected_media_segment" not in st.session_state:
        st.session_state.selected_media_segment = segment_label(0)

    if "ui_notice" not in st.session_state:
        st.session_state.ui_notice = None

    # Content selection
    for i in range(len(SEGMENT_TITLES)):
        seg_id = segment_id(i)
        st.session_state.setdefault(f"content_selected_{seg_id}", False)

    # Media prompt text + selection
    for i in range(len(SEGMENT_TITLES)):
        seg_id = segment_id(i)

        for scene_index in range(SCENES_PER_SEGMENT):
            suffix = f"{scene_index + 1:02d}"

            st.session_state.setdefault(
                f"media_image_{seg_id}_{suffix}",
                make_image_prompt(i, scene_index),
            )
            st.session_state.setdefault(
                f"media_video_{seg_id}_{suffix}",
                make_video_prompt(i, scene_index),
            )
            st.session_state.setdefault(
                f"media_selected_image_{seg_id}_{suffix}",
                False,
            )
            st.session_state.setdefault(
                f"media_selected_video_{seg_id}_{suffix}",
                False,
            )


# =========================================================
# SMALL HELPERS
# =========================================================

def sync_content_segment(seg_id: str) -> None:
    st.session_state.content_segments[seg_id] = st.session_state[
        f"content_editor_{seg_id}"
    ]


def current_media_segment_index() -> int:
    labels = [segment_label(i) for i in range(len(SEGMENT_TITLES))]
    return labels.index(st.session_state.selected_media_segment)


def selected_content_ids() -> list[str]:
    return [
        segment_id(i)
        for i in range(len(SEGMENT_TITLES))
        if st.session_state[f"content_selected_{segment_id(i)}"]
    ]


def selected_prompt_ids(seg_id: str) -> list[str]:
    result = []

    for scene_index in range(SCENES_PER_SEGMENT):
        suffix = f"{scene_index + 1:02d}"

        if st.session_state[f"media_selected_image_{seg_id}_{suffix}"]:
            result.append(f"Scene {suffix} — Image")

        if st.session_state[f"media_selected_video_{seg_id}_{suffix}"]:
            result.append(f"Scene {suffix} — Video")

    return result


def set_all_content_selection(value: bool) -> None:
    for i in range(len(SEGMENT_TITLES)):
        st.session_state[f"content_selected_{segment_id(i)}"] = value


def set_all_prompt_selection(seg_id: str, value: bool) -> None:
    for scene_index in range(SCENES_PER_SEGMENT):
        suffix = f"{scene_index + 1:02d}"
        st.session_state[f"media_selected_image_{seg_id}_{suffix}"] = value
        st.session_state[f"media_selected_video_{seg_id}_{suffix}"] = value


def show_notice() -> None:
    notice = st.session_state.ui_notice
    if not notice:
        return

    level, text = notice

    if level == "success":
        st.success(text)
    elif level == "warning":
        st.warning(text)
    else:
        st.info(text)

    st.session_state.ui_notice = None


# =========================================================
# STYLING
# =========================================================

def inject_css() -> None:
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 1.3rem;
                padding-bottom: 4rem;
                max-width: 1800px;
            }

            [data-testid="stSidebar"] {
                min-width: 310px;
                max-width: 380px;
            }

            .workspace-title {
                font-size: 1.9rem;
                font-weight: 750;
                margin-bottom: 0.2rem;
            }

            .workspace-subtitle {
                color: #888;
                margin-bottom: 1rem;
            }

            .segment-anchor {
                scroll-margin-top: 90px;
            }

            .scene-header {
                font-size: 1.05rem;
                font-weight: 700;
                margin-top: 0.3rem;
            }

            div[data-testid="stTextArea"] textarea {
                line-height: 1.5;
            }

            .outline-box {
                max-height: 560px;
                overflow-y: auto;
                padding-right: 0.35rem;
            }

            .outline-link {
                display: block;
                padding: 0.20rem 0.35rem;
                margin: 0.05rem 0;
                text-decoration: none !important;
                border-radius: 0.35rem;
            }

            .outline-link:hover {
                background: rgba(128, 128, 128, 0.12);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# AI ASSISTANT
# =========================================================

def render_ai_sidebar() -> None:
    with st.sidebar:
        st.title("AI Assistant")
        st.caption("Mock chat — luôn nằm cạnh Content và Media.")

        context = (
            f"Media: {st.session_state.selected_media_segment}"
            if "selected_media_segment" in st.session_state
            else "Content"
        )
        st.caption(f"Current context: {context}")

        st.divider()

        chat_box = st.container(height=430)
        with chat_box:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        prompt = st.chat_input("Ask AI...")

        if prompt:
            st.session_state.chat_history.append(
                {"role": "user", "content": prompt}
            )
            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": f"Đã nhận yêu cầu: {prompt}",
                }
            )
            st.rerun()

        if st.button("Clear chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()


# =========================================================
# CONTENT WORKSPACE
# =========================================================

def render_content_workspace() -> None:
    st.markdown('<div class="workspace-title">Content Workspace</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="workspace-subtitle">'
        "Toàn bộ content được hiển thị liên tục; outline chỉ dùng để nhảy nhanh."
        "</div>",
        unsafe_allow_html=True,
    )

    settings_col, content_col = st.columns([1.5, 4.5], gap="large")

    # -------------------------
    # Left: input + outline
    # -------------------------
    with settings_col:
        st.text_input("Keyword", key="content_keyword")
        st.text_area(
            "Description",
            key="content_description",
            height=120,
        )

        if st.button(
                "GENERATE CONTENT",
                type="primary",
                use_container_width=True,
        ):
            st.session_state.ui_notice = (
                "info",
                "UI test: GENERATE CONTENT clicked.",
            )
            st.rerun()

        st.divider()
        st.markdown("#### Content Outline")
        st.caption("Click để thử jump đến segment trong cùng trang.")

        outline_html = '<div class="outline-box">'

        for i, title in enumerate(SEGMENT_TITLES):
            seg_id = segment_id(i)
            outline_html += (
                f'<a class="outline-link" href="#segment-{seg_id}">'
                f'{seg_id}. {title}</a>'
            )

        outline_html += "</div>"
        st.markdown(outline_html, unsafe_allow_html=True)

    # -------------------------
    # Right: all segments
    # -------------------------
    with content_col:
        action_1, action_2, action_3 = st.columns([1, 1, 2])

        if action_1.button("SELECT ALL", use_container_width=True):
            set_all_content_selection(True)
            st.rerun()

        if action_2.button("CLEAR", use_container_width=True):
            set_all_content_selection(False)
            st.rerun()

        if action_3.button(
                "REGENERATE SELECTED",
                type="primary",
                use_container_width=True,
        ):
            selected = selected_content_ids()

            if selected:
                st.session_state.ui_notice = (
                    "success",
                    "UI test — selected segments: " + ", ".join(selected),
                )
            else:
                st.session_state.ui_notice = (
                    "warning",
                    "Chưa chọn segment nào.",
                )

            st.rerun()

        show_notice()

        selected = selected_content_ids()
        st.caption(
            f"Selected: {len(selected)} segment(s)"
            + (f" — {', '.join(selected)}" if selected else "")
        )

        st.divider()

        for i, title in enumerate(SEGMENT_TITLES):
            seg_id = segment_id(i)

            st.markdown(
                f'<div class="segment-anchor" id="segment-{seg_id}"></div>',
                unsafe_allow_html=True,
            )

            header_col, select_col = st.columns([7, 1])

            with header_col:
                st.markdown(f"### Segment {seg_id} — {title}")

            with select_col:
                st.checkbox(
                    "Select",
                    key=f"content_selected_{seg_id}",
                )

            editor_key = f"content_editor_{seg_id}"

            if editor_key not in st.session_state:
                st.session_state[editor_key] = st.session_state.content_segments[
                    seg_id
                ]

            st.text_area(
                f"Content for Segment {seg_id}",
                key=editor_key,
                height=210,
                label_visibility="collapsed",
                on_change=sync_content_segment,
                args=(seg_id,),
            )

            st.divider()


# =========================================================
# MEDIA WORKSPACE
# =========================================================

def render_media_workspace() -> None:
    st.markdown('<div class="workspace-title">Media Generation</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="workspace-subtitle">'
        "Chỉ Scene/Prompt của segment đang chọn được hiển thị."
        "</div>",
        unsafe_allow_html=True,
    )

    selector_col, info_col = st.columns([2.1, 4], gap="large")

    with selector_col:
        st.selectbox(
            "Select segment",
            options=[
                segment_label(i)
                for i in range(len(SEGMENT_TITLES))
            ],
            key="selected_media_segment",
        )

    seg_index = current_media_segment_index()
    seg_id = segment_id(seg_index)

    with info_col:
        st.info(
            f"Đang làm việc với **{segment_label(seg_index)}** — "
            f"{SCENES_PER_SEGMENT} scenes / "
            f"{SCENES_PER_SEGMENT * 2} prompts."
        )

    action_1, action_2, action_3 = st.columns([1.25, 1, 2.1])

    if action_1.button(
            "SELECT ALL PROMPTS",
            use_container_width=True,
    ):
        set_all_prompt_selection(seg_id, True)
        st.rerun()

    if action_2.button(
            "CLEAR",
            use_container_width=True,
    ):
        set_all_prompt_selection(seg_id, False)
        st.rerun()

    if action_3.button(
            "REGENERATE SELECTED PROMPTS",
            type="primary",
            use_container_width=True,
    ):
        selected = selected_prompt_ids(seg_id)

        if selected:
            st.session_state.ui_notice = (
                "success",
                f"UI test — selected {len(selected)} prompt(s) in Segment {seg_id}.",
            )
        else:
            st.session_state.ui_notice = (
                "warning",
                "Chưa chọn prompt nào.",
            )

        st.rerun()

    show_notice()

    selected_prompts = selected_prompt_ids(seg_id)
    st.caption(f"Selected prompts in Segment {seg_id}: {len(selected_prompts)}")

    st.divider()

    source_text = st.session_state.content_segments[seg_id]

    for scene_index in range(SCENES_PER_SEGMENT):
        suffix = f"{scene_index + 1:02d}"

        st.markdown(
            f'<div class="scene-header">SCENE {suffix}</div>',
            unsafe_allow_html=True,
        )

        with st.expander("Source content", expanded=False):
            st.write(source_text[:700])

        image_col, video_col = st.columns(2, gap="large")

        # -------------------------
        # Image prompt
        # -------------------------
        with image_col:
            st.markdown("**IMAGE PROMPT**")

            st.text_area(
                f"Image Prompt {suffix}",
                key=f"media_image_{seg_id}_{suffix}",
                height=135,
                label_visibility="collapsed",
            )

            select_col, gen_col = st.columns([1, 1.4])

            with select_col:
                st.checkbox(
                    "Select",
                    key=f"media_selected_image_{seg_id}_{suffix}",
                )

            with gen_col:
                if st.button(
                        "GEN IMAGE",
                        key=f"gen_image_{seg_id}_{suffix}",
                        use_container_width=True,
                ):
                    st.info(
                        f"UI test: GEN IMAGE — Segment {seg_id}, Scene {suffix}"
                    )

        # -------------------------
        # Video prompt
        # -------------------------
        with video_col:
            st.markdown("**VIDEO PROMPT**")

            st.text_area(
                f"Video Prompt {suffix}",
                key=f"media_video_{seg_id}_{suffix}",
                height=135,
                label_visibility="collapsed",
            )

            select_col, gen_col = st.columns([1, 1.4])

            with select_col:
                st.checkbox(
                    "Select",
                    key=f"media_selected_video_{seg_id}_{suffix}",
                )

            with gen_col:
                if st.button(
                        "GEN VIDEO",
                        key=f"gen_video_{seg_id}_{suffix}",
                        use_container_width=True,
                ):
                    st.info(
                        f"UI test: GEN VIDEO — Segment {seg_id}, Scene {suffix}"
                    )

        st.divider()


# =========================================================
# APP
# =========================================================

def main() -> None:
    init_state()
    inject_css()
    render_ai_sidebar()

    st.title("AI Film Workspace")
    st.caption(
        "Prototype UI — Content + Media Generation + AI Assistant"
    )

    content_tab, media_tab = st.tabs(
        ["CONTENT", "MEDIA GENERATION"]
    )

    with content_tab:
        render_content_workspace()

    with media_tab:
        render_media_workspace()


if __name__ == "__main__":
    main()
