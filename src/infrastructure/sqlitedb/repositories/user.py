import hashlib
from src.infrastructure.sqlitedb.connection import get_connection


class UserRepository:
    def get_all(self):
        '''Lấy toàn bộ user có trong bảng user'''
        conn = get_connection()
        try:
            cursor = conn.execute("""
                                  SELECT id, email, password_hash, role
                                  FROM users
                                  ;
                                  """)

            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def get_user(self, email: str, password: str):
        """Lấy user nếu email và password chính xác."""

        password_hash = hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

        conn = get_connection()

        try:
            cursor = conn.execute(
                """
                SELECT id, email, password_hash, role
                FROM users
                WHERE email = ?
                  AND password_hash = ?
                """,
                (email, password_hash)
            )

            row = cursor.fetchone()

            return dict(row) if row else None

        finally:
            conn.close()


if __name__ == '__main__':
    from pprint import pprint

    r = UserRepository()
    # pprint(r.get_all())
    pprint(r.get_user(
        email='minhprompt@gmail.com',
        password='123456'
    ))