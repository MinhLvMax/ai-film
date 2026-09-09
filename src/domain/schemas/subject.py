from pydantic import BaseModel, Field
from typing import Literal


class SizeRange(BaseModel):
    min: float = Field(
        gt=0,
        description="Giá trị nhỏ hợp lý của cá thể trưởng thành."
    )
    max: float = Field(
        gt=0,
        description="Giá trị lớn hợp lý của cá thể trưởng thành."
    )


class SubjectSizeProfile(BaseModel):
    body_length_cm: SizeRange | None = Field(
        default=None,
        description=(
            "Chiều dài cơ thể thực tế của cá thể trưởng thành, tính bằng cm. "
            "Không tính đuôi nếu nguồn khoa học thường tách riêng đuôi."
        )
    )

    shoulder_height_cm: SizeRange | None = Field(
        default=None,
        description=(
            "Chiều cao vai của động vật bốn chân trưởng thành, tính bằng cm. "
            "Để None nếu không áp dụng."
        )
    )

    standing_height_cm: SizeRange | None = Field(
        default=None,
        description=(
            "Chiều cao tổng thể khi ở tư thế tự nhiên, tính bằng cm. "
            "Dùng khi shoulder height không phù hợp."
        )
    )

    span_cm: SizeRange | None = Field(
        default=None,
        description=(
            "Sải cánh, sải chân hoặc span quan trọng về mặt thị giác, tính bằng cm. "
            "Ví dụ wingspan của chim hoặc leg span của tarantula."
        )
    )

    mass_kg: SizeRange | None = Field(
        default=None,
        description="Khối lượng trưởng thành điển hình, tính bằng kg."
    )

    visual_extent_cm: SizeRange = Field(
        description=(
            "Kích thước tuyến tính quan trọng nhất để so sánh tỷ lệ thị giác với "
            "các subject khác trong cùng shot. Đây là approximate occupied visual extent, "
            "không nhất thiết cùng một measurement anatomical cho mọi loài. "
            "Ví dụ jaguar có thể dùng body length, tarantula có thể dùng leg span. "
            "Field này bắt buộc để hệ thống tính relative scale."
        )
    )

    visual_extent_basis: Literal[
        "body_length",
        "shoulder_height",
        "standing_height",
        "leg_span",
        "wingspan",
        "overall_extent",
    ] = Field(
        description=(
            "Measurement thực tế nào được dùng làm visual_extent_cm."
        )
    )

    scale_notes: str = Field(
        default="",
        description=(
            "Các constraint ổn định giúp tránh scale hallucination. "
            "Ví dụ: compact medium-large cat, not tiger-sized; "
            "large spider but still much smaller than a mammal. "
            "Không mô tả scene cụ thể."
        )
    )


class SubjectLLMResult(BaseModel):
    name: str = Field(
        description=(
            "Tên ngắn gọn và ổn định của chủ thể bằng tiếng Anh."
        )
    )
    description: str = Field(
        description=(
            "Canonical visual identity dùng để tham chiếu ngoại hình của chủ thể "
            "trong mọi shot. Chỉ mô tả các đặc điểm ngoại hình ổn định và nhìn thấy được: "
            "body shape, proportions, anatomy, coloration, markings, fur, scales, "
            "limbs, fins, tail, head shape và các đặc điểm nhận dạng quan trọng. "
            "Không chứa hành vi, chuyển động, môi trường, camera, citation hoặc URL."
        )
    )

    size_profile: SubjectSizeProfile = Field(
        description=(
            "Kích thước vật lý thực tế của subject trưởng thành. "
            "Phải dựa trên số đo ngoài đời và được dùng để khóa absolute scale "
            "cũng như tính relative scale giữa các subject trong cùng shot. "
            "Không được phóng đại kích thước vì mục đích cinematic."
        )
    )

    motion_profile: str = Field(
        description=(
            "Các kiểu vận động tự nhiên và biomechanically correct của chủ thể "
            "có ích cho video generation, ví dụ walking, running, swimming, crawling, "
            "slithering hoặc flying. Mô tả cách cơ thể thực sự tạo chuyển động, "
            "không mô tả một scene cụ thể. Không chứa citation hoặc URL."
        )
    )

    behavior_profile: str = Field(
        description=(
            "Các khuynh hướng hành vi ổn định và species-typical có ích cho việc dựng "
            "interaction thực tế: mức độ cảnh giác, cách tiếp cận prey hoặc threat, "
            "khoảng cách an toàn, phản ứng khi bị đe dọa, cách tấn công, né tránh, "
            "rút lui hoặc phòng thủ. Không nhân cách hóa động vật, không mô tả cảm xúc "
            "kiểu con người, không mô tả một scene cụ thể. Không chứa citation hoặc URL."
        )
    )

    sources: list[str] = Field(
        default_factory=list,
        description=(
            "Danh sách nguồn dùng để xác minh ngoại hình, locomotion hoặc behavior. "
            "URL và citation chỉ được đặt trong field này."
        )
    )


class ListSubjectLLMResult(BaseModel):
    '''Class này chỉ để làm cái cho llm trả về thôi'''
    list_subjects: list[SubjectLLMResult] = Field(
        description="Danh sách tất cả nhân vật hoặc đối tượng quan trọng xuất hiện trong nội dung."
    )


class Subject(SubjectLLMResult):
    id: str
