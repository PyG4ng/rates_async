import asyncio

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from databases.database import Database
from telegram.buttons.katch_buttons import get_back_to_katch_button

speed_router = Router()


@speed_router.callback_query(F.data == "speed")
async def settings_handler(call: CallbackQuery, db: Database):
    text = '*Подсчёт скорости запускается 🚀*'
    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=get_back_to_katch_button().as_markup())
    await get_speed_last_minute(call, db, 5)


async def get_speed_last_minute(call: CallbackQuery, db: Database, minutes: int) -> None:
    for i in range(minutes):
        total_wins = db.get_total_wins()
        await asyncio.sleep(60)
        total_wins_2 = db.get_total_wins()
        speed = total_wins_2 - total_wins
        text = f'🚀 _*{i + 1}\|{minutes}*_ : *{speed}* _/min_ '
        await call.message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)
