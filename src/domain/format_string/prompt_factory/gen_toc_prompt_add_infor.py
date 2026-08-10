class GenTOCPrompt(str):
    def __new__(cls, keyword, chapter_count: int | None = None):
        text = f'\nOUTLINE TITLE:  {keyword}\n'
        if chapter_count is not None:
            text += f'NUMBER OF CHAPTERS: {chapter_count}\n'
        return super().__new__(cls, text)
