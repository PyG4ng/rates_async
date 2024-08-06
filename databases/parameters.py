from typing import Literal, Optional

from databases.db_base import DbBase


class Parameters(DbBase):
    """ Tables parameters """

    def create_table_parameters(self) -> None:
        with self.conn.cursor() as curs:
            curs.execute("""
                CREATE TABLE IF NOT EXISTS parameters (
                    param VARCHAR(50) NOT NULL,
                    val INT NOT NULL);
                """)
            self.conn.commit()

    def insert_table_parameters(self, param: Literal['wins_limit_value', 'are_wins_limited',
                                                     'is_rate_limited', 'rate_limit_value'], value: int) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"INSERT INTO parameters(param, val) VALUES(%s, %s);", (param, value))
            self.conn.commit()

    def drop_table_parameters(self) -> None:
        with self.conn.cursor() as curs:
            curs.execute("DROP TABLE parameters;")
            self.conn.commit()

    def get_parameter(self, param: Literal['wins_limit_value', 'are_wins_limited',
                                           'is_rate_limited', 'rate_limit_value']) -> Optional[int | bool]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT val FROM parameters WHERE param = %s;", (param,))
            result = curs.fetchall()
            return self.return_first_element_or_none(result)

    def update_parameters(self,
                          param: Literal['wins_limit_value', 'are_wins_limited', 'is_rate_limited', 'rate_limit_value'],
                          value: int) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE parameters SET val = %s WHERE param = %s;", (value, param))
            self.conn.commit()
