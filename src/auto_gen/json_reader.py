import json
from pathlib import Path

class JsonReader:
    def read(self, path: Path):
        if path.stat().st_size == 0:
            print(f'{path} File is empty')
            return None
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

if __name__ == '__main__':
    jsonreader = JsonReader()
    data = jsonreader.read(Path('input/input.json'))
    print(data)