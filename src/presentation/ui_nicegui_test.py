from io import BytesIO
from pathlib import Path
import inspect

import pandas as pd
from nicegui import ui, events, run


# ============================================================
# PUBLIC FUNCTION
# main.py chỉ cần gọi:
#
#     create_ui(backend)
#
# ============================================================

def create_ui(backend):

    # ========================================================
    # STATE CỦA UI
    # ========================================================

    state = {
        # Các kịch bản đã import
        'scripts': {},

        # Kịch bản đang chọn
        'current_script': None,

        # Các đoạn: HOOK, đoạn 1, đoạn 2...
        'segments': [],

        # Các prompt config gửi cho LLM
        'prompt_types': {
            'system_prompt': '',
            'segment_prompt': '',
        },

        # Prompt được sinh ra
        #
        # [
        #     {
        #         'section': 'HOOK',
        #         'image': '...',
        #         'video': '...',
        #     }
        # ]
        'prompt_pairs': [],
    }

    # ========================================================
    # HELPER: GỌI BACKEND
    # ========================================================
    #
    # Hỗ trợ cả:
    #
    # async def backend.xxx()
    #
    # và:
    #
    # def backend.xxx()
    #
    # Nếu backend của bạn gọi LLM/Playwright đồng bộ,
    # run.io_bound giúp không block NiceGUI.
    #
    # ========================================================

    async def call_backend(function, *args, **kwargs):

        if inspect.iscoroutinefunction(function):
            return await function(*args, **kwargs)

        return await run.io_bound(
            function,
            *args,
            **kwargs,
        )

    # ========================================================
    # BACKEND CONNECTION ZONE
    #
    # ĐÂY LÀ KHU VỰC QUAN TRỌNG NHẤT.
    #
    # Nếu tên usecase backend của bạn khác,
    # CHỈ SỬA CÁC HÀM NÀY.
    #
    # Không cần sửa code giao diện.
    # ========================================================

    async def backend_split_script(text: str):
        """
        Phân tích kịch bản thành:

        [
            {
                'title': 'HOOK',
                'text': '...'
            },
            {
                'title': 'Đoạn 1',
                'text': '...'
            }
        ]
        """

        # ----------------------------------------------------
        # CẮM BACKEND TẠI ĐÂY
        # ----------------------------------------------------
        #
        # Ví dụ:
        #
        # return await call_backend(
        #     backend.analyze_screenplay,
        #     text
        # )
        #
        # ----------------------------------------------------

        # Tạm thời dùng parser đơn giản để UI chạy được ngay.
        return basic_split(text)

    async def backend_generate_segment(segment):
        """
        Gen prompt cho MỘT đoạn.
        """

        # Snapshot prompt config hiện tại
        prompt_config = state['prompt_types'].copy()

        # ----------------------------------------------------
        # CẮM USECASE GEN PROMPT CỦA BẠN TẠI ĐÂY
        # ----------------------------------------------------
        #
        # Ví dụ:
        #
        # result = await call_backend(
        #     backend.generate_segment_prompt,
        #     segment=segment,
        #     prompt_config=prompt_config,
        # )
        #
        # return result
        #
        # Backend nên trả:
        #
        # [
        #     {
        #         'image': 'image prompt...',
        #         'video': 'video prompt...'
        #     }
        # ]
        #
        # ----------------------------------------------------

        # DEMO
        return [
            {
                'image': f'IMAGE PROMPT for: {segment["text"][:100]}',
                'video': f'VIDEO PROMPT for: {segment["text"][:100]}',
            }
        ]

    async def backend_generate_all(segments):
        """
        Gen prompt cho toàn bộ kịch bản.
        """

        # Nếu backend của bạn đã có usecase generate toàn bộ,
        # có thể thay toàn bộ vòng for dưới bằng:
        #
        # return await call_backend(
        #     backend.generate_all_prompts,
        #     segments=segments,
        #     prompt_config=state['prompt_types'].copy(),
        # )

        results = []

        for segment in segments:
            pairs = await backend_generate_segment(segment)

            for pair in pairs:
                pair['section'] = segment['title']
                results.append(pair)

        return results

    async def backend_send_all(prompt_pairs):
        """
        Gửi toàn bộ prompt lên web AI / Flow / Veo...
        """

        # ----------------------------------------------------
        # CẮM PLAYWRIGHT / FLOW USECASE Ở ĐÂY
        # ----------------------------------------------------
        #
        # Ví dụ:
        #
        # await call_backend(
        #     backend.send_all_prompts,
        #     prompt_pairs
        # )
        #
        # ----------------------------------------------------

        print('SEND ALL:')

        for pair in prompt_pairs:
            print(pair)

    # ========================================================
    # FILE READER
    # ========================================================

    def read_script_file(filename: str, raw: bytes) -> str:

        extension = Path(filename).suffix.lower()

        # TXT / Markdown
        if extension in {'.txt', '.md'}:
            return raw.decode('utf-8-sig')

        # CSV
        if extension == '.csv':
            df = pd.read_csv(BytesIO(raw), header=None)
            return dataframe_to_text(df)

        # Excel
        if extension in {'.xlsx', '.xls'}:
            df = pd.read_excel(BytesIO(raw), header=None)
            return dataframe_to_text(df)

        raise ValueError(
            f'Không hỗ trợ file {extension}'
        )

    def dataframe_to_text(df):
        """
        Ghép các cell Excel / CSV thành text.
        """

        lines = []

        for _, row in df.iterrows():

            values = [
                str(value)
                for value in row
                if pd.notna(value)
            ]

            if values:
                lines.append(' '.join(values))

        return '\n'.join(lines)

    # ========================================================
    # PARSER DEMO
    # ========================================================

    def basic_split(text):
        """
        Parser rất đơn giản để test UI.

        Sau này backend_split_script() sẽ gọi LLM/usecase thật.
        """

        chunks = [
            chunk.strip()
            for chunk in text.split('\n\n')
            if chunk.strip()
        ]

        segments = []

        for index, chunk in enumerate(chunks):

            if index == 0:
                title = 'HOOK'
            else:
                title = f'Đoạn {index}'

            segments.append({
                'title': title,
                'text': chunk,
            })

        return segments

    # ========================================================
    # SCRIPT EVENTS
    # ========================================================

    async def upload_script(
        e: events.UploadEventArguments,
    ):
        """
        Import script từ file.
        """

        try:
            raw = await e.file.read()

            text = read_script_file(
                e.file.name,
                raw,
            )

            state['scripts'][e.file.name] = text
            state['current_script'] = e.file.name

            # Cập nhật select
            script_select.options = list(
                state['scripts'].keys()
            )

            script_select.value = e.file.name
            script_select.update()

            # Đưa nội dung vào textarea
            script_text.value = text
            script_text.update()

            await analyze_script()

            ui.notify(
                f'Đã import {e.file.name}',
                type='positive',
            )

        except Exception as error:

            ui.notify(
                str(error),
                type='negative',
            )

    async def add_pasted_script():
        """
        Người dùng paste trực tiếp script.
        """

        text = script_text.value.strip()

        if not text:
            ui.notify('Chưa có nội dung kịch bản')
            return

        name = script_name.value.strip()

        if not name:
            name = f'Kịch bản {len(state["scripts"]) + 1}'

        state['scripts'][name] = text
        state['current_script'] = name

        script_select.options = list(
            state['scripts'].keys()
        )

        script_select.value = name
        script_select.update()

        await analyze_script()

    async def select_script(name):
        """
        Khi người dùng chọn một script khác.
        """

        if not name:
            return

        state['current_script'] = name

        script_text.value = state['scripts'][name]
        script_text.update()

        await analyze_script()

    async def analyze_script():
        """
        Tách screenplay thành HOOK / đoạn 1 / đoạn 2...
        """

        text = script_text.value.strip()

        if not text:
            return

        state['segments'] = await backend_split_script(text)

        # Kịch bản mới -> clear prompt cũ
        state['prompt_pairs'].clear()

        render_segments.refresh()
        render_prompt_pairs.refresh()

    # ========================================================
    # PROMPT CONFIG EVENTS
    # ========================================================

    def update_prompt(name, value):
        state['prompt_types'][name] = value

    def add_prompt_type():
        """
        Cho phép thêm prompt mới:
        character prompt
        cinematography prompt
        subject prompt
        ...
        """

        name = new_prompt_name.value.strip()

        if not name:
            return

        if name in state['prompt_types']:
            ui.notify('Prompt này đã tồn tại')
            return

        state['prompt_types'][name] = ''

        new_prompt_name.value = ''

        render_prompt_config.refresh()

    # ========================================================
    # GENERATION EVENTS
    # ========================================================

    async def generate_segment(index):
        """
        Gen riêng một section.
        """

        segment = state['segments'][index]

        ui.notify(
            f'Đang gen {segment["title"]}'
        )

        pairs = await backend_generate_segment(
            segment
        )

        for pair in pairs:

            state['prompt_pairs'].append({
                'section': segment['title'],
                'image': pair['image'],
                'video': pair['video'],
            })

        render_prompt_pairs.refresh()

    async def generate_all():
        """
        GEN TOÀN BỘ SCRIPT
        """

        if not state['segments']:
            ui.notify('Chưa có kịch bản')
            return

        ui.notify('Đang tạo toàn bộ prompt...')

        result = await backend_generate_all(
            state['segments']
        )

        state['prompt_pairs'] = result

        render_prompt_pairs.refresh()

        ui.notify(
            'Đã tạo xong',
            type='positive',
        )

    async def send_all():
        """
        SEND TOÀN BỘ PROMPT.
        """

        if not state['prompt_pairs']:
            ui.notify('Chưa có prompt để gửi')
            return

        await backend_send_all(
            state['prompt_pairs']
        )

        ui.notify(
            'Đã gửi prompt',
            type='positive',
        )

    # ========================================================
    # UI COMPONENT: SEGMENTS
    # ========================================================

    @ui.refreshable
    def render_segments():

        if not state['segments']:
            ui.label(
                'Chưa có đoạn kịch bản'
            ).classes('text-gray-400')

            return

        for index, segment in enumerate(
            state['segments']
        ):

            with ui.card().classes(
                'w-full p-3'
            ):

                with ui.row().classes(
                    'w-full items-center justify-between'
                ):

                    ui.label(
                        segment['title']
                    ).classes(
                        'font-bold'
                    )

                    ui.button(
                        'GEN',
                        on_click=lambda index=index:
                            generate_segment(index),
                    ).props(
                        'flat dense'
                    )

                ui.label(
                    segment['text']
                ).classes(
                    'text-sm text-gray-600'
                )

    # ========================================================
    # UI COMPONENT: PROMPT CONFIG
    # ========================================================

    @ui.refreshable
    def render_prompt_config():

        for name, value in state[
            'prompt_types'
        ].items():

            ui.textarea(
                label=name,
                value=value,
                on_change=lambda e, name=name:
                    update_prompt(
                        name,
                        e.value,
                    ),
            ).props(
                'outlined autogrow'
            ).classes(
                'w-full'
            )

    # ========================================================
    # UI COMPONENT: SINGLE PROMPT LINE
    # ========================================================

    def prompt_line(
        title,
        pair,
        key,
    ):

        with ui.row().classes(
            'w-full items-start no-wrap'
        ):

            ui.label(
                title
            ).classes(
                'w-16 pt-3 font-bold text-xs'
            )

            editor = ui.textarea(
                value=pair[key],
                on_change=lambda e:
                    pair.__setitem__(
                        key,
                        e.value,
                    ),
            ).props(
                'readonly outlined autogrow'
            ).classes(
                'flex-1'
            )

            # EDIT
            ui.button(
                icon='edit',
                on_click=lambda:
                    editor.props(
                        remove='readonly'
                    ),
            ).props(
                'flat round dense'
            ).tooltip(
                'Sửa'
            )

            # COPY
            async def copy_prompt():
                await ui.clipboard.write(
                    editor.value
                )

                ui.notify(
                    'Đã copy'
                )

            ui.button(
                icon='content_copy',
                on_click=copy_prompt,
            ).props(
                'flat round dense'
            ).tooltip(
                'Sao chép'
            )

    # ========================================================
    # UI COMPONENT: GENERATED PROMPTS
    # ========================================================

    @ui.refreshable
    def render_prompt_pairs():

        if not state['prompt_pairs']:

            ui.label(
                'Prompt sinh ra sẽ xuất hiện ở đây'
            ).classes(
                'text-gray-400'
            )

            return

        for index, pair in enumerate(
            state['prompt_pairs']
        ):

            with ui.card().classes(
                'w-full p-3'
            ):

                ui.label(
                    f'{index + 1:02d} · '
                    f'{pair.get("section", "")}'
                ).classes(
                    'font-bold'
                )

                # Row con 1
                prompt_line(
                    'IMAGE',
                    pair,
                    'image',
                )

                # Row con 2
                prompt_line(
                    'VIDEO',
                    pair,
                    'video',
                )

    # ========================================================
    # ====================== LAYOUT ===========================
    # ========================================================

    ui.label(
        'AI Film Prompt Studio'
    ).classes(
        'text-2xl font-bold mb-3'
    )

    with ui.row().classes(
        'w-full items-start flex-nowrap gap-3'
    ):

        # ====================================================
        # LEFT
        # ====================================================

        with ui.column().classes(
            'w-1/4 gap-3'
        ):

            ui.label(
                'KỊCH BẢN'
            ).classes(
                'font-bold'
            )

            # Import file
            ui.upload(
                label='Import script',
                on_upload=upload_script,
                auto_upload=True,
                multiple=True,
            ).props(
                'accept=.txt,.md,.csv,.xlsx,.xls'
            ).classes(
                'w-full'
            )

            # Chọn script
            script_select = ui.select(
                [],
                label='Kịch bản',
                on_change=lambda e:
                    select_script(e.value),
            ).classes(
                'w-full'
            )

            script_name = ui.input(
                'Tên kịch bản'
            ).classes(
                'w-full'
            )

            # Paste script
            script_text = ui.textarea(
                label='Hoặc dán kịch bản vào đây'
            ).props(
                'outlined'
            ).classes(
                'w-full h-48'
            )

            ui.button(
                'THÊM / PHÂN TÍCH KỊCH BẢN',
                on_click=add_pasted_script,
            ).classes(
                'w-full'
            )

            ui.separator()

            ui.label(
                'CÁC ĐOẠN'
            ).classes(
                'font-bold'
            )

            render_segments()

        # ====================================================
        # CENTER
        # ====================================================

        with ui.column().classes(
            'w-1/4 gap-3'
        ):

            ui.label(
                'PROMPT CONFIG'
            ).classes(
                'font-bold'
            )

            render_prompt_config()

            ui.separator()

            with ui.row().classes(
                'w-full items-center'
            ):

                new_prompt_name = ui.input(
                    'Loại prompt mới'
                ).classes(
                    'flex-1'
                )

                ui.button(
                    icon='add',
                    on_click=add_prompt_type,
                ).props(
                    'round'
                )

        # ====================================================
        # RIGHT
        # ====================================================

        with ui.column().classes(
            'w-1/2 gap-3'
        ):

            with ui.row().classes(
                'w-full items-center justify-between'
            ):

                ui.label(
                    'GENERATED PROMPTS'
                ).classes(
                    'font-bold'
                )

                with ui.row():

                    ui.button(
                        'GEN TOÀN BỘ',
                        icon='auto_awesome',
                        on_click=generate_all,
                    )

                    ui.button(
                        'SEND TOÀN BỘ',
                        icon='send',
                        on_click=send_all,
                    )

            render_prompt_pairs()