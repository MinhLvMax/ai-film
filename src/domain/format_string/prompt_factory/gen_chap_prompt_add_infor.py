class GenChapPrompt(str):
    def __new__(
            cls,
            chapter_name,
            chapter_summary: str | None = None,
            target_length: int | None = None,
    ):
        text = f'\nCHAPTER TITLE: {chapter_name}\n'

        if chapter_summary is not None:
            text += f'CHAPTER SUMMARY: {chapter_summary}\n'

        if target_length is not None:
            text += f'TARGET LENGTH: {target_length}\n'

        return super().__new__(cls, text)
