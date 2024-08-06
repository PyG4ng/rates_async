from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from databases.database import Database
from telegram.utilities.get_credits import form_balance
from telegram.buttons.katch_buttons import get_back_to_katch_button

check_balance_router = Router()


@check_balance_router.callback_query(F.data == "check_balance")
async def check_balance_handler(call: CallbackQuery, db: Database):
    text = await form_balance(db=db)
    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=get_back_to_katch_button().as_markup())
