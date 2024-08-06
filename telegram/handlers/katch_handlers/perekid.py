import asyncio

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from databases.database import Database
from telegram.utilities.special_characters import frmt
from telegram.buttons.perekid_buttons import get_perekid_buttons

perekid_router = Router()


class Form(StatesGroup):
    set_perekid_credits = State()


def perekid_text_info(db: Database):
    auto_perekid_by_1 = ''
    auto_perekid_by_2 = ''
    auto_perekid_by_3 = ''
    if db.is_auto_perekid():
        auto_state = 'Включено ✅'
        if db.is_perekid_by_points():
            auto_perekid_by_1 = '\n_● Если баланс бота меньше 10к_ 💰'
        if db.is_perekid_by_wins():
            auto_perekid_by_2 = '\n_● По достижению количества побед_ 🏆'
        if db.is_perekid_by_rate():
            auto_perekid_by_3 = '\n_● По достижению нужнего рейтинга_ 🌟'
    else:
        auto_state = 'Отключено 🅾️'
    text = f'\n\n_*Автоперекидывание:*_ {auto_state}{auto_perekid_by_1}{auto_perekid_by_2}{auto_perekid_by_3}'
    return text


@perekid_router.callback_query(F.data == "perekid")
async def perekid_handler(call: CallbackQuery, db: Database):
    text = f'*Настройки перекидывания*{perekid_text_info(db)}'
    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=get_perekid_buttons().as_markup())


CALLBACK_RESPONSES = {"activate_points_perekid",
                      "activate_wins_perekid",
                      "activate_rate_perekid",
                      "deactivate_auto_perekid",
                      "manually_perekid"}


@perekid_router.callback_query(F.data.in_(CALLBACK_RESPONSES))
async def perekid_handler(call: CallbackQuery, state: FSMContext, db: Database):
    if call.data == "activate_points_perekid":
        status = False if db.is_perekid_by_points() else True
        db.change_perekid_by_points(val=status)
        if db.is_perekid_by_wins() or db.is_perekid_by_points() or db.is_perekid_by_rate():
            db.change_auto_perekid(val=True)
        else:
            db.change_auto_perekid(val=False)

    if call.data == "activate_wins_perekid":
        status = False if db.is_perekid_by_wins() else True
        db.change_perekid_by_wins(val=status)
        if status is True:
            db.change_perekid_by_rate(val=False)
            db.update_parameters(param='is_rate_limited', value=0)

        if db.is_perekid_by_wins() or db.is_perekid_by_points() or db.is_perekid_by_rate():
            db.change_auto_perekid(val=True)
        else:
            db.change_auto_perekid(val=False)

    if call.data == "activate_rate_perekid":
        status = False if db.is_perekid_by_rate() else True
        db.change_perekid_by_rate(val=status)
        if status is True:
            db.change_perekid_by_wins(val=False)
            db.update_parameters(param='are_wins_limited', value=0)

        if db.is_perekid_by_wins() or db.is_perekid_by_points() or db.is_perekid_by_rate():
            db.change_auto_perekid(val=True)
        else:
            db.change_auto_perekid(val=False)

    if call.data == "deactivate_auto_perekid":
        db.change_auto_perekid(val=False)
        db.change_perekid_by_wins(val=False)
        db.change_perekid_by_rate(val=False)
        db.change_perekid_by_points(val=False)

    if call.data == "manually_perekid":
        await call.message.answer(text='*Введите Количество кредитов которое надо перекинуть: *',
                                  parse_mode=ParseMode.MARKDOWN_V2)
        await state.set_state(Form.set_perekid_credits)
        await call.message.delete()
        return

    text = f'*Настройки перекидывания*{perekid_text_info(db)}'
    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=get_perekid_buttons().as_markup())


@perekid_router.message(Form.set_perekid_credits)
async def set_credits_to_get(msg: Message, state: FSMContext, db: Database):
    credits_to_perekid = msg.text
    if " " in credits_to_perekid:
        credits_to_perekid = ''.join(credits_to_perekid.split(" "))
    if credits_to_perekid.isdigit():
        db.change_how_much_to_perekid(int(credits_to_perekid))
        db.change_all_table_status('OSTANOVIT')
        await asyncio.sleep(1)
        db.change_auto_perekid(val=False)
        db.change_perekid_by_wins(val=False)
        db.change_perekid_by_rate(val=False)
        db.change_perekid_by_points(val=False)
        db.change_stol_perekid_state(val='ON')
        text = f'*Автоперекидывание отключено*\n*Запускаю перекидывание на :* {frmt(int(credits_to_perekid))}'
        await msg.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)
        await state.clear()
        # text = f'*Настройки перекидывания*{perekid_text_info(db)}'
        # await msg.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2,
        #                  reply_markup=get_perekid_buttons().as_markup())
    else:
        await msg.answer('Введите *число* или /cancel чтобы завершить', parse_mode=ParseMode.MARKDOWN_V2)
