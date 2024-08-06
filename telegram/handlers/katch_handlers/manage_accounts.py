import random

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from katch.system import servers
from katch.system.api_async import DurakAsync
from telegram.buttons.acc_management_buttons import get_account_management_buttons
from telegram.buttons.tokens_buttons import get_tokens_buttons
from databases.database import Database
from telegram.utilities.get_credits import get_user_data
from telegram.utilities.get_friends_list import get_friend_list
from telegram.utilities.search_name_and_id import search_by_name, search_by_id

manage_account_router = Router()


class Form(StatesGroup):
    choose_management_account_form = State()
    manage_account_form = State()


@manage_account_router.callback_query(F.data == "manage_accounts")
async def manage_account_handler(call: CallbackQuery, state: FSMContext):
    await state.set_state(Form.choose_management_account_form)
    await call.message.edit_text(text='Управление аккаунтом', parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=get_tokens_buttons(back_to_katch=True).as_markup())


@manage_account_router.callback_query(Form.choose_management_account_form, F.data.in_({'bot_token', 'client_token'}))
async def account_connection(call: CallbackQuery, state: FSMContext, db: Database):
    user_token = db.get_token(call.data.upper())
    server_positions = db.get_all_servers()
    already_in_use = [srv_pos[1] for srv_pos in server_positions]
    available = [el for el in range(1, 14) if el not in already_in_use]
    chosen_server_position = random.choice(available)
    game_servers = await servers.get_servers_async()
    user_server = game_servers[0][chosen_server_position]
    user_account = DurakAsync(server=user_server, token=user_token)
    try:
        await user_account.connect()
    except PermissionError as err:
        print(err)
        err_msg = f'Пользователь скорее всего забанен! 🚫 \n{user_token}'
        await call.message.answer(err_msg)
        return
    except ValueError:
        game_servers = await servers.get_servers_async()
        err_msg = f'Подключение к серверу {game_servers[1][chosen_server_position]} не удалось ‼️ \n'
        await call.message.answer(err_msg)
        return
    else:
        await state.update_data(user_account=user_account)
        text = get_user_data(user_account)
        await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                                     reply_markup=get_account_management_buttons().as_markup())


CALLBACK_RESPONSES = {
    'buy_prem',
    'add_friend',
    'accept_friend',
    'delete_friend',
    'search_by_name',
    'search_by_id',
    'change_name',
    'friends_list'
}


@manage_account_router.callback_query(F.data.in_(CALLBACK_RESPONSES))
async def account_connection(call: CallbackQuery, state: FSMContext):
    if call.data == 'friends_list':
        data = await state.get_data()
        user_account = data.get("user_account")
        await get_friend_list(call, user_account)
        text = get_user_data(user_account)
        await call.message.delete()
        await call.message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                                  reply_markup=get_account_management_buttons().as_markup())
        return

    text = 'Ошибка'
    await state.update_data(action=call.data)

    if call.data in ['add_friend', 'accept_friend', 'delete_friend', 'search_by_id']:
        text = '*Введите айди игрока*'

    elif call.data == 'buy_prem':
        text = "*1\.* 10 монет \| 1 день\n*2\.* 28 монет \| 3 д\.\n*3\.* 60 монет \| 7 д\.\n*4\.* 250 монет \| 30 д\.\n" \
               "*5\.* 720 монет \| 90 д\.\n*6\.* 2700 монет \| 365 д\.\n\n" \
               "*Введите число \(от 1 до 6\)*"

    elif call.data in ['search_by_name', 'change_name']:
        text = '*Введите ник:*'

    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(state=Form.manage_account_form)


@manage_account_router.message(Form.manage_account_form)
async def management_actions(msg: Message, state: FSMContext, db: Database):
    input_text = msg.text
    data = await state.get_data()
    action = data.get('action')
    user_account = data.get("user_account")

    if action == 'buy_prem':
        if input_text.isdigit() and int(input_text) in [1, 2, 3, 4, 5, 6]:
            # await user_account.buy_prem(int(input_text) - 1)
            print(f'Buying premium for {int(input_text) - 1}')
            await msg.answer(text='*Готово✔️*', parse_mode=ParseMode.MARKDOWN_V2)

    if action == 'search_by_name':
        await search_by_name(msg, user_account, db)

    if action == 'change_name':
        await user_account.update_nick_name(nick_name=input_text)
        await msg.answer(text='*Готово✔️*', parse_mode=ParseMode.MARKDOWN_V2)

    if action == 'add_friend':
        if input_text.isdigit():
            await user_account.add_friend(user_id=int(input_text))
            await msg.answer(text='*Готово✔️*', parse_mode=ParseMode.MARKDOWN_V2)
        else:
            await msg.answer(text='❌: 🆔 состоит только из чисел!')

    if action == 'accept_friend':
        if input_text.isdigit():
            await user_account.accept_friend(user_id=int(input_text))
            await msg.answer(text='*Готово✔️*', parse_mode=ParseMode.MARKDOWN_V2)
        else:
            await msg.answer(text='❌: 🆔 состоит только из чисел!')

    if action == 'delete_friend':
        if input_text.isdigit():
            await user_account.delete_friend(user_id=int(input_text))
            await msg.answer(text='*Готово✔️*', parse_mode=ParseMode.MARKDOWN_V2)
        else:
            await msg.answer(text='❌: 🆔 состоит только из чисел!')

    if action == 'search_by_id':
        await search_by_id(msg, user_account, db)

    text = get_user_data(user_account)
    await msg.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                     reply_markup=get_account_management_buttons().as_markup())
