import os

from dotenv import load_dotenv

from configs import config
from databases.stoly import Stoly
from databases.tokens import Tokens
from databases.perekid_db import Perekid
from databases.parameters import Parameters
from databases.default_image import BaseImage
from databases.time_control import TimeControl

load_dotenv(f'{config.ROOT_FOLDER}/.env')

remote = {"dbname": os.getenv('PG_DB'),
          "user": os.getenv('PG_USER'),
          "password": os.getenv('PG_PASSWORD'),
          "host": os.getenv('REMOTE_HOST'),
          "port": 5432}

local = {
    "host": os.getenv('LOCAL_HOST'),
    "port": 5432,
    "database": os.getenv('PG_DB'),
    "user": os.getenv('PG_USER'),
    "password": os.getenv('PG_PASSWORD')}

current = remote


class Database(Tokens, Stoly, Parameters, Perekid, BaseImage, TimeControl):
    def __init__(self):
        super(Database, self).__init__(connection_params=current)
