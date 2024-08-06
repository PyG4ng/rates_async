import random
from datetime import datetime, timedelta

from katch.system import servers
from databases.database import Database
from katch.system.api_async import DurakAsync
from telegram.utilities.special_characters import escape_all, frmt


async def get_balance(db: Database):
    client_data = {}
    bot_data = {}
    server_positions = db.get_all_servers()
    already_in_use = [srv_pos[1] for srv_pos in server_positions]
    available = [el for el in range(1, 14) if el not in already_in_use]
    client_token = db.get_token('CLIENT_TOKEN')
    bot_token = db.get_token('BOT_TOKEN')
    game_servers = await servers.get_servers_async()
    client_server = game_servers[0][random.choice(available)]
    bot_server = game_servers[0][random.choice(available)]
    client = DurakAsync(server=client_server, token=client_token)
    bot = DurakAsync(server=bot_server, token=bot_token)
    try:
        await client.connect()
    except Exception:
        ...
    else:
        client_data = {'client_name': client.user.name,
                       'client_credits': client.user.points,
                       'client_coins': client.user.coins,
                       'client_rate': client.user.rate,
                       'client_rate_total': client.user.rate_total,
                       'client_user_id': client.user.user_id,
                       'client_premium': client.user.premium
                       }
    try:
        await bot.connect()
    except Exception:
        ...
    else:
        bot_data = {'bot_name': bot.user.name,
                    'bot_credits': bot.user.points,
                    'bot_coins': bot.user.coins,
                    'bot_rate': bot.user.rate,
                    'bot_rate_total': bot.user.rate_total,
                    'bot_user_id': bot.user.user_id,
                    'bot_premium': bot.user.premium
                    }
    return client_data, bot_data


def get_rang_color(rang: int) -> str:
    rang_color = ''
    if rang in range(0, 160_000):
        rang_color = '⬜️'
    elif rang in range(160_000, 320_000):
        rang_color = '🟨'
    elif rang in range(320_000, 480_000):
        rang_color = '🟥'
    elif rang in range(480_000, 640_000):
        rang_color = '🟩'
    elif rang in range(640_000, 800_000):
        rang_color = '🟦'
    elif rang in range(800_000, 960_000):
        rang_color = '🟪'
    elif rang >= 960_000:
        rang_color = '🟪♾'
    return rang_color


def get_angle_mak(user_score: int) -> str:
    angle_mark = 0
    rate = str(user_score)
    if len(rate) < 3:
        angle_mark = 0
    if len(rate) == 3:
        angle_mark = rate[0]
    elif len(rate) >= 4:
        if rate[-4] == '0':
            angle_mark = rate[-3]
        else:
            angle_mark = f'{rate[-4]}{rate[-3]}'

    if user_score >= 960_000:
        angle_mark = "♾"

    return angle_mark


def remain_prem(object_time):
    datetime_object = datetime.strptime(object_time, '%Y-%m-%dT%H:%M:%S.%fZ')
    text = '0д. 0ч. 0м. 0с.'
    if datetime_object >= datetime.utcnow():
        remaining_premium = datetime_object - datetime.utcnow()
        t = str(timedelta(seconds=remaining_premium.seconds))
        tt = t.split(':')
        text = f'{remaining_premium.days}д. {tt[0]}ч. {tt[1]}м. {tt[2]}с.'
    return text


async def form_balance(db: Database) -> str:
    text = '*Баланс*\n\n'
    client_data, bot_data = await get_balance(db=db)
    if bot_data:
        text += f"*Бот 🤖*\n" \
                f"*Ник:* `{escape_all(bot_data.get('bot_name'))}`\n" \
                f"*Кредиты:* {frmt(bot_data.get('bot_credits'))}\n" \
                f"*Монеты:* {frmt(bot_data.get('bot_coins'))}\n" \
                f"*Айди:* `{bot_data.get('bot_user_id')}`\n" \
                f"*Рейтинг:*  {frmt(bot_data.get('bot_rate'))} \| {frmt(bot_data.get('bot_rate_total'))} 🌟 " \
                f"{get_rang_color(bot_data.get('bot_rate_total'))}\n" \
                f"*Премиум:* {escape_all(remain_prem(bot_data.get('bot_premium')))}\n\n"
    if client_data:
        text += f"*Клиент 🏃‍♂*\n" \
                f"*Ник:* `{escape_all(client_data.get('client_name'))}`\n" \
                f"*Кредиты:* {frmt(client_data.get('client_credits'))}\n" \
                f"*Монеты:* {frmt(client_data.get('client_coins'))}\n" \
                f"*Айди:* `{client_data.get('client_user_id')}`\n" \
                f"*Рейтинг:*  {frmt(client_data.get('client_rate'))} \| {frmt(client_data.get('client_rate_total'))} 🌟" \
                f"{get_rang_color(client_data.get('client_rate_total'))}\n" \
                f"*Премиум:* {escape_all(remain_prem(client_data.get('client_premium')))}"
    return text


def get_user_data(user) -> str:
    user_data = {'user_name': user.user.name,
                 'user_credits': user.user.points,
                 'user_coins': user.user.coins,
                 'user_rate': user.user.rate,
                 'user_rate_total': user.user.rate_total,
                 'user_user_id': user.user.user_id,
                 'user_premium': user.user.premium
                 }
    text = f"*Ник:* `{escape_all(user_data.get('user_name'))}`\n" \
           f"*Кредиты:* {frmt(user_data.get('user_credits'))}\n" \
           f"*Монеты:* *{frmt(user_data.get('user_coins'))}*\n" \
           f"*Айди:* `{user_data.get('user_user_id')}`\n" \
           f"*Рейтинг:*  {frmt(user_data.get('user_rate'))} \| {frmt(user_data.get('user_rate_total'))} 🌟" \
           f"{get_rang_color(user_data.get('user_rate_total'))}\n" \
           f"*Премиум:* {escape_all(remain_prem(user_data.get('user_premium')))}"
    return text
