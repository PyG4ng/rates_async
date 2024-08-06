from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from databases.database import Database
from katch.system import servers
from telegram.buttons.katch_buttons import get_back_to_katch_button
from telegram.handlers.katch_handlers.change_wins_and_rate import get_wins_rate_and_limits_text_info
from telegram.handlers.katch_handlers.perekid import perekid_text_info
from telegram.handlers.katch_handlers.planing import get_planing_text_status
from telegram.utilities.special_characters import escape_all, frmt

status_router = Router()


@status_router.callback_query(F.data == "get_status")
async def check_balance_handler(call: CallbackQuery, db: Database):
    text = f'* Cостояние столов*\n\n{await get_all_status(db)}'
    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=get_back_to_katch_button().as_markup())


async def get_all_status(db: Database):
    text = ''
    all_data = db.get_everything()
    game_servers = await servers.get_servers_async()
    server_names = game_servers[1]
    for i in range(5):
        status = 'Остановлен' if all_data[i][1] == 'OSTANOVIT' else 'Работает'
        text += f'*Стол:* {all_data[i][0]}\n*Статус:* {status}\n*Ставка:* {frmt(all_data[i][2])}\n' \
                f'*Сервер:* {escape_all(server_names[all_data[i][3]])}\n*Сделано побед:* {frmt(all_data[i][4])}\n\n'

    wins_rate_text = get_wins_rate_and_limits_text_info(db)
    text += wins_rate_text

    perekid_info = perekid_text_info(db)
    text += perekid_info

    planing_text = get_planing_text_status(db)
    text += f'\n\n_*Действие по расписанию:*_ {planing_text}'

    return text
