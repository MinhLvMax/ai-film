class SystemPrompt(str):
    def __new__(cls, more_infor: str | None = None):
        text = ''
        if more_infor:
            text = f'\n{more_infor}\n'
        return super().__new__(cls, text)
