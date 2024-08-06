from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from telegram.authentication.authorizations import is_user_authorized
from telegram.utilities import tg_config

start_router = Router()


@start_router.message(F.chat.type == 'private', CommandStart())
async def command_start(msg: Message, bot: Bot) -> None:
    tg_user_id = msg.from_user.id
    if await is_user_authorized(tg_user_id) is True:
        await msg.answer(f"Hello ️✨, {msg.from_user.full_name} !")
        text = f'Доступ ОК ✅\n{msg.from_user.id}\n{msg.from_user.full_name}\n@{msg.from_user.username}'
    else:
        await msg.answer(f"Hello ️❌, {msg.from_user.full_name} ! Доступ запрещён ⛔️")
        text = f'Доступ запрещён ⛔️\n{msg.from_user.id}\n{msg.from_user.full_name}\n@{msg.from_user.username}'

    if tg_user_id != tg_config.MY_TG_ID:
        try:
            await bot.send_message(chat_id=tg_config.MY_TG_ID, text=text)
        except Exception as e:
            # log text and the error
            ...
