import random
from src.infrastructure.auto_sent_gg_flow.session import GoogleFlowSession
from src.domain import VideoGenerationMode, Ratio, Quantity, Durations, VideoModels
from src.infrastructure.auto_sent_gg_flow.home_page import ProjectPage


async def send_prompt_to_gen_vids(
        prompts: list[dict],
        generation_mode: VideoGenerationMode,
        ratio: Ratio,
        quantity: Quantity,
        duration: Durations,
        model: VideoModels,
        max_creating: int,
        project_name: str = 'Default project name',
):
    '''Tạo các video đơn lẻ từ danh sách prompts trên nền tảng google flow'''

    session = await GoogleFlowSession().start()
    try:
        home_page = session.home_page
        await home_page.page.goto(home_page.URL)
        project_page: ProjectPage = await home_page.open_or_create_new_project(project_name)

        for prompt in prompts:
            is_sent = prompt.get('is_sent', False)
            if is_sent:
                continue
            else:
                is_sent = await project_page.create_a_video(
                    video_prompt=prompt['prompt'],
                    generation_mode=generation_mode,
                    ratio=ratio,
                    quantity=quantity,
                    duration=duration,
                    model=model,
                    max_creating=max_creating,
                )
                if is_sent:
                    prompt["is_sent"] = True
                    print('Nghỉ chút trước khi gửi video tiếp theo')
                    await project_page.page.wait_for_timeout(30000)
                else:
                    await session.clear_cache()
                    await session.close_session()
                    # await project_page.page.pause()
                    break
                yield prompts
    except Exception as ex:
        print(ex)
        print('Có lỗi gì đó trong quá trình gửi gen tự động nên dừng lại')
        await home_page.page.pause()
    finally:
        await session.close_session()


async def send_prompt_sequentiallys(
        prompts: list[dict],
        project_url: str,
        sleep_time: int,
        browser_name: str,
):
    '''Gửi lần lượt prompt, có thời gian nghỉ'''
    session = await GoogleFlowSession(
        browser_name=browser_name,  # Cải tiến chọn ở giao diện sau -> cải tiến rồi
        # executable_path=r"C:\Program Files\CocCoc\Browser\Application\browser.exe"
    ).start()
    await session.page.goto(
        url=project_url
    )
    project_page = ProjectPage(session.page)

    # Tắt chế độ tác nhân
    await project_page.turn_off_agent_mode()

    # Duyệt và gửi prompts
    for prompt in prompts:
        if prompt.get('is_sent'):
            continue
        else:
            # Gửi
            await project_page.fill_and_send_prompt(prompt.get('prompt'))

            # Nghỉ ramdom giây trước khi tạo tiếp
            min_sleep = max(0, sleep_time - 10)
            max_sleep = sleep_time + 10

            new_sleep_time = random.uniform(
                min_sleep,
                max_sleep
            )
            new_sleep_time = max(0, new_sleep_time)
            for remaining in range(int(new_sleep_time), 0, -1):
                print(f"\rCòn {remaining}s...", end="", flush=True)
                await session.page.wait_for_timeout(1000)

            # Check cảnh báo
            is_exist_notification = await project_page.check_notification()
            if is_exist_notification:
                print('Có cảnh báo, dừng quá trình')
                prompt["is_sent"] = False

                await session.clear_cache()
                await session.close_session()
                # Debug
                # print('Dừng để debug')
                # await session.page.pause()

                break

            # Gán trạng thái đã gửi
            prompt["is_sent"] = True

            # Gửi ngược danh sách prompt sau khi update ra giao diện
            yield prompts
