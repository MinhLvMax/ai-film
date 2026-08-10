from src.infrastructure.groq_llm import GroqLLM
from src.infrastructure.python_logger import PythonLogger
from src.infrastructure.text_reader import TextReader
from src.application.context_manager import ContextManager
from src.application.use_case.gen_content import GenContent
from src.config import Config


def build_gen_content():
    gen_toc_llm = GroqLLM(Config.GROQ_API_KEY, 'openai/gpt-oss-20b')
    gen_chap_llm = GroqLLM(Config.GROQ_API_KEY, 'openai/gpt-oss-120b')
    logger = PythonLogger(__name__)
    context_manager = ContextManager()
    return GenContent(
        gen_toc_llm,
        gen_chap_llm,
        logger,
        context_manager
    )


if __name__ == '__main__':
    from pprint import pprint
    import re
    from src.application.dto.gen_content_dto import GenContentDTO
    from src.infrastructure.text_reader import TextReader
    from src.infrastructure.text_writer import TextWriter

    text_reader = TextReader()
    text_writer = TextWriter()
    gen_content = build_gen_content()
    prompt_paths_map = {
        'system': Config.PROMPTS / 'system_prompt.txt',
        'toc': Config.PROMPTS / 'gentoc_prompt.txt',
        'chap': Config.PROMPTS / 'genchap_prompt.txt',
    }
    input = GenContentDTO(
        title='VOYAGER 1 Câu chuyện về 10 nghìn tỷ năm tiếp theo | Space Documentary',
        system_prompt=text_reader.read(prompt_paths_map['system']),
        gen_toc_prompt=text_reader.read(prompt_paths_map['toc']),
        gen_chapter_prompt=text_reader.read(prompt_paths_map['chap']),
        chapter_length=500,
        chapter_count=5,
        sleep_time=30,
    )

    output = gen_content.gen(input)
    print(f'- {output.title=}')
    pprint(f'- {output.toc}=')
    print(f'- {output.chaps}=')

    full_content = (
        f'Title: {output.title}\n'
        f'{'\n\n'.join(output.chaps)}'
    )

    path = Config.DOWNLOADS / f'{output.title}.txt'
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', path.name)
    safe_path = path.parent / safe_name
    text_writer.write(full_content, safe_path)
