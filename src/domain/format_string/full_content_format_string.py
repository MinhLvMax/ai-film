class FullContent(str):
    def __new__(
            cls,
            title,
            content,
    ):
        text = (
            f"**TIÊU ĐỀ**: {title}\n"
            f"{content}"
        )
        return super().__new__(cls, text)


if __name__ == "__main__":
    full_content = FullContent(
        title="Python",
        content="""
# Chương 1: Giới thiệu Python

Python là một ngôn ngữ lập trình bậc cao...
""",
    )

    # Vì FullContent kế thừa str
    print(full_content)

    print("-" * 50)
    print(type(full_content))
    print(isinstance(full_content, str))
    print(len(full_content))

    print("-" * 50)
    print(full_content.upper()[:100])

    print("-" * 50)
    print(full_content.replace('Python', 'Java', 1))
