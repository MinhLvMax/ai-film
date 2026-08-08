from typing import Protocol


class LLMService(Protocol):
    def __init__(self, default_model):
        self.default_model = default_model

    def complete(self, messages: list[dict] | str, response_model=None):
        pass
