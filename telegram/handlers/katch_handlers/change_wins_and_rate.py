from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from databases.database import Database
from telegram.utilities.special_characters import frmt
from telegram.buttons.wins_rate_buttons import get_wins_and_rate_buttons

wins_and_rate_router = Router()


class Form(StatesGroup):
    set_wins_or_rate = State()


def get_wins_limit_and_wins_total(db: Database) -> tuple:
    wins_set = db.get_parameter('wins_limit_value')
    is_wins_set_active = db.get_parameter('are_wins_limited')
    wins_total = db.get_total_wins()
    credits_spent = db.get_total_credits_spent()
    return wins_set, wins_total, is_wins_set_active, credits_spent


def get_wins_rate_and_limits_text_info(db: Database) -> str:
    wins_set, wins_total, is_wins_set_active, credits_spent = get_wins_limit_and_wins_total(db)
    limit = 'Включено' if is_wins_set_active else 'Отключено'
    text = f'_*Сделано побед:*_ {frmt(wins_total)}\n_*Потрачено кредитов:*_ {frmt(credits_spent)}\n\n' \
           f'_*Ограничение по победам:*_ {limit}'
    if is_wins_set_active:
        text += f'\n_*Количество:*_ _{frmt(wins_set)} 🏆_'

    rate_limit = 'Включено' if db.get_parameter('is_rate_limited') else 'Отключено'
    text += f'\n\n_*Ограничение по рейтингу:*_ {rate_limit}'
    if rate_limit == 'Включено':
        text += f'\n_*Рейтинг:*_ {frmt(db.get_parameter("rate_limit_value"))} 🌟'

    return text


@wins_and_rate_router.callback_query(F.data == "change_wins_and_rate")
async def wins_and_rate_handler(call: CallbackQuery, db: Database):
    wins_rate_text_info = get_wins_rate_and_limits_text_info(db)
    text = f'*Настройки побед и рейтинга*\n\n{wins_rate_text_info}'
    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=get_wins_and_rate_buttons().as_markup())


CALLBACK_RESPONSES = {"reset_wins_count",
                      "activate_deactivate_wins_limit",
                      "activate_deactivate_rate_limit",
                      "set_wins_limit",
                      "set_rate_limit"}


def reset_wins(db: Database) -> None:
    db.update_all_wins_count(0)
    db.update_all_credits_spent(0)
    db.change_credits_got_back(0)


@wins_and_rate_router.callback_query(F.data.in_(CALLBACK_RESPONSES))
async def wins_and_rate_settings(call: CallbackQuery, state: FSMContext, db: Database):
    if call.data == "reset_wins_count":
        reset_wins(db)

    if call.data == "activate_deactivate_wins_limit":
        value = 0 if db.get_parameter(param='are_wins_limited') == 1 else 1
        db.update_parameters(param='are_wins_limited', value=value)
        if value == 1:
            db.update_parameters(param='is_rate_limited', value=0)
            db.change_perekid_by_rate(val=False)

    if call.data == "activate_deactivate_rate_limit":
        value = 0 if db.get_parameter(param='is_rate_limited') == 1 else 1
        db.update_parameters(param='is_rate_limited', value=value)
        if value == 1:
            db.update_parameters(param='are_wins_limited', value=0)
            db.change_perekid_by_wins(val=False)

    if call.data == "set_wins_limit":
        await state.update_data(what_to_set='set_wins_limit')
        await call.message.edit_text(text='*Введите Количество побед: *', parse_mode=ParseMode.MARKDOWN_V2)
        await state.set_state(Form.set_wins_or_rate)
        await call.message.delete()
        return

    if call.data == "set_rate_limit":
        await state.update_data(what_to_set='set_rate_limit')
        await call.message.edit_text(text='*Введите рейтинг на котором надо остановиться: *',
                                     parse_mode=ParseMode.MARKDOWN_V2)
        await state.set_state(Form.set_wins_or_rate)
        await call.message.delete()
        return

    wins_rate_text_info = get_wins_rate_and_limits_text_info(db)
    text = f'*Настройки побед и рейтинга*\n\n{wins_rate_text_info}'
    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=get_wins_and_rate_buttons().as_markup())


@wins_and_rate_router.message(Form.set_wins_or_rate)
async def set_players_tokens(msg: Message, state: FSMContext, db: Database):
    new_limit = msg.text

    if " " in new_limit:
        new_limit = ''.join(new_limit.split(" "))

    if new_limit.isdigit():
        data = await state.get_data()
        what_to_set = data.get('what_to_set')

        if what_to_set == 'set_wins_limit':
            db.update_parameters(param='wins_limit_value', value=int(new_limit))
            db.update_parameters(param='are_wins_limited', value=1)
            db.update_parameters(param='is_rate_limited', value=0)
            db.change_perekid_by_rate(val=False)
            await msg.answer(f'*Новое ограничение побед:* {new_limit}', parse_mode=ParseMode.MARKDOWN_V2)
        elif what_to_set == 'set_rate_limit':
            db.update_parameters(param='rate_limit_value', value=int(new_limit))
            db.update_parameters(param='is_rate_limited', value=1)
            db.update_parameters(param='are_wins_limited', value=0)
            db.change_perekid_by_wins(val=False)
            await msg.answer(f'*Новое ограничение  рейтинга:* {new_limit}', parse_mode=ParseMode.MARKDOWN_V2)

        await state.clear()
        wins_rate_text_info = get_wins_rate_and_limits_text_info(db)
        text = f'*Настройки побед и рейтинга*\n\n{wins_rate_text_info}'
        await msg.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                         reply_markup=get_wins_and_rate_buttons().as_markup())

    else:
        await msg.answer(f'Введите *число* или /cancel чтобы завершить', parse_mode=ParseMode.MARKDOWN_V2)
