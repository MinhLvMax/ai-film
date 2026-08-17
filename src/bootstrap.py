from src.infrastructure.llm.groq_llm import GroqLLM
from src.infrastructure.llm.openai_llm import OpenAILLM
from src.infrastructure.python_logger import PythonLogger
from src.infrastructure.file_services.text_reader import TextReader
from src.infrastructure.file_services.json_writer import JsonWriter
from src.infrastructure.file_services.sheet_reader import SheetReader
from src.application.message_manager import MessageManager
from src.application.use_case.create_film_plan import CreateFilmPlan
from src.application.use_case.gen_content import GenContent
from src.application.use_case.gen_prompts import GenPrompt
from src.config import Config


def build_gen_content():
    gen_toc_llm = OpenAILLM(Config.OPEN_API_KEY)
    # gen_toc_llm = GroqLLM(Config.GROQ_API_KEY, 'openai/gpt-oss-20b')
    gen_chap_llm = GroqLLM(Config.GROQ_API_KEY, 'openai/gpt-oss-120b')
    logger = PythonLogger(__name__)
    context_manager = MessageManager()
    return GenContent(
        gen_toc_llm,
        gen_chap_llm,
        logger,
        context_manager
    )


def build_create_film_plan(screenplay_path: str):
    llm = OpenAILLM(Config.OPEN_API_KEY)
    json_writer = JsonWriter()
    # sheet_reader = SheetReader()
    text_reader = TextReader()
    return CreateFilmPlan(llm, text_reader, json_writer, screenplay_path)


def build_gen_prompts():
    llm = OpenAILLM(Config.OPEN_API_KEY)
    text_reader = TextReader()
    return GenPrompt(text_reader, llm, Config.PROMPTS / 'gen_prompt_from_segment.txt')


def build_send_prompts(prompts):
    from src.auto_gen.main import build_gen_services
    return build_gen_services(prompts)


# def build_app():
#     class App():
#         pass
#
#     return App


if __name__ == '__main__':
    from pprint import pprint

    prompt_map_path = {
        'char': Config.PROMPTS / 'extract_character_prompt.txt',
        'seg': Config.PROMPTS / 'gen_prompt_from_segment.txt'
    }

    create_film_plan = build_create_film_plan(r"C:\Users\Admin\Downloads\3.txt")
    # pprint(create_film_plan._extract_character(prompt_map_path['char']))

    segments = create_film_plan._sreenplay_chunking()
    HOOK = segments[0]
    prompts = create_film_plan.gen_prompt_from_a_segment(prompt_map_path['seg'], HOOK)
    pprint(prompts)
    pass
