from typing import TypeVar
from pydantic import BaseModel
from openai import OpenAI
from src.infrastructure.python_logger import PythonLogger
from src.application.ports.logger_port import LoggerService
from src.application.dto.llm_complete_results import CompleteResult

T = TypeVar("T", bound=BaseModel)  # T là kiểu bất kì nhưng phải kế thừa BaseModel


class OpenAILLM:
    def __init__(
            self,
            api_key,
            default_model="gpt-5.6-luna",
            logger: LoggerService | None = None,
    ):
        self.api_key = api_key
        self.default_model = default_model
        self.client = OpenAI(api_key=api_key)
        self.logger = logger or PythonLogger(__name__)

    def complete(
            self,
            messages: list[dict] | str,
            response_model: type[T] | None = None,
            llm_model: str | None = None,
    ):
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]

        if response_model is None:
            response = self.client.responses.create(
                model=llm_model if llm_model else self.default_model,
                input=messages,
            )

            return CompleteResult(
                content=response.output_text,
            )

        response = self.client.responses.parse(
            model=llm_model if llm_model else self.default_model,
            input=messages,
            text_format=response_model,
        )

        return CompleteResult(
            content=response.output_text,
            response_model=response.output_parsed,
        )

    def get_list_models(self):
        model_list = self.client.models.list()
        model_ids = [model.id for model in model_list]
        from pprint import pprint
        pprint(model_ids)


if __name__ == '__main__':
    from src.config import Config

    open_ai = OpenAILLM(Config.OPEN_API_KEY)
    open_ai.get_list_models()

# OPEN_API_KEY = os.getenv("OPEN_API_KEY")  # Load OPENAI_API_KEY từ biến môi trường
# client = OpenAI(api_key=OPEN_API_KEY)

# response = client.responses.create(
#     model="gpt-5",
#     input="Xin chào, hãy giới thiệu bản thân."
# )

# print(response.output_text)
