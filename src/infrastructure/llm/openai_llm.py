from typing import TypeVar
from pydantic import BaseModel
from openai import AsyncOpenAI
from src.infrastructure.python_logger import PythonLogger
from src.application.ports.logger_port import LoggerService
from src.application.dto.llm_complete_results import CompleteResult

T = TypeVar("T", bound=BaseModel)  # T là kiểu bất kì nhưng phải kế thừa BaseModel


class OpenAILLM:
    def __init__(
            self,
            api_key,
            default_model="gpt-5.6-luna",
            default_reasoning_effort="max",
            logger: LoggerService | None = None,
    ):
        self.api_key = api_key
        self.default_model = default_model
        self.default_reasoning_effort = default_reasoning_effort
        self.client = AsyncOpenAI(api_key=api_key)
        self.logger = logger or PythonLogger(__name__)

    async def complete(
            self,
            messages: list[dict] | str,
            response_model: type[T] | None = None,
            llm_model: str | None = None,
            reasoning_effort: str | None = None,
    ):

        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]

        model = llm_model or self.default_model
        reasoning_effort = (
                reasoning_effort or self.default_reasoning_effort
        )

        if response_model is None:
            response = await self.client.responses.create(
                model=model,
                input=messages,
                reasoning={
                    "effort": reasoning_effort,
                },
                tools=[
                    {"type": "web_search"}
                ],
                tool_choice="auto",
            )

            return CompleteResult(
                content=response.output_text,
            )

        response = await self.client.responses.parse(
            model=model,
            input=messages,
            text_format=response_model,
            reasoning={
                "effort": reasoning_effort,
            },
            tools=[
                {"type": "web_search"}
            ],
            tool_choice="auto",
        )

        return CompleteResult(
            content=response.output_text,
            response_model=response.output_parsed,
        )

    async def get_list_models(self):
        model_list = await self.client.models.list()
        model_ids = [model.id for model in model_list]
        from pprint import pprint
        pprint(model_ids)


async def main():
    from src.config import Config
    # import os

    # open_ai = OpenAILLM(Config.OPEN_API_KEY)
    # open_ai.get_list_models()

    # OPEN_API_KEY = os.getenv("OPEN_API_KEY")  # Load OPENAI_API_KEY từ biến môi trường
    # client = AsyncOpenAI(api_key=OPEN_API_KEY)
    #
    # response = await client.responses.create(
    #     model="gpt-5.6-sol",
    #     input="Xin chào, hãy giới thiệu bản thân."
    # )
    #
    # print(response.output_text)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
