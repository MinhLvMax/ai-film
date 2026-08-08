from nicegui import ui

SEGMENT_TITLES = [
    "Introduction", "Daily Life", "Culture", "Conflict", "Village Life",
    "Family", "Education", "Work", "Travel", "Tradition",
    "Turning Point", "Challenge", "Recovery", "Discovery", "Collaboration",
    "Momentum", "Reflection", "Resolution", "Future", "Conclusion",
]

SCENES_PER_SEGMENT = 15

segment_contents = {
    i: (
        f"{SEGMENT_TITLES[i]} — mock content for Segment {i + 1:02d}.\n\n"
        "This is editable long-form content used only to test the NiceGUI workspace. "
        "In the real application this segment can contain around 1000 tokens.\n\n"
        "The editor can revise structure, wording, visual cues and production notes here."
    )
    for i in range(len(SEGMENT_TITLES))
}

media_prompts = {}
for segment_index in range(len(SEGMENT_TITLES)):
    media_prompts[segment_index] = {}
    for scene_index in range(SCENES_PER_SEGMENT):
        media_prompts[segment_index][scene_index] = {
            "image": (
                f"Cinematic documentary image for Segment {segment_index + 1:02d}, "
                f"Scene {scene_index + 1:02d}. Realistic people, natural light, "
                "documentary composition."
            ),
            "video": (
                f"Cinematic documentary video for Segment {segment_index + 1:02d}, "
                f"Scene {scene_index + 1:02d}. Slow camera movement, natural human "
                "activity, realistic continuity."
            ),
        }

selected_content_segments = set()
selected_media_prompts = set()
chat_history = []


def seg_label(index: int) -> str:
    return f"{index + 1:02d} — {SEGMENT_TITLES[index]}"


def selected_segment_text() -> str:
    if not selected_content_segments:
        return "No segment selected"
    return ", ".join(f"{i + 1:02d}" for i in sorted(selected_content_segments))


def add_chat(role: str, text: str) -> None:
    chat_history.append((role, text))
    with chat_messages:
        ui.chat_message(
            text=text,
            name="You" if role == "user" else "AI",
            sent=role == "user",
        )


def send_chat() -> None:
    text = chat_input.value.strip()
    if not text:
        return

    add_chat("user", text)
    add_chat("assistant", f"Mock AI đã nhận yêu cầu: {text}")
    chat_input.value = ""


def toggle_content_segment(index: int, checked: bool) -> None:
    if checked:
        selected_content_segments.add(index)
    else:
        selected_content_segments.discard(index)
    content_selection_label.text = f"Selected: {selected_segment_text()}"


def select_all_content() -> None:
    selected_content_segments.clear()
    selected_content_segments.update(range(len(SEGMENT_TITLES)))
    for checkbox in content_checkboxes.values():
        checkbox.value = True
    content_selection_label.text = f"Selected: {selected_segment_text()}"


def clear_content_selection() -> None:
    selected_content_segments.clear()
    for checkbox in content_checkboxes.values():
        checkbox.value = False
    content_selection_label.text = "Selected: No segment selected"


def mock_regenerate_content() -> None:
    if not selected_content_segments:
        ui.notify("Chưa chọn segment nào", type="warning")
        return
    ui.notify(
        f"Mock regenerate Segment: {selected_segment_text()}",
        type="positive",
    )


def jump_to_segment(index: int) -> None:
    ui.run_javascript(
        f'document.getElementById("segment-{index}").scrollIntoView('
        '{behavior:"smooth", block:"start"});'
    )


def toggle_media_prompt(prompt_id: str, checked: bool) -> None:
    if checked:
        selected_media_prompts.add(prompt_id)
    else:
        selected_media_prompts.discard(prompt_id)
    media_selection_label.text = f"Selected prompts: {len(selected_media_prompts)}"


def clear_media_selection() -> None:
    selected_media_prompts.clear()
    for checkbox in media_checkboxes:
        checkbox.value = False
    media_selection_label.text = "Selected prompts: 0"


def select_all_media() -> None:
    selected_media_prompts.clear()
    for prompt_id, checkbox in media_checkbox_by_id.items():
        selected_media_prompts.add(prompt_id)
        checkbox.value = True
    media_selection_label.text = f"Selected prompts: {len(selected_media_prompts)}"


