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
    # try:
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
            else:
                await project_page.page.pause()
            yield prompts
    # except Exception as ex:
    #     print(ex)
    # finally:
    #     await session.close_session()
