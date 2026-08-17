import json
from pathlib import Path

class JsonWriter:
    def write(self, path: Path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )