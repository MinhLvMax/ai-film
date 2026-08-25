from src.infrastructure.auto_sent_gg_flow.session import GoogleFlowSession
from src.domain import VideoGenerationMode, Ratio, Quantity, Durations, VideoModels


async def send_prompt_to_gen_vids(
        prompts: list[dict],
        generation_mode: VideoGenerationMode,
        ratio: Ratio,
        quantity: Quantity,
        duration: Durations,
        model: VideoModels,
        project_name: str = 'Default project name',
):
    '''Tạo các video đơn lẻ từ danh sách prompts trên nền tảng google flow'''
    session = await GoogleFlowSession().start()
    # try:
    home_page = session.home_page
    await home_page.page.goto(home_page.URL)
    await home_page.create_with_google_flow()
    project_page = await home_page.open_or_create_new_project(project_name)

    for prompt in prompts:
        is_sent = prompt.get('is_sent', False)
        if is_sent:
            continue
        else:
            await project_page.create_a_video(
                video_prompt=prompt['prompt'],
                generation_mode=generation_mode,
                ratio=ratio,
                quantity=quantity,
                duration=duration,
                model=model
            )
            prompt["is_sent"] = True
    # except Exception as ex:
    #     print(ex)
    # finally:
    #     await session.close_session()
