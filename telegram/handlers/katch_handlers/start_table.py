import asyncio

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from databases.database import Database
from telegram.buttons.table_buttons import get_table_buttons
from telegram.handlers.katch_handlers.get_status import get_all_status
from telegram.utilities.special_characters import escape_all

start_tables_router = Router()


class Form(StatesGroup):
    start_tables_form = State()


@start_tables_router.callback_query(F.data == "start_table")
async def settings_handler(call: CallbackQuery, state: FSMContext, db: Database):
    text = f'*Запустить*\n\n{await get_all_status(db)}'
    await state.set_state(Form.start_tables_form)
    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=get_table_buttons(all_button=True, back_to_katch=True).as_markup())


@start_tables_router.callback_query(Form.start_tables_form, F.data.in_({'1', '2', '3', '4', '5', 'all'}))
async def start_katch_table(call: CallbackQuery, state: FSMContext, db: Database):
    if call.data in ['1', '2', '3', '4', '5']:
        table = int(call.data)
        db.update_status(table_id=table, new_state='IGRAEM')
        text = f'*Запуск стола {table}...*'
        await call.message.edit_text(text=escape_all(text), parse_mode=ParseMode.MARKDOWN_V2)

    if call.data == 'all':
        text = '*Запуск всех столов...*'
        await call.message.edit_text(text=escape_all(text), parse_mode=ParseMode.MARKDOWN_V2)
        db.change_all_table_status(status='IGRAEM')

    await state.clear()
    await asyncio.sleep(2)
    await call.message.delete()
