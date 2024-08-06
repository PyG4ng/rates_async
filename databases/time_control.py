from typing import Literal, Optional

from databases.db_base import DbBase


class TimeControl(DbBase):
    """ Stop | Start Time """

    def create_table_time_control(self) -> None:
        with self.conn.cursor() as curs:
            curs.execute("""
                    CREATE TABLE IF NOT EXISTS time_control (
                        id SERIAL,
                        what_to_do VARCHAR(50),
                        time_to_check BIGINT,
                        status VARCHAR(50));
                    """)
            self.conn.commit()

    def insert_table_time_control(self, id: int, what_to_do: Literal['start_table', 'stop_table'], time_to_check: int,
                                  status: Literal['waiting', 'done']) -> None:
        with self.conn.cursor() as curs:
            curs.execute(
                f"INSERT INTO time_control(id, what_to_do, time_to_check, status) "
                f"VALUES(%s, %s, %s, %s);", (id, what_to_do, time_to_check, status))
            self.conn.commit()

    def drop_table_time_control(self) -> None:
        with self.conn.cursor() as curs:
            curs.execute("DROP TABLE time_control;")
            self.conn.commit()

    def get_time_control(self) -> Optional[tuple]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT what_to_do, time_to_check, status FROM time_control WHERE id = 1;")
            result = curs.fetchall()
            if result:
                return result[-1]

    def update_time_to_check(self, time_to_check: int) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE time_control SET time_to_check = %s WHERE id = 1;", (time_to_check,))
            self.conn.commit()

    def update_what_to_do(self, what_to_do: Literal['start_table', 'stop_table']) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE time_control SET what_to_do = %s WHERE id = 1;", (what_to_do,))
            self.conn.commit()

    def update_time_control_status(self, status: Literal['waiting', 'done']) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE time_control SET status = %s  WHERE id = 1;", (status,))
            self.conn.commit()
