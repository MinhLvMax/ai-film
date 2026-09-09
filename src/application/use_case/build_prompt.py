from typing import Any
from pydantic import BaseModel

def _to_dict(value: Any) -> dict:
    """
    Normalize nested Pydantic model / dict về dict.
    Giúp function hoạt động được cả khi chars đến từ model_dump()
    hoặc vẫn còn chứa nested BaseModel.
    """
    if value is None:
        return {}

    if isinstance(value, BaseModel):
        return value.model_dump()

    if isinstance(value, dict):
        return value

    return {}


def _format_number(value: float) -> str:
    """
    28.0 -> "28"
    28.5 -> "28.5"
    """
    value = float(value)

    if value.is_integer():
        return str(int(value))

    return f"{value:g}"


def _format_range(
        value: dict | BaseModel | None,
        unit: str,
) -> str | None:
    """
    {
        "min": 25,
        "max": 28
    }
    ->
    "25-28 cm"
    """
    data = _to_dict(value)

    if not data:
        return None

    min_value = data.get("min")
    max_value = data.get("max")

    if min_value is None or max_value is None:
        return None

    min_text = _format_number(min_value)
    max_text = _format_number(max_value)

    if float(min_value) == float(max_value):
        return f"{min_text} {unit}"

    return f"{min_text}-{max_text} {unit}"


def _range_midpoint(
        value: dict | BaseModel | None,
) -> float | None:
    """
    Dùng midpoint chỉ cho việc tính relative scale.

    Ví dụ:
    25-28 cm -> 26.5 cm
    """
    data = _to_dict(value)

    if not data:
        return None

    min_value = data.get("min")
    max_value = data.get("max")

    if min_value is None or max_value is None:
        return None

    return (
        float(min_value)
        + float(max_value)
    ) / 2


def _build_absolute_size_text(
        size_profile: dict | BaseModel | None,
) -> str:
    """
    Tạo mô tả absolute real-world dimensions
    để đưa trực tiếp vào từng subject.

    Không dùng visual_extent_cm ở đây nếu nó chỉ lặp lại
    body length / leg span / wingspan.

    visual_extent_cm chủ yếu dùng nội bộ để tính relative scale.
    """
    size_profile = _to_dict(size_profile)

    if not size_profile:
        return ""

    parts = []

    body_length = _format_range(
        size_profile.get("body_length_cm"),
        "cm",
    )

    shoulder_height = _format_range(
        size_profile.get("shoulder_height_cm"),
        "cm",
    )

    standing_height = _format_range(
        size_profile.get("standing_height_cm"),
        "cm",
    )

    span = _format_range(
        size_profile.get("span_cm"),
        "cm",
    )

    mass = _format_range(
        size_profile.get("mass_kg"),
        "kg",
    )

    if body_length:
        parts.append(
            f"body length {body_length}"
        )

    if shoulder_height:
        parts.append(
            f"shoulder height {shoulder_height}"
        )

    if standing_height:
        parts.append(
            f"standing height {standing_height}"
        )

    if span:
        span_basis = (
                size_profile.get("visual_extent_basis")
                or ""
        )

        if span_basis == "leg_span":
            parts.append(
                f"leg span {span}"
            )

        elif span_basis == "wingspan":
            parts.append(
                f"wingspan {span}"
            )

        else:
            parts.append(
                f"span {span}"
            )

    if mass:
        parts.append(
            f"mass {mass}"
        )

    return "; ".join(parts)


