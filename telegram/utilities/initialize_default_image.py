import asyncio

from aiogram import Bot
from aiogram.types import FSInputFile
from loguru import logger

from configs import config
from databases.database import Database
from telegram.utilities import tg_config


async def create_default_image(bot: Bot, db: Database) -> None:
    file = FSInputFile(f'{config.ROOT_FOLDER}/telegram/utilities/default_image.png')
    try:
        api_answer = await bot.send_photo(photo=file, chat_id=tg_config.MY_TG_ID)
    except Exception as e:
        logger.info(str(e))
        return
    new_file_id = api_answer.photo[-1].file_id
    file_id = db.get_file_id(uid=1)
    if file_id is None:
        db.insert_table_base_image(uid=1, file_id=new_file_id)
    else:
        db.update_base_image(uid=1, file_id=new_file_id)
    await bot.delete_message(chat_id=tg_config.MY_TG_ID, message_id=api_answer.message_id)
