from pydantic import BaseModel, Field
from src.domain.schemas.camera import Camera
from src.domain.schemas.subject import SubjectLLMResult

class ShotLLMResult(BaseModel):
    """Structured shot data used to build a Veo video-generation prompt."""

    subject_ids: list[str] = Field(
        description=(
            "IDs of all subjects directly visible in the shot. "
            "Include only subjects that physically appear on screen."
        )
    )

    cinematography: str = Field(
        description=(
            "One physically achievable camera setup for the entire shot. "
            "Describe shot size, camera angle, camera position, camera movement or static behavior, "
            "lens or focus behavior when relevant, and composition. "
            "State what spatial relationship or action must remain clearly readable in frame. "
            "Use one coherent camera setup rather than multiple cuts or conflicting camera moves. "
            "Do not describe subject appearance, environment details, or the action sequence here."
        )
    )

    action_timeline: list[str] = Field(
        min_length=1,
        description=(
            "Ordered observable action phases for one continuous video shot. "
            "Each item must describe what visibly happens next in chronological order. "
            "Begin with the initial physical state when it is important to the action. "
            "Describe posture, orientation, direction of travel, speed, acceleration, reaction, "
            "relative position, distance changes, physical contact, and environmental interaction "
            "when relevant. "
            "For predator-prey scenes, explicitly preserve predator and prey roles and state "
            "who approaches, flees, pursues, strikes, makes contact, or reacts, and in what order. "
            "Use positive, direct descriptions of the desired motion. "
            "Do not describe camera, visual style, or general environment here. "
            "Keep the sequence physically achievable within one continuous shot."
        )
    )

    context: str = Field(
        description=(
            "The visible physical context surrounding the action. "
            "Describe location, terrain, vegetation, water, mud, roots, branches, weather, "
            "lighting conditions, obstacles, surface conditions, and other environmental elements "
            "that materially affect the shot. "
            "Keep it specific to what is visible and relevant. "
            "Do not repeat subject appearance, camera instructions, or the action timeline."
        )
    )

    audio: str = Field(
        default="",
        description=(
            "Natural audible elements appropriate to the shot, such as animal vocalizations, "
            "water movement, wind, insects, birds, foliage movement, impacts, or other environmental sounds. "
            "Leave empty when audio control is unnecessary. "
            "Do not describe music unless the shot explicitly requires it."
        )
    )

    negative_prompt: list[str] = Field(
        default_factory=list,
        description=(
            "Concise unwanted visual or motion outcomes that would cause the shot to fail. "
            "Write each item as a short descriptive phrase, not as an instruction. "
            "Prefer forms such as 'side-by-side predator and prey', 'high-speed swimming', "
            "'camera tracking', 'exposed torso above water', or 'CGI appearance'. "
            "Avoid wording such as 'do not', 'don't', 'never', or long explanatory sentences. "
            "Include only shot-specific failure modes; generic visual-style exclusions should stay "
            "in the shared style lock."
        )
    )


class ListShotLLMResult(BaseModel):
    '''Class này chỉ để làm cái cho llm trả về thôi'''
    shots: list[ShotLLMResult]


class Shot(ShotLLMResult):
    '''Class này là để khi lưu json'''
    shot_id: str
    # subjects: list[SubjectLLMResult]
    section: str  # Chứa tên của section để biết nó nằm trong section nào