def _collect_subject_scale_data(
        subject_ids: list[str],
        char_map: dict[str, dict],
) -> list[dict]:
    """
    Lấy primary visual extent của các subject thực sự xuất hiện
    trong shot.

    visual_extent_cm là measurement chuẩn hóa dùng để so sánh
    occupied physical scale giữa các loài.
    """
    subjects = []

    for subject_id in subject_ids:

        char = char_map.get(subject_id)

        if not char:
            continue

        size_profile = _to_dict(
            char.get("size_profile")
        )

        if not size_profile:
            continue

        visual_extent = _range_midpoint(
            size_profile.get("visual_extent_cm")
        )

        if visual_extent is None:
            continue

        name = (
                char.get("name")
                or subject_id
        ).strip()

        basis = (
                size_profile.get("visual_extent_basis")
                or "overall_extent"
        )

        subjects.append({
            "id": subject_id,
            "name": name,
            "visual_extent_cm": visual_extent,
            "basis": basis,
        })

    return subjects


def _build_relative_scale_text(
        subject_ids: list[str],
        char_map: dict[str, dict],
) -> str:
    """
    Tạo relative scale constraint chỉ từ các subject
    xuất hiện đồng thời trong shot.

    1 subject:
        chỉ khóa physical size consistency.

    2 subjects:
        tạo relationship trực tiếp A vs B.

    >2 subjects:
        dùng subject lớn nhất làm reference để tránh
        pairwise explosion làm prompt quá dài.
    """
    subjects = _collect_subject_scale_data(
        subject_ids=subject_ids,
        char_map=char_map,
    )

    if not subjects:
        return ""

    if len(subjects) == 1:
        subject = subjects[0]

        return (
            f"Scale consistency: Preserve the real-world physical size "
            f"and proportions of {subject['name']} throughout the shot. "
            f"Perspective may change apparent screen size, but the animal's "
            f"actual body dimensions must remain constant."
        )

    # -------------------------------------------------
    # Exactly 2 subjects
    # -------------------------------------------------
    if len(subjects) == 2:

        a, b = subjects

        if a["visual_extent_cm"] >= b["visual_extent_cm"]:
            larger = a
            smaller = b
        else:
            larger = b
            smaller = a

        ratio = (
            larger["visual_extent_cm"]
            / smaller["visual_extent_cm"]
        )

        return (
            f"Relative scale: Preserve their real-world size relationship. "
            f"{larger['name']} has approximately {ratio:.2f} times the "
            f"primary physical extent of {smaller['name']}. "
            f"Do not enlarge the smaller animal or shrink the larger animal "
            f"for dramatic composition. Perspective may alter apparent screen "
            f"size, but their underlying physical dimensions and anatomical "
            f"proportions must remain consistent throughout the shot."
        )

    # -------------------------------------------------
    # 3+ subjects
    # -------------------------------------------------
    subjects = sorted(
        subjects,
        key=lambda item: item["visual_extent_cm"],
        reverse=True,
    )

    reference = subjects[0]

    relationships = []

    for subject in subjects[1:]:

        ratio = (
            reference["visual_extent_cm"]
            / subject["visual_extent_cm"]
        )

        relationships.append(
            f"{reference['name']} is approximately "
            f"{ratio:.2f} times the primary physical extent "
            f"of {subject['name']}"
        )

    relationship_text = "; ".join(
        relationships
    )

    return (
        f"Relative scale: Preserve real-world size relationships between "
        f"all visible subjects: {relationship_text}. "
        f"Do not resize any subject for dramatic composition. "
        f"Perspective may alter apparent screen size, but underlying physical "
        f"dimensions and anatomical proportions must remain consistent "
        f"throughout the shot."
    )


