from typing import Protocol


class LLM(Protocol):
    def __init__(self, default_model):
        self.default_model = default_model

    def complete(self, messages: list[dict] | str, llm_model=None, response_model=None):
        pass
