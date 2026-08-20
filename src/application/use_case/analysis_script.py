import re
import uuid
import unicodedata
from src.application.ports.llm_port import LLM
from src.domain.schemas.subject import ListSubjectLLMResult, Subject
from src.domain.schemas.shot import ListShotLLMResult, Shot


class AnalysisScript:
    def __init__(self, llm: LLM):
        self.llm = llm

    def extract_chars(self, prompt, model, content):
        prompt = (
            f'{prompt}\n'
            '[Content to be extracted]\n'
            f'{content}\n'
        )
        complete_result = self.llm.complete(messages=prompt, response_model=ListSubjectLLMResult, llm_model=model)
        chars_lln_res: ListSubjectLLMResult = complete_result.response_model
        subjects = [
            Subject(
                id=self._normalize(char.name),
                **char.model_dump(),
            ).model_dump()
            for char in chars_lln_res.list_subjects
        ]
        return subjects

    def extract_shots_for_section(self, prompt, model, section, title, chars):
        prompt = (
            f'{prompt}\n'
            '[Content to be extracted]\n'
            f'{section}\n'
        )
        complete_result = self.llm.complete(messages=prompt, response_model=ListShotLLMResult, llm_model=model)
        list_shots_llm_res: ListShotLLMResult = complete_result.response_model
        shots = [
            Shot(
                shot_id=str(uuid.uuid4()),
                subjects=[
                    next(
                        (char for char in chars if char["id"] == subject_id),
                        None
                    )
                    for subject_id in shot.subject_ids
                ],
                **shot.model_dump(),
            ).model_dump()
            for shot in list_shots_llm_res.shots
        ]
        return {
            'section': title,
            'shots': shots,
        }

    def _sreenplay_chunking(self, content):
        '''
        Chia kịch bản ra thành các đoạn
        :return: [{
                "title": tiêu đề đoạn,
                "content": nội dung đoạn,
            }, ...]
        '''
        pattern = re.compile(
            r'(?m)^[A-ZÁÉÍÓÚÜÑ0-9][A-ZÁÉÍÓÚÜÑ0-9\s:,\-–—\'".!?()&]+$'
        )

        matches = list(pattern.finditer(content))

        chunks = []

        # Content trước section đầu tiên
        if matches and content[:matches[0].start()].strip():
            chunks.append({
                "title": None,
                "content": content[:matches[0].start()].strip(),
            })

        for i, match in enumerate(matches):
            title = match.group().strip()

            start = match.end()
            end = (
                matches[i + 1].start()
                if i + 1 < len(matches)
                else len(content)
            )

            chunks.append({
                "title": title,
                "content": content[start:end].strip(),
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
