from src.domain.prompt_factory.gen_content_prompt import GenContentPrompt


class FormatStringFactory:
    def gen_content_prompt(
            self,
            keyword: str,
            description: str,
    ) -> GenContentPrompt:
        '''
        Tạo prompt dùng để sinh nội dung dựa trên chủ đề và mô tả.
        :param keyword: Chủ đề chính cần sinh nội dung.
        :param description: Mô tả bổ sung giúp AI hiểu rõ phạm vi và yêu cầu.
        :return: GenContentPrompt: Prompt đã được khởi tạo và format sẵn, sẵn sàng truyền vào LLM.
        '''
        return GenContentPrompt(
            keyword=keyword,
            description=description,
        )
