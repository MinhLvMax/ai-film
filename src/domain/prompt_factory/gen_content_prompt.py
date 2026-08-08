class GenContentPrompt(str):
    def __new__(cls, keyword, description):
        text = (
            f"Bạn là một chuyên gia xây dựng nội dung video du lịch. "
            f"Hãy tạo một kịch bản và cấu trúc nội dung hấp dẫn cho video về địa điểm dưới đây.\n\n"
            f"ĐỊA ĐIỂM/CHỦ ĐỀ: {keyword}\n"
            f"MÔ TẢ: {description}\n\n"
            f"Yêu cầu:\n"
            f"- Xây dựng nội dung phù hợp cho video du lịch.\n"
            f"- Có phần mở đầu thu hút người xem (hook).\n"
            f"- Mô tả cảnh quay, trải nghiệm, văn hóa, ẩm thực và điểm nổi bật.\n"
            f"- Đề xuất trình tự các cảnh quay hợp lý.\n"
            f"- Tạo cảm xúc và khuyến khích người xem muốn khám phá địa điểm này.\n"
            f"- Trình bày rõ ràng theo từng phân đoạn video."
        )
        return super().__new__(cls, text)


if __name__ == "__main__":
    pass
