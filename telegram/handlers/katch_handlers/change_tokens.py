from typing import Literal

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from databases.database import Database
from telegram.buttons.tokens_buttons import get_tokens_buttons
from telegram.utilities import names
from telegram.utilities.special_characters import escape_all, is_token_valid

tokens_router = Router()


class Form(StatesGroup):
    change_tokens_form = State()
    chose_token_to_change_from = State()


@tokens_router.callback_query(F.data == "change_tokens")
async def tokens_handler(call: CallbackQuery, state: FSMContext, db: Database):
    text = get_all_tokens(db)
    await state.set_state(state=Form.chose_token_to_change_from)
    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=get_tokens_buttons().as_markup())


def get_all_tokens(db: Database) -> str:
    text = '*Токены*\n'
    bot_token = db.get_token(player='BOT_TOKEN')
    client_token = db.get_token(player='CLIENT_TOKEN')
    text += f'*Бот 🤖:*  `{escape_all(bot_token)}`\n*Клиент 🏃‍♂:*  `{escape_all(client_token)}`'
    return text


@tokens_router.callback_query(Form.chose_token_to_change_from, F.data.in_({"bot_token", "client_token"}))
async def change_players_tokens(call: CallbackQuery, state: FSMContext):
    player = 'bot' if call.data == 'bot_token' else 'client'
    await state.update_data(player=player)
    text = f'*Введите токен {names.NAMES_HELP.get(player)}: *'
    await call.message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(Form.change_tokens_form)
    await call.message.delete()


@tokens_router.message(Form.change_tokens_form)
async def set_players_tokens(msg: Message, state: FSMContext, db: Database):
    new_token = msg.text
    data = await state.get_data()
    player: Literal['bot', 'client'] = data.get('player')
    if is_token_valid(new_token):
        player_token = 'BOT_TOKEN' if player == 'bot' else 'CLIENT_TOKEN'
        db.update_token(player_token=player_token, tkn=new_token)
        text = f'*Новый токен {names.NAMES_HELP.get(player)}:* \n{escape_all(new_token)}'
        await msg.answer(text, parse_mode=ParseMode.MARKDOWN_V2)
        players_tokens = get_all_tokens(db)
        await msg.answer(text=players_tokens, parse_mode=ParseMode.MARKDOWN_V2,
                         reply_markup=get_tokens_buttons().as_markup())
        await state.set_state(state=Form.chose_token_to_change_from)
    else:
        text = f'*Неправильный формат токена {names.NAMES_HELP.get(player)}:* \n{escape_all(new_token)}\n' \
               f'Попробуйте ещё раз или /cancel чтобы завершить'
        await msg.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)
        await state.set_state(Form.change_tokens_form)
