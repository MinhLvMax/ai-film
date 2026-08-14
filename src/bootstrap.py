from src.infrastructure.groq_llm import GroqLLM
from src.infrastructure.python_logger import PythonLogger
from src.application.message_manager import MessageManager
from src.application.use_case.gen_content import GenContent
from src.config import Config


def build_gen_content():
    gen_toc_llm = GroqLLM(Config.GROQ_API_KEY, 'openai/gpt-oss-20b')
    gen_chap_llm = GroqLLM(Config.GROQ_API_KEY, 'openai/gpt-oss-120b')
    logger = PythonLogger(__name__)
    context_manager = MessageManager()
    return GenContent(
        gen_toc_llm,
        gen_chap_llm,
        logger,
        context_manager
    )


if __name__ == '__main__':
    pass
