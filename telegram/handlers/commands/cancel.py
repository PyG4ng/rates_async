import asyncio

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from telegram.authentication.authorizations import is_user_authorized

cancel_router = Router()


@cancel_router.message(F.chat.type == 'private', Command('cancel'))
async def cancel_command(msg: Message, state: FSMContext):
    tg_user_id = msg.from_user.id
    if await is_user_authorized(tg_user_id) is True:
        await state.clear()
        msg_2 = await msg.answer('*Отмена*', parse_mode=ParseMode.MARKDOWN_V2)
        await asyncio.sleep(0.3)
        await msg.delete()
        await msg_2.delete()


@cancel_router.callback_query(F.data == "close_menu")
async def close_menu_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await asyncio.sleep(0.3)
    await call.message.delete()
