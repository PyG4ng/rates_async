from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from telegram.authentication.authorizations import is_user_authorized
from telegram.buttons.main_buttons import get_main_buttons

menu_router = Router()


@menu_router.message(F.chat.type == 'private', Command('menu'))
async def command_menu(msg: Message) -> None:
    tg_user_id = msg.from_user.id
    if await is_user_authorized(tg_user_id) is True:
        await msg.answer(f'*Меню*', reply_markup=get_main_buttons().as_markup(), parse_mode='MarkdownV2')
        await msg.delete()
