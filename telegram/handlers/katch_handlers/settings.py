from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.buttons.settings_buttons import get_settings_buttons

settings_router = Router()


@settings_router.callback_query(F.data == "settings")
async def settings_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(text=f'*Настройки ⚙️*', parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=get_settings_buttons().as_markup())