async def build_prompt_from_chars_and_shots(
        style_lock: str,
        chars: list[dict],
        shots: list[dict],
):
    """
    Build Veo prompts using the structured plain-text format:

    CINEMATOGRAPHY
    SUBJECTS
    ACTION
    CONTEXT
    STYLE & AMBIANCE
    AUDIO
    NEGATIVE PROMPT

    SUBJECTS is omitted automatically when the shot contains
    no visible subjects.

    Absolute scale comes from each subject's size_profile.

    Relative scale is calculated dynamically only between
    subjects actually visible together in the current shot.
    """

    # -------------------------------------------------
    # Character lookup
    # -------------------------------------------------
    char_map = {
        char["id"]: char
        for char in chars
        if char.get("id")
    }

    results = []

    for shot in shots:

        # -------------------------------------------------
        # Normalize subject_ids
        # -------------------------------------------------
        raw_subject_ids = (
                shot.get("subject_ids")
                or []
        )

        if isinstance(raw_subject_ids, str):
            subject_ids = [
                subject_id.strip()
                for subject_id
                in raw_subject_ids.split(",")
                if subject_id.strip()
            ]
        else:
            subject_ids = [
                str(subject_id).strip()
                for subject_id in raw_subject_ids
                if str(subject_id).strip()
            ]

        # -------------------------------------------------
        # Build SUBJECTS
        # -------------------------------------------------
        subject_blocks = []

        for index, subject_id in enumerate(
                subject_ids,
                start=1,
        ):

            char = char_map.get(subject_id)

            # ---------------------------------------------
            # Unknown subject fallback
            # ---------------------------------------------
            if not char:
                subject_blocks.append(
                    "\n".join([
                        f"{index}. {subject_id}",
                        f"ID: {subject_id}",
                    ])
                )
                continue

            name = (
                    char.get("name")
                    or subject_id
            ).strip()

            description = (
                    char.get("description")
                    or ""
            ).strip()

            motion_profile = (
                    char.get("motion_profile")
                    or ""
            ).strip()

            behavior_profile = (
                    char.get("behavior_profile")
                    or ""
            ).strip()

            size_profile = _to_dict(
                char.get("size_profile")
            )

            absolute_size = (
                _build_absolute_size_text(
                    size_profile
                )
            )

            scale_notes = (
                    size_profile.get("scale_notes")
                    or ""
            ).strip()

            parts = [
                f"{index}. {name}",
                f"ID: {subject_id}",
            ]

            if description:
                parts.append(
                    f"Appearance: {description}"
                )

            # ---------------------------------------------
            # Absolute real-world scale
            # ---------------------------------------------
            if absolute_size:
                parts.append(
                    f"Real-world size: {absolute_size}"
                )

            if scale_notes:
                parts.append(
                    f"Scale reference: {scale_notes}"
                )

            # ---------------------------------------------
            # Motion / behavior
            # ---------------------------------------------
            if motion_profile:
                parts.append(
                    f"Motion reference: {motion_profile}"
                )

            if behavior_profile:
                parts.append(
                    f"Behavior reference: {behavior_profile}"
                )

            subject_blocks.append(
                "\n".join(parts)
            )

        # -------------------------------------------------
        # Dynamic relative scale
        # -------------------------------------------------
        relative_scale_text = (
            _build_relative_scale_text(
                subject_ids=subject_ids,
                char_map=char_map,
            )
        )

        if relative_scale_text:
            subject_blocks.append(
                relative_scale_text
            )

        subjects_text = "\n\n".join(
            subject_blocks
        )

        # -------------------------------------------------
        # CINEMATOGRAPHY
        # -------------------------------------------------
        cinematography = (
                shot.get("cinematography")
                or ""
        ).strip()

        # -------------------------------------------------
        # ACTION
        # -------------------------------------------------
        raw_action_timeline = (
                shot.get("action_timeline")
                or []
        )

        if isinstance(
                raw_action_timeline,
                str,
        ):
            action_timeline = (
                [raw_action_timeline.strip()]
                if raw_action_timeline.strip()
                else []
            )
        else:
            action_timeline = [
                str(action).strip()
                for action
                in raw_action_timeline
                if str(action).strip()
            ]

        action_text = "\n".join(
            f"{index}. {action}"
            for index, action
            in enumerate(
                action_timeline,
                start=1,
            )
        )

        # -------------------------------------------------
        # CONTEXT
        # -------------------------------------------------
        context = (
                shot.get("context")
                or ""
        ).strip()

        # -------------------------------------------------
        # AUDIO
        # -------------------------------------------------
        audio = (
                shot.get("audio")
                or ""
        ).strip()

        # -------------------------------------------------
        # NEGATIVE PROMPT
        # -------------------------------------------------
        raw_negative_prompt = (
                shot.get("negative_prompt")
                or []
        )

        if isinstance(
                raw_negative_prompt,
                str,
        ):
            negative_prompt = [
                item.strip()
                for item
                in raw_negative_prompt.split(",")
                if item.strip()
            ]
        else:
            negative_prompt = [
                str(item).strip()
                for item
                in raw_negative_prompt
                if str(item).strip()
            ]

        negative_prompt_text = ", ".join(
            negative_prompt
        )

        # -------------------------------------------------
        # Build final sections
        # -------------------------------------------------
        prompt_sections = []

        if cinematography:
            prompt_sections.append(
                "\n".join([
                    "CINEMATOGRAPHY:",
                    cinematography,
                ])
            )

        if subjects_text:
            prompt_sections.append(
                "\n".join([
                    "SUBJECTS:",
                    subjects_text,
                ])
            )

        if action_text:
            prompt_sections.append(
                "\n".join([
                    "ACTION:",
                    action_text,
                ])
            )

        if context:
            prompt_sections.append(
                "\n".join([
                    "CONTEXT:",
                    context,
                ])
            )

        if style_lock.strip():
            prompt_sections.append(
                "\n".join([
                    "STYLE & AMBIANCE:",
                    style_lock.strip(),
                ])
            )

        if audio:
            prompt_sections.append(
                "\n".join([
                    "AUDIO:",
                    audio,
                ])
            )

        if negative_prompt_text:
            prompt_sections.append(
                "\n".join([
                    "NEGATIVE PROMPT:",
                    negative_prompt_text,
                ])
            )

        # -------------------------------------------------
        # Final Veo prompt
        # -------------------------------------------------
        prompt = "\n\n".join(
            prompt_sections
        )

        results.append({
            "prompt": prompt,
            "is_sent": False,
        })

    return results

