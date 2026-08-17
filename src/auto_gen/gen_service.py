from src.auto_gen.pages.google_flow_page import GoogleFlowPage
from src.auto_gen.json_reader import JsonReader
from src.auto_gen.json_writer import JsonWriter
from src.auto_gen.constant import GenMode
from src.auto_gen.pages.generation_config import ImageGenerationConfig, VideoGenerationConfig
from src.auto_gen.constant.resoluion import Resolution
from pathlib import Path
import time
import random


class GenService:
    def __init__(
            self,
            google_flow_page_obj: GoogleFlowPage,
            image_gen_config: ImageGenerationConfig | None = None,
            video_gen_config: VideoGenerationConfig | None = None,
    ):
        self.google_flow_page_obj = google_flow_page_obj

        self.image_gen_config = image_gen_config or ImageGenerationConfig()
        self.video_gen_config = video_gen_config or VideoGenerationConfig()

        self.reader = JsonReader()
        self.writer = JsonWriter()

    def _is_prompt_completed(self, data: list[dict]) -> bool:
        return all(
            pair.get("image_done") and pair.get("video_done")
            for pair in data
        )

    def run_prompt_file(self, prompt_path: Path):
        print(f'Chạy phân cảnh {prompt_path}')

        data = self.reader.read(path=prompt_path)

        if data is None:
            print(f'{prompt_path} không có dữ liệu')
            return

        if self._is_prompt_completed(data):
            print(f"{prompt_path} đã hoàn thành, bỏ qua.")
            return

        self.google_flow_page_obj.go_to_this_page()
        self.google_flow_page_obj.create_with_google_flow()

        prj_page = self.google_flow_page_obj.get_or_create_new_project(prompt_path.stem)

        start = time.time()
        for i, pair in enumerate(data):
            print(f'Cặp thứ {i}/{len(data)}')
            if pair.get("image_done"):
                print("skip image")
            else:
                prj_page.send_a_prompt(
                    pair.get('image'),
                    GenMode.IMAGE,
                    self.image_gen_config
                )
                prj_page.wait_until_creating_image_below(1)
                pair["image_done"] = True

            if pair.get("video_done"):
                print("skip video")
                continue
            else:
                prj_page.wait_until_creating_video_below(
                    1)  # Check đầu check cuối cho chắc vì lúc vừa gửi video thì nó load mấy trạng thái khác nhau ko phát hiện chính xác được là có cái nào đang tạo hay không
                prj_page.create_video_from_latest_image(
                    pair.get('video'),
                    self.video_gen_config
                )
                pair["video_done"] = True
                prj_page.wait_until_creating_video_below(1)

            print('Lưu trạng thái gen')
            self.writer.write(prompt_path, data)

            print('Nghỉ 1 chút')
            prj_page.wait_for_seconds(random.randint(5, 10))

        end = time.time()
        print(f"Thời gian chạy: {end - start:.2f} giây")

    def run_prompt_folder(self, prompt_folder_path):
        '''

        :param prompt_folder_path: folder chứa các json prompt
        :return:
        '''
        print(f'Chạy tạo dự án {prompt_folder_path}')
        prompt_folder_path = self._get_prompt_files(prompt_folder_path)
        for prompt_file_path in prompt_folder_path:
            self.run_prompt_file(prompt_file_path)

    def _get_prompt_files(self, prompt_folder: Path) -> list[Path]:
        print('Lấy danh sách file json')

        files = sorted(
            file
            for file in prompt_folder.glob("*.json")
            if file.is_file()
        )

        print(files)
        return files

    def send_prompts(self, prompts: list[dict[str, str]]) -> None:
        '''
        Nhận vào 1 danh sách prompt và thực hiện gửi toàn bộ để gen
        :param prompts:
        :return:
        '''
        data = prompts
        self.google_flow_page_obj.go_to_this_page()
        self.google_flow_page_obj.create_with_google_flow()

        prj_page = self.google_flow_page_obj.get_or_create_new_project('new_project')

        start = time.time()
        for i, pair in enumerate(data):
            print(f'Cặp thứ {i}/{len(data)}')
            if pair.get("image_done"):
                print("skip image")
            else:
                prj_page.send_a_prompt(
                    pair.get('image'),
                    GenMode.IMAGE,
                    self.image_gen_config
                )
                prj_page.wait_until_creating_image_below(1)
                pair["image_done"] = True

            if pair.get("video_done"):
                print("skip video")
                continue
            else:
                prj_page.wait_until_creating_video_below(
                    1)  # Check đầu check cuối cho chắc vì lúc vừa gửi video thì nó load mấy trạng thái khác nhau ko phát hiện chính xác được là có cái nào đang tạo hay không
                prj_page.create_video_from_latest_image(
                    pair.get('video'),
                    self.video_gen_config
                )
                pair["video_done"] = True
                prj_page.wait_until_creating_video_below(1)

            print('Nghỉ 1 chút')
            prj_page.wait_for_seconds(random.randint(5, 10))

        end = time.time()
        print(f"Thời gian chạy: {end - start:.2f} giây")
