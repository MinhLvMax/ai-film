from pprint import pprint
import re
from src.application.dto.gencontentdto import GenContentDTO
from src.infrastructure.file_services.text_reader import TextReader
from src.infrastructure.file_services.text_writer import TextWriter
from src.bootstrap import build_gen_content
from src.config import Config


def main():
    text_reader = TextReader()
    text_writer = TextWriter()
    gen_content = build_gen_content()

    paths_map = {
        'system': Config.PROMPTS / 'system_prompt.txt',
        'toc': Config.PROMPTS / 'gentoc_prompt.txt',
        'chap': Config.PROMPTS / 'genchap_prompt.txt',
        'title': Config.INPUT / 'title.txt',
        'chapter_count': Config.INPUT / 'chapter_count.txt',
        'chapter_length': Config.INPUT / 'chapter_length.txt',
        'output': Config.OUTPUT,
    }

    genDTO = GenContentDTO(
        title=text_reader.read(paths_map['title']),
        system_prompt=text_reader.read(paths_map['system']),
        gen_toc_prompt=text_reader.read(paths_map['toc']),
        gen_chapter_prompt=text_reader.read(paths_map['chap']),
        chapter_length=text_reader.read(paths_map['chapter_length']),
        chapter_count=text_reader.read(paths_map['chapter_count']),
        sleep_time=30,
    )

    pprint(genDTO.__dict__)

    output = gen_content.gen(genDTO)

    print(f'- {output.title=}')
    pprint(f'- {output.toc}=')
    pprint(f'- {output.chaps}=')

    full_content = (
        f'Title: {output.title}\n'
        f'{'\n\n'.join(output.chaps)}'
    )

    path = Config.OUTPUT / f'{output.title}.txt'
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', path.name)
    safe_path = path.parent / safe_name
    text_writer.write(full_content, safe_path)


if __name__ == '__main__':
    main()
