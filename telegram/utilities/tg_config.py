import os

from dotenv import load_dotenv

from configs.config import ROOT_FOLDER

load_dotenv(f'{ROOT_FOLDER}/.env')

TOKEN = os.getenv('TOKEN_TG')
MY_TG_ID = int(os.getenv('MY_ID'))
USER_TG_ID = int(os.getenv('USER_TG_ID'))
AUTHORIZED_IDS = [MY_TG_ID, USER_TG_ID]
