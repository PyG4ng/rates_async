import asyncio

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from katch.system import servers
from telegram.utilities import names
from databases.database import Database
from telegram.buttons.table_buttons import get_table_buttons
from telegram.utilities.special_characters import escape_all

servers_router = Router()


class Form(StatesGroup):
    change_servers_form = State()
    set_server_form = State()


@servers_router.callback_query(F.data == "change_servers")
async def servers_handler(call: CallbackQuery, state: FSMContext, db: Database):
    await state.set_state(Form.change_servers_form)
    text = f'*🎮 Использованные сервера*\n' \
           f'{await server_in_use(db)}\n' \
           f'_Введите цифру соответсвующая выбраному столу для замены сервера_'
    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=get_table_buttons().as_markup())


async def server_in_use(db: Database) -> str:
    game_servers = await servers.get_servers_async()
    server_names = game_servers[1]
    server_positions = db.get_all_servers()
    text = ''
    for table, server_position in server_positions:
        text += f'*{table}:* {escape_all(server_names[server_position])}\n'
    return text


async def available_servers_list(db: Database) -> str:
    servers_list = '__Список свободных серверов__\n'
    game_servers = await servers.get_servers_async()
    server_names = game_servers[1]
    server_positions = db.get_all_servers()
    already_in_use = [srv_pos[1] + 1 for srv_pos in server_positions]
    for index, server_name in enumerate(server_names, 1):
        if index in already_in_use:
            continue
        servers_list += f'*{index}*: {escape_all(server_name)}\n'
    return servers_list


@servers_router.callback_query(Form.change_servers_form, F.data.in_({'1', '2', '3', '4', '5'}))
async def change_table_servers(call: CallbackQuery, state: FSMContext, db: Database):
    table_to_change = int(call.data)
    await state.update_data(table=table_to_change)
    servers_list = await available_servers_list(db)
    text = f'*🎮 Меняем сервер стола {table_to_change}*\n' \
           f'{await server_in_use(db)}\n' \
           f'{servers_list}\n' \
           f'_Введите цифру соответсвующая выбраному серверу или /cancel чтобы завершить работу_'
    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(Form.set_server_form)


@servers_router.message(Form.set_server_form)
async def set_players_tokens(msg: Message, state: FSMContext, db: Database):
    new_server = msg.text

    data = await state.get_data()
    table = data.get('table')
    if new_server.isdigit() and int(new_server) in list(range(1, 15)):
        game_servers = await servers.get_servers_async()
        server_names = game_servers[1]
        server_positions = db.get_all_servers()
        already_in_use = [srv_pos[1] for srv_pos in server_positions]
        new_server = int(new_server)

        if new_server - 1 not in already_in_use:
            db.update_server(table_id=table, server=new_server - 1)
            text = f'*🎮✅ Новый сервер {names.NAMES_HELP.get(table)}: *{escape_all(server_names[new_server - 1])}'
            await msg.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)
            await asyncio.sleep(0.3)
            await state.set_state(Form.change_servers_form)
            text = f'*🎮 Использованные сервера*\n' \
                   f'{await server_in_use(db)}\n' \
                   f'_Введите цифру соответсвующая выбраному столу для замены сервера_'
            await msg.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2,
                             reply_markup=get_table_buttons().as_markup())
        else:
            text = f'*🎮 Настройка {names.NAMES_HELP.get(table)}*\n' \
                   f'Попытка выбрать сервер *{escape_all(server_names[new_server - 1])}*\n' \
                   f'*Этот сервер уже используется* ❗️\n' \
                   f'{await server_in_use(db)}\n' \
                   f'{await available_servers_list(db)}\n' \
                   f'_Введите цифру соответсвующая выбраному серверу или /cancel чтобы завершить работу_'
            await msg.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)
    else:
        text = f'*Неправильно выбран сервер ❗️*\n' \
               f'🎮 *Настройка {names.NAMES_HELP.get(table)}*\n' \
               f'{await server_in_use(db)}\n' \
               f'{await available_servers_list(db)}\n' \
               f'_Введите цифру соответсвующая выбраному серверу или /cancel чтобы завершить работу_'
        await msg.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)
