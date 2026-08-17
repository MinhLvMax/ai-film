from pathlib import Path

# Chạy để tạo trước các file json chứa prompt, tôi lên chatgpt tạo prompt dán vào

def create_empty_files(
    prefix: str,
    count: int,
    data_folder: Path | str = ".",
    exist_ok: bool = False,
) -> list[Path]:
    project_folder = Path(data_folder) / prefix
    project_folder.mkdir(parents=True, exist_ok=True)

    created = []

    for i in range(count):
        file_path = project_folder / f"{prefix} phân đoạn {i:02d}.json"

        if file_path.exists() and not exist_ok:
            continue

        file_path.touch(exist_ok=True)
        created.append(file_path)

    return created


if __name__ == '__main__':
    project_name = 'Minh bài 17'
    chapter_total = 31

    create_empty_files(prefix=project_name, count=chapter_total)
