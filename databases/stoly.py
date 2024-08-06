from typing import Literal, Optional

from databases.db_base import DbBase


class Stoly(DbBase):
    """ Tables -status -bet -server -wins_count """

    def create_tale_stoly(self) -> None:
        with self.conn.cursor() as curs:
            curs.execute("""
                CREATE TABLE IF NOT EXISTS stoly (
                    id SERIAL,
                    status VARCHAR(50) NOT NULL,
                    bet INT NOT NULL,
                    server INT NOT NULL,
                    wins_count INT,
                    connection_retry INT,
                    credits_spent INT);
                """)
            self.conn.commit()

    def insert_table_stoly(self, table_id: int, status: Literal['OSTANOVIT', 'IGRAEM'], bet: int, server: int,
                           wins_count: int) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"""INSERT INTO stoly(id, status, bet, server, wins_count) 
                                VALUES(%s, %s, %s, %s, %s);""", (table_id, status, bet, server, wins_count))
            self.conn.commit()

    def drop_table_stoly(self) -> None:
        with self.conn.cursor() as curs:
            curs.execute("DROP TABLE stoly;")
            self.conn.commit()

    def get_everything(self) -> Optional[tuple]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT * FROM stoly ORDER BY id;")
            result = curs.fetchall()
            if result:
                return result

    "status"

    def get_status(self, table_id: int) -> Optional[str]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT status FROM stoly WHERE id = %s;", (table_id,))
            result = curs.fetchall()
            return self.return_first_element_or_none(result)

    def update_status(self, table_id: int, new_state: Literal['OSTANOVIT', 'IGRAEM']) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE stoly SET status = %s WHERE id = %s;", (new_state, table_id))
            self.conn.commit()

    def change_all_table_status(self, status: Literal['OSTANOVIT', 'IGRAEM']) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE stoly SET status = %s;", (status,))
            self.conn.commit()

    "bet"

    def get_bet(self, table_id: int) -> Optional[int]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT bet FROM stoly WHERE id = %s;", (table_id,))
            result = curs.fetchall()
            return self.return_first_element_or_none(result)

    def get_all_bets(self) -> Optional[tuple]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT id, bet FROM stoly ORDER BY id;")
            result = curs.fetchall()
            if result:
                return result

    def update_bet(self, table_id: int, bet: int) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE stoly SET bet = %s WHERE id = %s;", (bet, table_id))
            self.conn.commit()

    def update_all_bet(self, bet: int) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE stoly SET bet = %s;", (bet,))
            self.conn.commit()

    "server"

    def get_server(self, table_id: int) -> Optional[int]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT server FROM stoly WHERE id = %s;", (table_id,))
            result = curs.fetchall()
            return self.return_first_element_or_none(result)

    def get_all_servers(self) -> Optional[tuple]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT id, server FROM stoly ORDER BY id;")
            result = curs.fetchall()
            if result:
                return result

    def update_server(self, table_id: int, server: int) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE stoly SET server = %s WHERE id = %s;", (server, table_id))
            self.conn.commit()

    "wins_count"

    def get_wins_count(self, table_id: int) -> Optional[int]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT wins_count FROM stoly WHERE id = %s;", (table_id,))
            result = curs.fetchall()
            return self.return_first_element_or_none(result)

    def update_wins_count(self, table_id: int, wins_count: int) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE stoly SET wins_count = %s WHERE id = %s;", (wins_count, table_id))
            self.conn.commit()

    def update_all_wins_count(self, wins_count: int) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE stoly SET wins_count = %s;", (wins_count,))
            self.conn.commit()

    def get_total_wins(self):
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT SUM(wins_count) FROM stoly;")
            result = curs.fetchall()
            return self.return_first_element_or_none(result)

    "connection_retry"

    def get_connection_retry(self, table_id: int) -> Optional[int]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT connection_retry FROM stoly WHERE id = %s;", (table_id,))
            result = curs.fetchall()
            return self.return_first_element_or_none(result)

    def update_connection_retry(self, table_id: int, retries: int) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE stoly SET connection_retry = %s WHERE id = %s;", (retries, table_id))
            self.conn.commit()

    def update_all_connection_retry(self, retries: int) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE stoly SET connection_retry = %s;", (retries,))
            self.conn.commit()

    "credits_spent"

    def get_credits_spent(self, table_id: int) -> Optional[int]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT credits_spent FROM stoly WHERE id = %s;", (table_id,))
            result = curs.fetchall()
            return self.return_first_element_or_none(result)

    def update_credits_spent(self, table_id: int, credits: int) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE stoly SET credits_spent = %s WHERE id = %s;", (credits, table_id))
            self.conn.commit()

    def update_all_credits_spent(self, credits: int) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE stoly SET credits_spent = %s;", (credits,))
            self.conn.commit()

    def get_total_credits_spent(self) -> Optional[int]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT SUM(credits_spent) FROM stoly;")
            result = curs.fetchall()
            return self.return_first_element_or_none(result)
