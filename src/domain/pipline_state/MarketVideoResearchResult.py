from pydantic import BaseModel, Field


class VideoResearchResult(BaseModel):
    title: str
    url: str
    channel_name: str

    view_count: int | None = None
    published_at: str | None = None

    captions: list[dict] = Field(
        default_factory=list,
        description='Captions của video'
    )

    relevance_score: float = Field(
        description="Mức độ liên quan của video với chủ đề đang nghiên cứu."
    )

    performance_score: float = Field(
        description="Mức độ nổi bật của lượt xem so với các video khác trên cùng kênh."
    )

    comments_insight: str | None = Field(
        default=None,
        description="Insight thu được từ bình luận của khán giả."
    )

    success_factors: list[str] = Field(
        default_factory=list,
        description="Các yếu tố có thể khiến video thành công: nội dung, thumbnail, tranh cãi, thương hiệu..."
    )

    content_angles: list[str] = Field(
        default_factory=list,
        description="Các góc nội dung đáng tham khảo từ video."
    )


class MarketVideoResearchResult(BaseModel):
    main_video: VideoResearchResult = Field(
        description="Video chính được chọn để phân tích sâu về cấu trúc, hook và văn phong."
    )

    supporting_videos: list[VideoResearchResult] = Field(
        default_factory=list,
        max_length=3,
        description="2-3 video phụ dùng để bổ sung thông tin và các góc triển khai."
    )
