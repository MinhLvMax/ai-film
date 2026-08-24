from pydantic import BaseModel, Field


# class ImagePrompt(BaseModel):
#     subjects: list[str] = Field(
#         ...,
#         description=(
#             "All important subjects visible in the image. "
#             "Each item should describe one subject, including its identity, "
#             "important physical characteristics, appearance, and distinctive features."
#         )
#     )
#
#     pose: str = Field(
#         ...,
#         description=(
#             "The visible poses, postures, physical states, or momentary actions "
#             "of all important subjects captured at this specific moment."
#         )
#     )
#
#     environment: str = Field(
#         ...,
#         description=(
#             "The physical environment surrounding the subjects, including location, "
#             "terrain, vegetation, weather, background elements, and relevant spatial context."
#         )
#     )
#
#     composition: str = Field(
#         ...,
#         description=(
#             "The visual arrangement of subjects and environmental elements within the frame, "
#             "including foreground, midground, background, subject placement, "
#             "relative positions, and visual balance."
#         )
#     )
#
#     camera: str = Field(
#         ...,
#         description=(
#             "The camera setup used to capture the image, including shot size, camera angle, "
#             "camera position, lens characteristics, depth of field, focus, and perspective."
#         )
#     )
#
#     lighting: str = Field(
#         ...,
#         description=(
#             "The lighting conditions of the shot, including light source, direction, intensity, "
#             "color temperature, contrast, shadows, and time-of-day characteristics."
#         )
#     )
#
#     style: str = Field(
#         ...,
#         description=(
#             "The intended visual style and rendering characteristics, such as documentary realism, "
#             "photographic realism, cinematic treatment, texture, detail level, "
#             "and color treatment."
#         )
#     )
#
#     continuity: str = Field(
#         ...,
#         description=(
#             "Visual elements that must remain consistent with related shots or the parent scene, "
#             "such as subject appearance, environment, geography, lighting, weather, "
#             "scale, spatial relationships, and props."
#         )
#     )
#
#     constraints: list[str] = Field(
#         default_factory=list,
#         description=(
#             "Explicit visual restrictions or undesirable elements that should be avoided "
#             "when generating the image."
#         )
#     )
#
#
# class VideoPrompt(BaseModel):
#     action: str = Field(
#         ...,
#         description=(
#             "The main event that unfolds from the provided starting image, "
#             "including interactions between subjects when relevant."
#         )
#     )
#
#     subject_motion: str = Field(
#         ...,
#         description=(
#             "How the visible subjects move from their positions and poses "
#             "in the provided starting image, including direction, speed, "
#             "body mechanics, gestures, and relative movement between subjects."
#         )
#     )
#
#     environment_motion: str = Field(
#         ...,
#         description=(
#             "Natural or background movement within the environment, such as water, "
#             "foliage, clouds, rain, dust, smoke, atmospheric effects, "
#             "or distant background activity."
#         )
#     )
#
#     camera_motion: str = Field(
#         ...,
#         description=(
#             "How the camera moves from the framing established by the provided "
#             "starting image, including direction, speed, and movement type."
#         )
#     )
#
#     pacing: str = Field(
#         ...,
#         description=(
#             "The temporal rhythm of the shot, describing how quickly or gradually "
#             "the subject action, environmental movement, and camera movement develop."
#         )
#     )
#
#     end_state: str = Field(
#         ...,
#         description=(
#             "The desired physical and spatial state of the subjects and relevant "
#             "scene elements at the end of the shot."
#         )
#     )
#
#     continuity: str = Field(
#         ...,
#         description=(
#             "Visual, spatial, and identity-related elements from the starting image "
#             "that must remain stable throughout the generated video."
#         )
#     )
#
#     constraints: list[str] = Field(
#         default_factory=list,
#         description=(
#             "Motion, continuity, or generation errors that must be avoided, "
#             "such as morphing, anatomical deformation, duplicated subjects, "
#             "unnatural movement, unwanted cuts, camera shake, or lighting flicker."
#         )
#     )


class PairPrompt(BaseModel):
    '''Cặp prompt ảnh-video'''
    """Cặp prompt ảnh-video"""

    image_prompt: str = Field(
        ...,
        description=(
            "The image-generation prompt used to create the starting frame "
            "or visual keyframe for the shot."
        )
    )

    video_prompt: str = Field(
        ...,
        description=(
            "The image-to-video prompt used to animate the generated starting image "
            "into the final video shot."
        )
    )
