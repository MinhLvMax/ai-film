class GenTOCPrompt(str):
    def __new__(cls, keyword, chapter_count: int | str | None = None):
        text = f'\nOUTLINE TITLE:  {keyword}\n'
        if chapter_count is not None:
            text += f'NUMBER OF CHAPTERS: {str(chapter_count)}\n'
        return super().__new__(cls, text)
