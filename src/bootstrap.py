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
    pass
