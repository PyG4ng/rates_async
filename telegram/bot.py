import asyncio
import logging
import sys

from aiogram import Dispatcher, Bot

from loguru import logger
from configs.config import ROOT_FOLDER
from databases.database import Database
from telegram.handlers.katch_handlers.planing import check_table_state_on_time
from telegram.utilities import tg_config
from telegram.handlers.commands.menu import menu_router
from telegram.handlers.commands.start import start_router
from telegram.handlers.commands.cancel import cancel_router
from telegram.handlers.katch_handlers.katch import katch_router
from telegram.handlers.back_to_menu_handler import back_to_menu_router
from telegram.utilities.initialize_default_image import create_default_image

db = Database()

logger.remove()
logger.add(sys.stderr, format="{time:HH:mm:ss.SSS} {message}", level="INFO")
logger.add(f'{ROOT_FOLDER}/logs.log')


@logger.catch
async def main() -> None:
    dp = Dispatcher()
    bot = Bot(tg_config.TOKEN)
    dp.include_routers(cancel_router, start_router, menu_router)
    dp.include_routers(back_to_menu_router, katch_router)
    loop = asyncio.get_event_loop()
    loop.create_task(check_table_state_on_time(bot=bot, db=db))

    await create_default_image(bot=bot, db=db)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, db=db)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
