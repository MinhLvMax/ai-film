from pydantic import BaseModel, Field


class TitleAnalysisResult(BaseModel):
    main_keyword: str = Field(
        description="Keyword/chủ đề chính của video."
    )

    title_promise: str = Field(
        description="Điều mà tiêu đề đang hứa hẹn cung cấp cho khán giả."
    )

    central_question: str = Field(
        description="Câu hỏi trung tâm mà toàn bộ video cần trả lời."
    )

    audience_interest: str = Field(
        description="Điều khán giả thực sự muốn biết: cảnh đẹp, đời sống, nghịch lý xã hội hoặc chủ đề khác."
    )



