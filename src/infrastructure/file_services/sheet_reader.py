from openpyxl import load_workbook
import csv


class SheetReader:

    # def read(self, file_path: str) -> list[dict]:
    #     workbook = load_workbook(file_path, data_only=True)
    #     sheet = workbook.active
    #
    #     rows = list(sheet.iter_rows(values_only=True))
    #
    #     if not rows:
    #         return []
    #
    #     headers = rows[0]
    #
    #     return [
    #         dict(zip(headers, row))
    #         for row in rows[1:]
    #     ]

    def read(self, file_path: str) -> list[dict]:
        with open(file_path, mode="r", encoding="utf-8-sig", newline="") as file:
            return list(csv.DictReader(file))


if __name__ == '__main__':
    from pprint import pprint
    from tkinter import filedialog

    path = filedialog.askopenfilename()
    sheet = SheetReader()
    shots = sheet.read(path)
    excludes = ['shot_id', '']
    for shot in shots:
        print()
        for key, value in shot.items():
            if key in excludes:
                continue
            print(f"<{key}>{value}</{key}>")
