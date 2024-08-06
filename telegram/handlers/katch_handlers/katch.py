from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegram.buttons.katch_buttons import get_katch_buttons
from telegram.handlers.perenos_handler import perenos_router
from telegram.handlers.katch_handlers.speed import speed_router
from telegram.handlers.get_tokens_handler import get_tokens_router
from telegram.handlers.katch_handlers.perekid import perekid_router
from telegram.handlers.katch_handlers.planing import planing_router
from telegram.handlers.katch_handlers.change_bets import bets_router
from telegram.handlers.katch_handlers.get_status import status_router
from telegram.handlers.katch_handlers.settings import settings_router
from telegram.handlers.katch_handlers.change_tokens import tokens_router
from telegram.handlers.katch_handlers.change_servers import servers_router
from telegram.handlers.katch_handlers.stop_table import stop_tables_router
from telegram.handlers.katch_handlers.start_table import start_tables_router
from telegram.handlers.katch_handlers.check_balance import check_balance_router
from telegram.handlers.katch_handlers.manage_accounts import manage_account_router
from telegram.handlers.katch_handlers.change_wins_and_rate import wins_and_rate_router

katch_router = Router()
routers_to_include = [
    settings_router,
    tokens_router,
    servers_router,
    bets_router,
    wins_and_rate_router,
    perekid_router,
    check_balance_router,
    status_router,
    speed_router,
    start_tables_router,
    stop_tables_router,
    planing_router,
    manage_account_router,
    get_tokens_router,
    perenos_router
]
katch_router.include_routers(*routers_to_include)


@katch_router.callback_query(F.data == "katch")
async def katch_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(text=f'*Прокачка ✨*', parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=get_katch_buttons().as_markup())
