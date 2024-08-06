import time
from typing import Optional

import psycopg2
from psycopg2 import OperationalError


class DbBase:
    def __init__(self, connection_params=None):
        if connection_params is None:
            raise ValueError('Missing DSN for database connection')
        while True:
            try:
                self.conn = psycopg2.connect(**connection_params)
            except OperationalError as error:
                print(error)
                print('DB not ready waiting 10 seconds')
                time.sleep(10)
            else:
                break

    def close_connection(self) -> None:
        self.conn.close()

    @staticmethod
    def return_first_element_or_none(result) -> Optional[int | str | bool]:
        if isinstance(result, list) and len(result) >= 1 and isinstance(result[0], tuple) and len(result[0]) >= 1:
            return result[0][0]
        else:
            return None