def mock_regenerate_prompts() -> None:
    if not selected_media_prompts:
        ui.notify("Chưa chọn prompt nào", type="warning")
        return
    ui.notify(
        f"Mock regenerate {len(selected_media_prompts)} prompt(s)",
        type="positive",
    )


def render_media_segment(segment_index: int) -> None:
    media_container.clear()
    selected_media_prompts.clear()
    media_checkbox_by_id.clear()
    media_checkboxes.clear()

    with media_container:
        ui.label(
            f"Segment {segment_index + 1:02d} — {SEGMENT_TITLES[segment_index]}"
        ).classes("text-xl font-bold")

        ui.label(
            f"{SCENES_PER_SEGMENT} scenes / {SCENES_PER_SEGMENT * 2} prompts"
        ).classes("text-sm text-gray-500")

        for scene_index in range(SCENES_PER_SEGMENT):
            scene_no = scene_index + 1

            with ui.card().classes("w-full"):
                ui.label(f"SCENE {scene_no:02d}").classes("text-lg font-bold")

                with ui.expansion("Source content", icon="article").classes("w-full"):
                    ui.label(segment_contents[segment_index]).classes(
                        "text-sm whitespace-pre-wrap"
                    )

                with ui.row().classes("w-full gap-4 items-stretch"):
                    with ui.card().classes("w-full"):
                        ui.label("IMAGE PROMPT").classes("font-semibold")

                        image_area = ui.textarea(
                            value=media_prompts[segment_index][scene_index]["image"]
                        ).props("outlined autogrow").classes("w-full")

                        image_area.on(
                            "change",
                            lambda e, s=segment_index, sc=scene_index, area=image_area:
                            media_prompts[s][sc].__setitem__("image", area.value),
                        )

                        image_id = f"{segment_index}:{scene_index}:image"
                        image_checkbox = ui.checkbox(
                            "Select",
                            on_change=lambda e, pid=image_id:
                            toggle_media_prompt(pid, e.value),
                        )
                        media_checkbox_by_id[image_id] = image_checkbox
                        media_checkboxes.append(image_checkbox)

                        ui.button(
                            "GEN IMAGE",
                            on_click=lambda s=segment_index, sc=scene_index:
                            ui.notify(
                                f"UI test: GEN IMAGE — Segment {s + 1:02d}, "
                                f"Scene {sc + 1:02d}"
                            ),
                        ).props("outline").classes("w-full")

                    with ui.card().classes("w-full"):
                        ui.label("VIDEO PROMPT").classes("font-semibold")

                        video_area = ui.textarea(
                            value=media_prompts[segment_index][scene_index]["video"]
                        ).props("outlined autogrow").classes("w-full")

                        video_area.on(
                            "change",
                            lambda e, s=segment_index, sc=scene_index, area=video_area:
                            media_prompts[s][sc].__setitem__("video", area.value),
                        )

                        video_id = f"{segment_index}:{scene_index}:video"
                        video_checkbox = ui.checkbox(
                            "Select",
                            on_change=lambda e, pid=video_id:
                            toggle_media_prompt(pid, e.value),
                        )
                        media_checkbox_by_id[video_id] = video_checkbox
                        media_checkboxes.append(video_checkbox)

                        ui.button(
                            "GEN VIDEO",
                            on_click=lambda s=segment_index, sc=scene_index:
                            ui.notify(
                                f"UI test: GEN VIDEO — Segment {s + 1:02d}, "
                                f"Scene {sc + 1:02d}"
                            ),
                        ).props("outline").classes("w-full")


# ---------------------------------------------------------
# PAGE LAYOUT
# ---------------------------------------------------------

ui.add_head_html(
    """
    <style>
        body {
            background: #f7f7f8;
        }
        .main-workspace {
            max-width: 1800px;
            margin: 0 auto;
        }
    </style>
    """
)

with ui.header().classes("items-center justify-between"):
    ui.label("AI Film Workspace").classes("text-lg font-bold")
    ui.button("AI Assistant", icon="smart_toy", on_click=lambda: ai_drawer.toggle()).props(
        "flat color=white"
    )

