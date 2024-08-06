import asyncio

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from databases.database import Database
from telegram.buttons.table_buttons import get_table_buttons
from telegram.utilities import names
from telegram.utilities.special_characters import escape_all

bets_router = Router()


class Form(StatesGroup):
    change_bets_form = State()
    set_bet_form = State()


@bets_router.callback_query(F.data == "change_bets")
async def bets_handler(call: CallbackQuery, state: FSMContext, db: Database):
    await state.set_state(Form.change_bets_form)
    text = f'*💸 Текущие ставки столов*\n' \
           f'{currents_bet(db)}\n' \
           f'_Введите цифру соответсвующая выбраному столу для замены ставки_'
    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=get_table_buttons(all_button=True).as_markup())


def currents_bet(db: Database) -> str:
    text = ''
    all_bets = db.get_all_bets()
    for table, bet in all_bets:
        text += f'*{table}:* {bet}\n'
    return text


@bets_router.callback_query(Form.change_bets_form, F.data.in_({'1', '2', '3', '4', '5', 'all'}))
async def change_table_bets(call: CallbackQuery, state: FSMContext):
    if call.data == 'all':
        text = '*Введите ставку для всех столов: *'
        table = call.data
    else:
        table = int(call.data)
        text = f'*Введите ставку стола {table}: *'
    await state.update_data(table=table)
    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(Form.set_bet_form)


def is_bet_valid(bet: int) -> bool:
    if bet in [100, 250, 500, 1000, 2500, 5000,
               10_000, 25_000, 50_000, 100_000, 250_000,
               500_000, 1_000_000, 2_500_000, 5_000_000, 10_000_000]:
        return True
    else:
        return False


@bets_router.message(Form.set_bet_form)
async def set_players_tokens(msg: Message, state: FSMContext, db: Database):
    new_bet = msg.text

    if " " in new_bet:
        new_bet = ''.join(new_bet.split(" "))
    data = await state.get_data()
    table = data.get('table')

    if new_bet.isdigit() and is_bet_valid(int(new_bet)):
        new_bet = int(new_bet)
        if table == 'all':
            db.update_all_bet(bet=new_bet)
        elif table in [1, 2, 3, 4, 5]:
            db.update_bet(table_id=table, bet=new_bet)
        text = f'💸✅ Новая ставка {names.NAMES_HELP.get(table)}: *{new_bet}*'
        await msg.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)
        await asyncio.sleep(0.3)
        await state.set_state(Form.change_bets_form)
        text = f'*💸 Текущие ставки столов*\n' \
               f'{currents_bet(db)}\n' \
               f'_Введите цифру соответсвующая выбраному столу для замены ставки_'
        await msg.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                         reply_markup=get_table_buttons(all_button=True).as_markup())
    else:
        text = f'*💸 Неправильная ставка ❗️:* \n' \
               f'{escape_all(new_bet)}\n' \
               f'_Введите ставку для {names.NAMES_HELP.get(table)} или /cancel чтобы завершить_'
        await msg.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)
