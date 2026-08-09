from src.application.ports.file_reader_port import FileReaderPort

class TextReader(FileReaderPort):
    def read(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            noi_dung = f.read()
            return noi_dung