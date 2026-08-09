from pydantic import BaseModel
from groq import Groq
from typing import TypeVar
from src.application.ports.logger_port import LoggerService
from src.infrastructure.python_logger import PythonLogger

T = TypeVar("T", bound=BaseModel)  # T là kiểu bất kì nhưng phải kế thừa BaseModel


class CompleteResult:
    def __init__(self, content=None, total_tokens=None, total_time=None, cached_tokens=None, response_model=None):
        self.content = content
        self.total_tokens = total_tokens
        self.total_time = total_time
        self.cached_tokens = cached_tokens
        self.response_model = response_model


class GroqLLM:
    def __init__(
            self,
            api_key,
            default_model="openai/gpt-oss-20b",
            logger: LoggerService | None = None,
    ):
        self.api_key = api_key
        self.default_model = default_model
        self.client = Groq(api_key=api_key)
        self.logger = logger or PythonLogger(__name__)

    def complete(
            self,
            messages: list[dict] | str,
            response_model: type[T] | None = None,
    ) -> CompleteResult:
        '''
        Gửi yêu cầu hoàn thành nội dung tới mô hình Groq và nhận kết quả trả về.
        :param messages: Nội dung gửi tới LLM.
        :param response_model: Pydantic model dùng để validate structured output, nếu None, trả về chuỗi text, nếu có giá trị, kết quả JSON từ LLM sẽ được parse thành instance của model đó.
        :return: Nội dung text do LLM sinh ra nếu không yêu cầu schema | Instance của Pydantic model nếu response_model được cung cấp.
        '''
        self.logger.info(f"{self.__class__.__name__}.{self.complete.__name__}")
        self.logger.debug(f'{messages=}')

        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]

        kwargs = {}
        if response_model is not None:
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": response_model.__name__,
                    "schema": response_model.model_json_schema(),
                },
            }

        response = self.client.chat.completions.create(
            model=self.default_model,
            messages=messages,
            **kwargs,
        )

        content = response.choices[0].message.content

        complete_result = CompleteResult(
            content=content,
            total_tokens=response.usage.total_tokens,
            total_time=response.usage.total_time,
            cached_tokens=response.usage.prompt_tokens_details.cached_tokens,
        )

        if response_model is None:
            return complete_result

        complete_result.response_model = response_model.model_validate_json(content)
        return complete_result

    def extract_text(self, audio_path: str, model: str = 'whisper-large-v3'):
        with open(audio_path, "rb") as file:
            transcription = self.client.audio.transcriptions.create(
                file=(audio_path, file.read()),
                model=model,
                temperature=0,
                response_format="verbose_json",
            )
            return transcription.text


if __name__ == "__main__":
    from src.config import Config

    g = GroqLLM(Config.GROQ_API_KEY)

    # Test audio extract
    # audio_path = Path(r'C:\Users\Admin\Downloads\videoplayback.m4a')
    # text = g.extract_text(str(audio_path))
    # print(text)

    # print(g.complete('Xin chào'))

    pass
