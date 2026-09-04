from src.infrastructure.sqlitedb.connection import get_connection


class PromptsRepository:
    def get_by_set_id(self, set_id):
        conn = get_connection()

        try:
            cursor = conn.execute(
                """
                SELECT id, prompt_set_id, prompt_type, content, created_at, updated_at
                FROM prompts
                WHERE prompt_set_id = ?;
                """,
                (set_id)
            )

            return [dict(row) for row in cursor.fetchall()]

        finally:
            conn.close()
