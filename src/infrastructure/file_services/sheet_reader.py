from openpyxl import load_workbook


class SheetReader:

    def read(self, file_path: str) -> list[dict]:
        workbook = load_workbook(file_path, data_only=True)
        sheet = workbook.active

        rows = list(sheet.iter_rows(values_only=True))

        if not rows:
            return []

        headers = rows[0]

        return [
            dict(zip(headers, row))
            for row in rows[1:]
        ]

if __name__ == '__main__':
    from pprint import pprint
    sheet = SheetReader()
    pprint(sheet.read(r"C:\Users\Admin\Downloads\3.xlsx"))
