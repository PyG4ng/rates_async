from typing import Literal, Optional

from databases.db_base import DbBase


class Tokens(DbBase):
    """ Tables tokens """

    def create_tale_tokens(self) -> None:
        with self.conn.cursor() as curs:
            curs.execute("""
                CREATE TABLE IF NOT EXISTS tokens (
                    player VARCHAR(50) NOT NULL,
                    tkn VARCHAR(50) NOT NULL);
                """)
            self.conn.commit()

    def insert_table_tokens(self, player: Literal['BOT_TOKEN', 'CLIENT_TOKEN'], tkn: str) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"INSERT INTO tokens(player, tkn) VALUES(%s, %s);", (player, tkn))
            self.conn.commit()

    def drop_table_tokens(self) -> None:
        with self.conn.cursor() as curs:
            curs.execute("DROP TABLE tokens;")
            self.conn.commit()

    def get_token(self, player: str) -> Optional[str]:
        with self.conn.cursor() as curs:
            curs.execute(f"SELECT tkn FROM tokens WHERE player = %s;", (player,))
            result = curs.fetchall()
            return self.return_first_element_or_none(result)

    def update_token(self, player_token: str, tkn: str) -> None:
        with self.conn.cursor() as curs:
            curs.execute(f"UPDATE tokens SET tkn = %s WHERE player = %s;", (tkn, player_token))
            self.conn.commit()
