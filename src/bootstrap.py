from src.infrastructure.llm.groq_llm import GroqLLM
from src.infrastructure.llm.openai_llm import OpenAILLM
from src.infrastructure.python_logger import PythonLogger
from src.infrastructure.file_services.text_reader import TextReader
from src.infrastructure.file_services.json_writer import JsonWriter
from src.infrastructure.file_services.sheet_reader import SheetReader
from src.application.message_manager import MessageManager
from src.application.use_case.create_film_plan import CreateFilmPlan
from src.application.use_case.gen_content import GenContent
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


if __name__ == '__main__':
    from pprint import pprint

    prompt_map_path = {
        'char': Config.PROMPTS / 'extract_character_prompt.txt',
    }

    create_film_plan = build_create_film_plan(r"C:\Users\Admin\Downloads\3.txt")
    pprint(create_film_plan._extract_character(prompt_map_path['char']))
    pass
