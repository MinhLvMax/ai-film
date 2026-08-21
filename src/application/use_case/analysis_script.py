import re
import uuid
import unicodedata
from src.application.ports.llm_port import LLM
from src.domain.schemas.subject import ListSubjectLLMResult, Subject
from src.domain.schemas.shot import ListShotLLMResult, Shot
from src.infrastructure import llm


class AnalysisScript:
    def __init__(self, llm: LLM):
        self.llm = llm

    async def extract_chars(self, prompt, model, content):
        prompt = (
            f"{prompt}\n"
            "<content>\n"
            f"{content}\n"
            "</content>\n"
        )
        complete_result = await self.llm.complete(messages=prompt, response_model=ListSubjectLLMResult, llm_model=model)
        chars_lln_res: ListSubjectLLMResult = complete_result.response_model
        subjects = [
            Subject(
                id=self._normalize(char.name),
                **char.model_dump(),
            ).model_dump()
            for char in chars_lln_res.list_subjects
        ]
        return subjects

    async def extract_shots(self, prompt, model, content, chars):
        sections = self._sreenplay_chunking(content)
        results = []
        for section in sections:
            shots_for_section = await self.extract_shots_for_section(
                prompt=prompt,
                model=model,
                section=section['content'],
                title=section['title'],
                chars=chars,
            )
            results.extend(shots_for_section)
            yield shots_for_section

    async def extract_shots_for_section(self, prompt, model, section, title, chars):
        chars_ids = [char["id"] for char in chars]
        prompt = (
            f"{prompt}\n\n"
            "<content>\n"
            f"{section}\n"
            "</content>\n\n"
            "<character_ids>\n"
            f"{', '.join(chars_ids)}\n"
            "</character_ids>"
        )
        complete_result = await self.llm.complete(messages=prompt, response_model=ListShotLLMResult, llm_model=model)
        list_shots_llm_res: ListShotLLMResult = complete_result.response_model
        shots = [
            Shot(
                shot_id=str(uuid.uuid4()),
                # subjects=[
                #     next(
                #         (char for char in chars if char["id"] == subject_id),
                #         None
                #     )
                #     for subject_id in shot.subject_ids
                # ],
                section=title,
                **shot.model_dump(),
            ).model_dump()
            for shot in list_shots_llm_res.shots
        ]
        return shots

    def _sreenplay_chunking(self, content):
        '''
        Chia kịch bản ra thành các đoạn
        :return: [{
                "title": tiêu đề đoạn,
                "content": nội dung đoạn,
            }, ...]
        '''
        # Chuẩn hóa line ending Windows / Linux
        content = content.replace("\r\n", "\n").replace("\r", "\n").strip()

        # Tách section tại ít nhất một dòng trống
        sections = re.split(r"\n\s*\n+", content)

        chunks = []

        for section in sections:
            section = section.strip()

            if not section:
                continue

            lines = section.splitlines()

            title = lines[0].strip()
            body = "\n".join(lines[1:]).strip()

            chunks.append({
                "title": title,
                "content": body,
            })

        return chunks

    def _normalize(self, text: str) -> str:
        text = unicodedata.normalize("NFD", text)

        text = "".join(
            c for c in text
            if unicodedata.category(c) != "Mn"
        )

        text = text.lower()

        return re.sub(r"\s+", "_", text).strip("_")
