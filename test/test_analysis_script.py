from src.application.use_case.analysis_script import AnalysisScript
from src.infrastructure.llm.openai_llm import OpenAILLM
from src.infrastructure.file_services.text_reader import TextReader
from src.config import Config

if __name__ == '__main__':
    llm = OpenAILLM(Config())
    text_reader = TextReader()
    analysis_script = AnalysisScript(llm)
    content = text_reader.read(r"C:\Users\Admin\Downloads\3.txt")
    from pprint import pprint
    pprint(analysis_script._sreenplay_chunking(content))
    pass
