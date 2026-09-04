from src.infrastructure.sqlitedb.connection import get_connection


class PromptsSetRepository:
    def get_all(self):
        conn = get_connection()

        try:
            cursor = conn.execute("""
                                  SELECT id, name, description, created_at, updated_at
                                  FROM prompt_sets
                                  ORDER BY id
                                  """)

            return [dict(row) for row in cursor.fetchall()]

        finally:
            conn.close()

    def create(self, name: str, description: str | None = None):
        conn = get_connection()

        try:
            cursor = conn.execute(
                """
                INSERT INTO prompt_sets (name, description)
                VALUES (?, ?)
                """,
                (name, description)
            )

            conn.commit()

            return cursor.lastrowid

        finally:
            conn.close()




if __name__ == '__main__':
    from pprint import pprint

    # psr = PromptsSetRepository()
    # pprint(psr.get_all())