# ======

# async def build_prompt_from_chars_and_shots(
#         style_lock: str,
#         chars: list[dict],
#         shots: list[dict],
# ):
#     """
#     Build Veo prompts using a structured plain-text format:
#
#     CINEMATOGRAPHY
#     SUBJECTS
#     ACTION
#     CONTEXT
#     STYLE & AMBIANCE
#     AUDIO
#     NEGATIVE PROMPT
#     """
#
#     char_map = {
#         char["id"]: char
#         for char in chars
#     }
#
#     results = []
#
#     for shot in shots:
#
#         # -------------------------------------------------
#         # Normalize subject_ids
#         # -------------------------------------------------
#         raw_subject_ids = shot.get("subject_ids", [])
#
#         if isinstance(raw_subject_ids, str):
#             subject_ids = [
#                 subject_id.strip()
#                 for subject_id in raw_subject_ids.split(",")
#                 if subject_id.strip()
#             ]
#         else:
#             subject_ids = raw_subject_ids or []
#
#         # -------------------------------------------------
#         # Build SUBJECTS section
#         # -------------------------------------------------
#         subject_blocks = []
#
#         for index, subject_id in enumerate(subject_ids, start=1):
#
#             char = char_map.get(subject_id)
#
#             if not char:
#                 subject_blocks.append(
#                     "\n".join([
#                         f"{index}. {subject_id}",
#                         f"ID: {subject_id}",
#                     ])
#                 )
#                 continue
#
#             name = (
#                     char.get("name")
#                     or subject_id
#             ).strip()
#
#             description = (
#                     char.get("description")
#                     or ""
#             ).strip()
#
#             motion_profile = (
#                     char.get("motion_profile")
#                     or ""
#             ).strip()
#
#             behavior_profile = (
#                     char.get("behavior_profile")
#                     or ""
#             ).strip()
#
#             parts = [
#                 f"{index}. {name}",
#                 f"ID: {subject_id}",
#             ]
#
#             if description:
#                 parts.append(
#                     f"Appearance: {description}"
#                 )
#
#             if motion_profile:
#                 parts.append(
#                     f"Motion reference: {motion_profile}"
#                 )
#
#             if behavior_profile:
#                 parts.append(
#                     f"Behavior reference: {behavior_profile}"
#                 )
#
#             subject_blocks.append(
#                 "\n".join(parts)
#             )
#
#         subjects_text = "\n\n".join(subject_blocks)
#
#         # -------------------------------------------------
#         # CINEMATOGRAPHY
#         # -------------------------------------------------
#         cinematography = (
#                 shot.get("cinematography")
#                 or ""
#         ).strip()
#
#         # -------------------------------------------------
#         # ACTION
#         # -------------------------------------------------
#         raw_action_timeline = (
#                 shot.get("action_timeline")
#                 or []
#         )
#
#         if isinstance(raw_action_timeline, str):
#             action_timeline = [
#                 raw_action_timeline.strip()
#             ] if raw_action_timeline.strip() else []
#         else:
#             action_timeline = [
#                 str(action).strip()
#                 for action in raw_action_timeline
#                 if str(action).strip()
#             ]
#
#         action_text = "\n".join(
#             f"{index}. {action}"
#             for index, action in enumerate(
#                 action_timeline,
#                 start=1,
#             )
#         )
#
#         # -------------------------------------------------
#         # CONTEXT
#         # -------------------------------------------------
#         context = (
#                 shot.get("context")
#                 or ""
#         ).strip()
#
#         # -------------------------------------------------
#         # AUDIO
#         # -------------------------------------------------
#         audio = (
#                 shot.get("audio")
#                 or ""
#         ).strip()
#
#         # -------------------------------------------------
#         # NEGATIVE PROMPT
#         # -------------------------------------------------
#         raw_negative_prompt = (
#                 shot.get("negative_prompt")
#                 or []
#         )
#
#         if isinstance(raw_negative_prompt, str):
#             negative_prompt = [
#                 item.strip()
#                 for item in raw_negative_prompt.split(",")
#                 if item.strip()
#             ]
#         else:
#             negative_prompt = [
#                 str(item).strip()
#                 for item in raw_negative_prompt
#                 if str(item).strip()
#             ]
#
#         negative_prompt_text = ", ".join(
#             negative_prompt
#         )
#
#         # -------------------------------------------------
#         # Build sections
#         # -------------------------------------------------
#         prompt_sections = []
#
#         if cinematography:
#             prompt_sections.append(
#                 "\n".join([
#                     "CINEMATOGRAPHY:",
#                     cinematography,
#                 ])
#             )
#
#         if subjects_text:
#             prompt_sections.append(
#                 "\n".join([
#                     "SUBJECTS:",
#                     subjects_text,
#                 ])
#             )
#
#         if action_text:
#             prompt_sections.append(
#                 "\n".join([
#                     "ACTION:",
#                     action_text,
#                 ])
#             )
#
#         if context:
#             prompt_sections.append(
#                 "\n".join([
#                     "CONTEXT:",
#                     context,
#                 ])
#             )
#
#         if style_lock.strip():
#             prompt_sections.append(
#                 "\n".join([
#                     "STYLE & AMBIANCE:",
#                     style_lock.strip(),
#                 ])
#             )
#
#         if audio:
#             prompt_sections.append(
#                 "\n".join([
#                     "AUDIO:",
#                     audio,
#                 ])
#             )
#
#         if negative_prompt_text:
#             prompt_sections.append(
#                 "\n".join([
#                     "NEGATIVE PROMPT:",
#                     negative_prompt_text,
#                 ])
#             )
#
#         # -------------------------------------------------
#         # Final Veo prompt
#         # -------------------------------------------------
#         prompt = "\n\n".join(
#             prompt_sections
#         )
#
#         results.append({
#             "prompt": prompt,
#             "is_sent": False,
#         })
#
#     return results