with ui.right_drawer(value=False).props("bordered").classes("w-96") as ai_drawer:
    ui.label("AI Assistant").classes("text-xl font-bold")
    ui.label("Chat song song với workspace").classes("text-sm text-gray-500")
    ui.separator()

    chat_messages = ui.column().classes("w-full gap-2")

    with ui.row().classes("w-full items-end"):
        chat_input = ui.textarea(placeholder="Ask AI...").props("outlined autogrow").classes(
            "grow"
        )
        ui.button(icon="send", on_click=send_chat).props("round")

    ui.button(
        "Clear chat",
        on_click=lambda: (chat_history.clear(), chat_messages.clear()),
    ).props("flat").classes("w-full")


with ui.column().classes("w-full main-workspace p-4 gap-4"):

    with ui.tabs().classes("w-full") as tabs:
        content_tab = ui.tab("CONTENT", icon="article")
        media_tab = ui.tab("MEDIA GENERATION", icon="movie")

    with ui.tab_panels(tabs, value=content_tab).classes("w-full"):

        # =================================================
        # CONTENT TAB
        # =================================================
        with ui.tab_panel(content_tab):

            with ui.row().classes("w-full gap-6 items-start"):

                # Left control/outline
                with ui.card().classes("w-80 sticky top-20"):
                    ui.label("Content Setup").classes("text-lg font-bold")

                    ui.input("Keyword", value="Living in Suriname").classes("w-full")
                    ui.textarea(
                        "Description",
                        value=(
                            "A documentary about daily life, culture, communities, "
                            "work and landscapes."
                        ),
                    ).props("outlined autogrow").classes("w-full")

                    ui.button(
                        "GENERATE CONTENT",
                        on_click=lambda: ui.notify("UI test: Generate Content"),
                    ).classes("w-full")

                    ui.separator()
                    ui.label("Content Outline").classes("font-bold")

                    with ui.scroll_area().classes("w-full h-96"):
                        for i, title in enumerate(SEGMENT_TITLES):
                            ui.button(
                                f"{i + 1:02d}. {title}",
                                on_click=lambda index=i: jump_to_segment(index),
                            ).props("flat dense align=left").classes("w-full")

                # Whole content
                with ui.column().classes("grow gap-3"):

                    with ui.row().classes("w-full items-center"):
                        ui.button("SELECT ALL", on_click=select_all_content).props("outline")
                        ui.button("CLEAR", on_click=clear_content_selection).props("outline")
                        ui.button(
                            "REGENERATE SELECTED",
                            on_click=mock_regenerate_content,
                        )
                        content_selection_label = ui.label(
                            "Selected: No segment selected"
                        ).classes("text-sm text-gray-500 ml-3")

                    content_checkboxes = {}

                    for i, title in enumerate(SEGMENT_TITLES):
                        with ui.card().classes("w-full").props(f'id=segment-{i}'):
                            with ui.row().classes(
                                "w-full items-center justify-between"
                            ):
                                ui.label(
                                    f"Segment {i + 1:02d} — {title}"
                                ).classes("text-lg font-bold")

                                checkbox = ui.checkbox(
                                    "Select",
                                    on_change=lambda e, index=i:
                                    toggle_content_segment(index, e.value),
                                )
                                content_checkboxes[i] = checkbox

                            area = ui.textarea(
                                value=segment_contents[i]
                            ).props("outlined autogrow").classes("w-full")

                            area.on(
                                "change",
                                lambda e, index=i, editor=area:
                                segment_contents.__setitem__(index, editor.value),
                            )

        # =================================================
        # MEDIA TAB
        # =================================================
        with ui.tab_panel(media_tab):

            with ui.row().classes("w-full items-end gap-4"):
                segment_select = ui.select(
                    {
                        i: seg_label(i)
                        for i in range(len(SEGMENT_TITLES))
                    },
                    value=0,
                    label="Select Segment",
                ).classes("w-96")

                media_selection_label = ui.label(
                    "Selected prompts: 0"
                ).classes("text-sm text-gray-500")

            with ui.row().classes("w-full gap-2"):
                ui.button("SELECT ALL PROMPTS", on_click=select_all_media).props("outline")
                ui.button("CLEAR", on_click=clear_media_selection).props("outline")
                ui.button(
                    "REGENERATE SELECTED PROMPTS",
                    on_click=mock_regenerate_prompts,
                )

            media_checkbox_by_id = {}
            media_checkboxes = []
            media_container = ui.column().classes("w-full gap-4")

            segment_select.on(
                "update:model-value",
                lambda e: render_media_segment(int(e.value)),
            )

            render_media_segment(0)


ui.run(
    title="AI Film Workspace",
    reload=True,
)