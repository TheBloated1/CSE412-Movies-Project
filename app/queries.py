from psycopg2.extras import RealDictCursor

class NetflixDB:
    """
    All SQL queries for the Netflix database application.
    Pass in an active psycopg2 connection on instantiation.
    """

    def __init__(self, conn):
        self.conn = conn

    def _cursor(self):
        return self.conn.cursor(cursor_factory=RealDictCursor)

    # ---------
    # INSERT
    # ---------

    def register_user(self, username, password_hash, role_name='user'):
        with self._cursor() as cur:
            cur.execute("""
                INSERT INTO users (username, password_hash, role)
                VALUES (%s, %s, (SELECT role_id FROM role WHERE role_name = %s))
                RETURNING user_id;
            """, (username, password_hash, role_name))
            self.conn.commit()
            return cur.fetchone()['user_id']

    def add_favorite(self, user_id, show_id):
        with self._cursor() as cur:
            cur.execute("""
                INSERT INTO isFavorited (f_user_id, f_show_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
            """, (user_id, show_id))
            self.conn.commit()

    # ---------
    # UPDATE
    # ---------

    def update_password(self, username, new_hash):
        with self._cursor() as cur:
            cur.execute("""
                UPDATE users SET password_hash = %s
                WHERE username = %s;
            """, (new_hash, username))
            self.conn.commit()

    def promote_to_admin(self, username):
        with self._cursor() as cur:
            cur.execute("""
                UPDATE users
                SET role = (SELECT role_id FROM role WHERE role_name = 'admin')
                WHERE username = %s;
            """, (username,))
            self.conn.commit()

    # -----------
    # DELETE
    # -----------

    def remove_favorite(self, user_id, show_id):
        with self._cursor() as cur:
            cur.execute("""
                DELETE FROM isFavorited
                WHERE f_user_id = %s AND f_show_id = %s;
            """, (user_id, show_id))
            self.conn.commit()

    # ---------
    # EXTRA
    # ---------
    def netflix_content_last_decade(self):
        with self._cursor() as cur: 
            cur.execute("""
                SELECT release_year, type, COUNT(*) AS count
                FROM media
                WHERE release_year IS NOT NULL
                AND release_year >= EXTRACT(YEAR FROM CURRENT_DATE) - 10
                GROUP BY release_year, type
                ORDER BY release_year DESC, type;
            """)
            self.conn.commit()
            return cur.fetchall()