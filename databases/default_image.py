from typing import Optional

from databases.db_base import DbBase


class BaseImage(DbBase):
    """ Tables base_image """

    def create_table_base_image(self) -> None:
        with self.conn.cursor() as curs:
            curs.execute("""
                CREATE TABLE IF NOT EXISTS base_image (
                    id SERIAL,
                    file_id VARCHAR(250) NOT NULL
                """)
            self.conn.commit()

    def insert_table_base_image(self, uid: int, file_id: str) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"INSERT INTO base_image(id, file_id) VALUES(%s, %s);", (uid, file_id))
            self.conn.commit()

    def drop_table_base_image(self) -> None:
        with self.conn.cursor() as curs:
            curs.execute("DROP TABLE base_image;")
            self.conn.commit()

    def get_file_id(self, uid: int) -> Optional[str]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT file_id FROM base_image WHERE id = %s;", (uid,))
            result = curs.fetchall()
            return self.return_first_element_or_none(result=result)

    def update_base_image(self, uid: int, file_id: str) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE base_image SET file_id = %s WHERE id = %s;", (file_id, uid))
            self.conn.commit()
