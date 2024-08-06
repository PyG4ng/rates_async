import asyncio
import re
from datetime import datetime, timezone, timedelta

from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from databases.async_database import get_time_control_status, get_time_control_time_to_check, get_time_control_wtd
from databases.database import Database
from telegram.buttons.planing_buttons import get_planing_buttons
from telegram.utilities import tg_config
from telegram.utilities.special_characters import escape_all

planing_router = Router()


class Form(StatesGroup):
    planing_form = State()


def get_time_for_russia(time_to_check: int) -> str:
    return (datetime.fromtimestamp(time_to_check, timezone.utc) + timedelta(hours=3)).strftime(
        '%d.%m.%Y %H:%M')


def get_planing_text_status(db: Database) -> str:
    text = ' '
    planing = db.get_time_control()
    what_to_do, time_to_check, status = planing
    if status == 'waiting':
        cur_status = 'Включено'
        planed_time = get_time_for_russia(time_to_check)
        planed_action = 'Остановить все столы 🅾️' if what_to_do == 'stop_table' else 'Запустить все столы ✅'
        text = f'_*Действие:*_ _{planed_action}_\n_*Дата:*_ _{escape_all(planed_time)}_'
    else:
        cur_status = 'Отключено'
    return f'{cur_status}\n{text}'


@planing_router.callback_query(F.data == "planing")
async def planing_handler(call: CallbackQuery, db: Database):
    cur_status_text = get_planing_text_status(db)
    text = f'*Планировать ⌛️ Старт Стоп*\n\n_*Состояние:*_ {cur_status_text}'
    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=get_planing_buttons().as_markup())


@planing_router.callback_query(F.data.in_({"planing_stop_table", "planing_start_table", "stop_planing"}))
async def select_planing_fooo(call: CallbackQuery, state: FSMContext, db: Database):
    if call.data == "stop_planing":
        db.update_time_control_status(status='done')
        cur_status_text = get_planing_text_status(db)
        text = f'*Планировать ⌛️ Старт Стоп*\n\n_*Состояние:*_ {cur_status_text}'
        await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                                     reply_markup=get_planing_buttons().as_markup())
        return

    if call.data == "planing_stop_table":
        await state.update_data(what_to_do="stop_table")
    if call.data == "planing_start_table":
        await state.update_data(what_to_do="start_table")
    text = 'Введите дату в таком формате:\n*дд\.мм\.гггг чч:мм*\n_*Пример:* 01\.03\.2023 02:01_'
    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(state=Form.planing_form)


def verify_date(input_text: str):
    pattern = r"(\d{2})\.(\d{2})\.(\d{4}) (\d{2}):(\d{2})"
    result = re.fullmatch(pattern, input_text)
    if result:
        day, month, year, hour, minutes = re.findall(pattern, input_text)[0]
        try:
            utc_requested_date = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour),
                                          minute=int(minutes), tzinfo=timezone.utc) - timedelta(hours=3)
            if not 1970 <= int(year) <= 2100:
                return
        except ValueError:
            # log the error
            return
        except Exception as e:
            # log the error
            return
        return utc_requested_date
    return


@planing_router.message(Form.planing_form)
async def set_planing(msg: Message, state: FSMContext, db: Database):
    new_date = msg.text

    data = await state.get_data()
    what_to_do = data.get('what_to_do')
    utc_requested_date = verify_date(new_date)

    if utc_requested_date is not None:
        db.update_what_to_do(what_to_do=what_to_do)
        db.update_time_to_check(round(datetime.timestamp(utc_requested_date)))
        db.update_time_control_status(status='waiting')
        cur_status_text = get_planing_text_status(db)
        text = f'*Планировать ⌛️ Старт Стоп*\n\n_*Состояние:*_ {cur_status_text}'
        await msg.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                         reply_markup=get_planing_buttons().as_markup())
    else:
        text = 'Неправильный формат даты ❗️\n' \
               '*дд\.мм\.гггг чч:мм*\n' \
               '_*Пример:*_ 01\.03\.2023 02:01\n\n' \
               '_Попробуйте ещё раз или /cancel чтобы завершить работу_'
        await msg.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)


async def check_table_state_on_time(bot: Bot, db: Database) -> None:
    while True:
        await asyncio.sleep(1)
        status = await get_time_control_status()
        if status == 'waiting' and datetime.now(timezone.utc).timestamp() >= await get_time_control_time_to_check():
            while True:
                if db.is_stol_perekid_on() == 'ON':
                    await asyncio.sleep(10)
                    continue
                else:
                    break

            wtd = await get_time_control_wtd()
            if wtd == 'start_table':
                db.change_all_table_status(status='IGRAEM')
                await bot.send_message(chat_id=tg_config.MY_TG_ID, text='*Запланирован Запуск по расписанию*',
                                       parse_mode=ParseMode.MARKDOWN_V2)
                if tg_config.USER_TG_ID != 0:
                    await bot.send_message(chat_id=tg_config.USER_TG_ID, text='*Запланирован Запуск по расписанию*',
                                           parse_mode=ParseMode.MARKDOWN_V2)
            elif wtd == 'stop_table':
                db.change_all_table_status(status='OSTANOVIT')
                db.change_auto_perekid(val=True)
                db.change_perekid_mode(val='no_mode')
                db.change_stol_perekid_state('ON')
                await bot.send_message(chat_id=tg_config.MY_TG_ID, text='*Запланирована Остановка по расписанию*',
                                       parse_mode=ParseMode.MARKDOWN_V2)
                if tg_config.USER_TG_ID:
                    await bot.send_message(chat_id=tg_config.USER_TG_ID, text='*Запланирована Остановка по расписанию*',
                                           parse_mode=ParseMode.MARKDOWN_V2)
            db.update_time_control_status(status='done')
