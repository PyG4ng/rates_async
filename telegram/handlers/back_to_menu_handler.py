from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from telegram.buttons.main_buttons import get_main_buttons

back_to_menu_router = Router()


@back_to_menu_router.callback_query(F.data == "back_to_menu")
async def back_to_menu(call: CallbackQuery) -> None:
    await call.message.edit_text('*Меню*', reply_markup=get_main_buttons().as_markup(),
                                 parse_mode=ParseMode.MARKDOWN_V2)
