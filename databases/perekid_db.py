from typing import Literal, Optional

from databases.db_base import DbBase


class Perekid(DbBase):
    """ Tables perekid """

    def create_tale_perekid(self) -> None:
        with self.conn.cursor() as curs:
            curs.execute("""
                    CREATE TABLE IF NOT EXISTS perekid (
                        id SERIAL,
                        stol_perekid VARCHAR(50) NOT NULL,
                        auto_perekid BOOLEAN NOT NULL,
                        perekid_by_points BOOLEAN NOT NULL,
                        perekid_by_wins BOOLEAN NOT NULL,
                        perekid_by_rate BOOLEAN NOT NULL,
                        how_much_to_perekid INT,
                        credits_got_back INT,
                        perekid_mode VARCHAR(50));
                    """)
            self.conn.commit()

    def insert_table_perekid(self, stol_perekid: Literal['ON', 'OFF'], auto_perekid: bool, perekid_by_points: bool,
                             perekid_by_wins: bool) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"""INSERT INTO perekid(stol_perekid, auto_perekid, perekid_by_points, perekid_by_wins) 
                             VALUES(%s, %s, %s, %s);""",
                         (stol_perekid, auto_perekid, perekid_by_points, perekid_by_wins))
            self.conn.commit()

    def drop_table_perekid(self) -> None:
        with self.conn.cursor() as curs:
            curs.execute("DROP TABLE perekid;")
            self.conn.commit()

    def is_stol_perekid_on(self) -> Optional[str]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT stol_perekid FROM perekid WHERE id = 1;")
            result = curs.fetchall()
            return self.return_first_element_or_none(result)

    def change_stol_perekid_state(self, val: Literal['ON', 'OFF']) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE perekid SET stol_perekid = %s WHERE id = 1;", (val,))
            self.conn.commit()

    def is_auto_perekid(self) -> Optional[bool]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT auto_perekid FROM perekid WHERE id = 1;")
            result = curs.fetchall()
            return self.return_first_element_or_none(result)

    def change_auto_perekid(self, val: bool) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE perekid SET auto_perekid = %s WHERE id = 1;", (val,))
            self.conn.commit()

    def is_perekid_by_points(self) -> Optional[bool]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT perekid_by_points FROM perekid WHERE id = 1;")
            result = curs.fetchall()
            return self.return_first_element_or_none(result)

    def change_perekid_by_points(self, val: bool) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE perekid SET perekid_by_points = %s WHERE id = 1;", (val,))
            self.conn.commit()

    def is_perekid_by_wins(self) -> Optional[bool]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT perekid_by_wins FROM perekid WHERE id = 1;")
            result = curs.fetchall()
            return self.return_first_element_or_none(result)

    def change_perekid_by_wins(self, val: bool) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE perekid SET perekid_by_wins = %s WHERE id = 1;", (val,))
            self.conn.commit()

    def is_perekid_by_rate(self) -> Optional[bool]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT perekid_by_rate FROM perekid WHERE id = 1;")
            result = curs.fetchall()
            return self.return_first_element_or_none(result)

    def change_perekid_by_rate(self, val: bool) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE perekid SET perekid_by_rate = %s WHERE id = 1;", (val,))
            self.conn.commit()

    def get_how_much_to_perekid(self) -> Optional[int]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT how_much_to_perekid FROM perekid WHERE id = 1;")
            result = curs.fetchall()
            return self.return_first_element_or_none(result)

    def change_how_much_to_perekid(self, val: int) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE perekid SET how_much_to_perekid = %s WHERE id = 1;", (val,))
            self.conn.commit()

    def get_credits_got_back(self) -> Optional[int]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT credits_got_back FROM perekid WHERE id = 1;")
            result = curs.fetchall()
            return self.return_first_element_or_none(result)

    def change_credits_got_back(self, val: int) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE perekid SET credits_got_back = %s WHERE id = 1;", (val,))
            self.conn.commit()

    def get_perekid_mode(self) -> Optional[str]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT perekid_mode FROM perekid WHERE id = 1;")
            result = curs.fetchall()
            return self.return_first_element_or_none(result)

    def change_perekid_mode(self, val: Literal['points', 'wins', 'rate', 'no_mode']) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE perekid SET perekid_mode = %s WHERE id = 1;", (val,))
            self.conn.commit()
