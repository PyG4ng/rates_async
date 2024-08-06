import asyncio

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from databases.database import Database
from telegram.utilities.special_characters import escape_all
from telegram.utilities.get_tokens import get_tokens_from_link
from telegram.buttons.phone_model_button import get_phone_model_buttons

get_tokens_router = Router()


class Form(StatesGroup):
    link_form = State()


@get_tokens_router.callback_query(F.data == "get_tokens")
async def tokens_handler(call: CallbackQuery):
    text = '*Получить токены по ссылке*'
    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=get_phone_model_buttons().as_markup())


@get_tokens_router.callback_query(F.data.in_({'iphone', 'android'}))
async def change_players_tokens(call: CallbackQuery, state: FSMContext):
    await state.update_data(system=call.data)
    await state.set_state(state=Form.link_form)
    await call.message.edit_text(text='*Введите ссылку: *', parse_mode=ParseMode.MARKDOWN_V2)


@get_tokens_router.message(Form.link_form)
async def set_players_tokens(msg: Message, state: FSMContext, db: Database):
    link = msg.text
    data = await state.get_data()
    system = data.get('system')
    result = get_tokens_from_link(system=system, link=link)
    if result:
        if result == 'session key not obtained':
            text = '*_Не получается подключиться к игре_*\n_Введите ссылку ещё раз или /cancel чтобы завершить_'
            await msg.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)
        elif result == 'no id_token bad link':
            text = '*_Ссылка неправильная_*\n_Введите ссылку ещё раз или /cancel чтобы завершить_'
            await msg.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)
        elif result == 'unknown error':
            text = '*_Неизвестная ошибка_*\n_Введите ссылку ещё раз или /cancel чтобы завершить_'
            await msg.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)
        else:
            for user in result:
                token = user.get('token')
                name = user.get('name')
                rid = user.get('rid')
                avatar = user.get('avatar') if user.get('avatar') else db.get_file_id(uid=1)
                text = f'*Токен:* `{escape_all(token)}`\n*Ник:* {escape_all(name)}\n*rid:* {escape_all(rid)}'
                await msg.answer_photo(photo=avatar, caption=text, parse_mode=ParseMode.MARKDOWN_V2)

            await state.clear()
    else:
        text = '*_Неизвестная ошибка_*\n_Введите ссылку ещё раз или /cancel чтобы завершить_'
        await msg.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)

    await asyncio.sleep(10)
    await msg.delete()
