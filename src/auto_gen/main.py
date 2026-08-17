import random
import time
from src.auto_gen.constant.resoluion import Resolution
from src.auto_gen.context_factory.chrome_context_factory import ChromeContextFactory
from src.auto_gen.pages.generation_config import ImageGenerationConfig, VideoGenerationConfig
from pathlib import Path
from src.auto_gen.pages.google_flow_page import GoogleFlowPage
from src.config import Config
from src.auto_gen.constant import GenMode, VideoModelNameString, ImageModelNameString
from src.auto_gen.gen_service import GenService


def build_gen_services(prompts):
    context_factory_obj = ChromeContextFactory()
    user_profile = Config.PROJECT_PATH / r'src\auto_gen\profiles\user0'
    gen_context = context_factory_obj.create_context(user_profile=user_profile,
                                                     download_path=Path('../downloads'))

    # Trang chủ chứa các dự án
    google_flow_page_obj = GoogleFlowPage(gen_context.new_page())

    # Từ chỗ này trở xuống call dịch vụ
    google_flow_page_obj.go_to_this_page()
    google_flow_page_obj.create_with_google_flow()

    # print('Dừng để thêm tính năng tự tải sau khi tạo') # chưa làm xong
    # google_flow_page_obj.pause_page()

    # Cấu hình gen ảnh
    image_generation_config = ImageGenerationConfig(
        model_name=ImageModelNameString.Nano_Banana_2
    )
    # Cấu hình gen video
    video_generation_config = VideoGenerationConfig(
        model_name=VideoModelNameString.VEO_3_1_LITE_LOWER_PRIORITY
    )

    # Khởi tạo dịch vụ gen
    gen_service = GenService(google_flow_page_obj, image_generation_config, video_generation_config)
    # Truyền prompts vào và chạy
    gen_service.send_prompts(prompts)
    pass


if __name__ == '__main__':
    prompts = [
        {
            'image': 'A cute golden retriever puppy running through a field of wildflowers, cinematic photography, warm sunlight',
            'video': 'A golden retriever puppy happily running through a field of wildflowers, slow motion, cinematic camera movement'
        },
        {
            'image': 'A majestic Bengal tiger sitting on a mossy rock in a dense jungle, dramatic lighting, ultra realistic',
            'video': 'A Bengal tiger slowly walking through a dense jungle, sunlight filtering through the trees, cinematic wildlife footage'
        },
        {
            'image': 'A red panda eating bamboo on a tree branch in a misty forest, adorable, highly detailed',
            'video': 'A red panda climbing a tree and eating bamboo, gentle movements, natural forest environment'
        },
    ]

    build_gen_services(prompts)
    pass

# ===========
# # Trang của 1 dự án cụ thể
# prj_page = google_flow_page_obj.get_or_create_new_project('Minh bài 13 phần outro')
#
# # Các đối tượng đọc ghi
# reader = JsonReader()
# writer = JsonWriter()
#
# data = reader.read(path=Path('input/input.json'))
#
#
# start = time.time()
# for i, pair in enumerate(data):
#     print(f'Cặp thứ {i}/{len(data)}')
#     if pair.get("image_done"):
#         print("skip image")
#     else:
#         prj_page.send_a_prompt(
#             pair.get('image'),
#             GenMode.IMAGE,
#             ImageGenerationConfig()
#         )
#         prj_page.wait_until_creating_image_below(1)
#         pair["image_done"] = True
#
#     if pair.get("video_done"):
#         print("skip video")
#         continue
#     else:
#         prj_page.create_video_from_latest_image(
#             pair.get('video'),
#             VideoGenerationConfig()
#         )
#         pair["video_done"] = True
#         prj_page.wait_until_creating_video_below(1)
#
#     print('Lưu trạng thái gen')
#     writer.write(Path('input/input.json'), data)
#
#     print('Nghỉ 1 chút')
#     prj_page.wait_for_seconds(random.randint(5, 10))
#
# end = time.time()
# print(f"Thời gian chạy: {end - start:.2f} giây")
