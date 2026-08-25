async def build_prompt_from_chars_and_shots(style_lock: str, chars: dict, shots: dict):
    '''
    Tạo bộ prompt từ dữ liệu nhân vật và cảnh
    :param prompt: Prompt chung để ra lệnh tạo bộ prompt cho từng phân đoạn
    :param segment_content: nội dung phân đoạn truyền kèm vào
    :param chars: danh sách nhân vật có trong bài
    :param shots: danh sách các shot có trong bài
    :return: list các cặp prompt ảnh - video
    '''

    char_map = {
        char["id"]: char
        for char in chars
    }

    results = []

    for shot in shots:
        subjects = []

        # # 4 dòng in debug
        # print("SHOT:", shot)
        # print("subject_ids:", shot.get("subject_ids"))
        # print("type:", type(shot.get("subject_ids")))
        # print()

        for subject_id in shot["subject_ids"]:
            char = char_map.get(subject_id)

            if char:
                subjects.append(
                    f"{char['name']}: {char['description']}"
                )
            else:
                subjects.append(subject_id)

        subjects_text = "\n".join(
            f"- {subject}"
            for subject in subjects
        )

        prompt = (
            f"<subjects>\n"
            f"{subjects_text}\n"
            f"</subjects>\n\n"

            f"<action>\n"
            f"{shot['action']}\n"
            f"</action>\n\n"

            f"<environment>\n"
            f"{shot['environment']}\n"
            f"</environment>\n\n"

            f"<camera>\n"
            f"{shot['camera']}\n"
            f"</camera>\n\n"

            f"<style>\n"
            f"{style_lock}\n"
            f"</style>"
        )

        results.append({
            "shot_id": shot["shot_id"],
            "section": shot["section"],
            "prompt": prompt,
            'is_sent': False,
        })

    return results
