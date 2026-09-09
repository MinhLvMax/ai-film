from src.application.use_case.analysis_script import AnalysisScript
from src.application.use_case.build_prompt import build_prompt_from_chars_and_shots
from src.application.ui_capabilities import UICapabilities
from src.infrastructure.llm.openai_llm import OpenAILLM
from src.infrastructure.auto_sent_gg_flow import send_prompt_sequentiallys
from src.config import Config


def build_ui_capabilities():
    llm = OpenAILLM(Config.OPEN_API_KEY)
    analysis_script = AnalysisScript(llm)
    return UICapabilities(
        analysis_script=analysis_script,
        build_prompt_method=build_prompt_from_chars_and_shots,
        send_prompt_method=send_prompt_sequentiallys,
    )


uicapabilities = build_ui_capabilities()

if __name__ == '__main__':
    ''''''
