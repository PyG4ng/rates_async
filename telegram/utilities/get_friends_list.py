import os

from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from katch.system.api_async import DurakAsync
from telegram.utilities.special_characters import escape_all


async def get_friend_list(call: CallbackQuery, user_account: DurakAsync):
    m1 = await call.message.answer(text=f'*Получаю список друзей {escape_all("...")}*',
                                   parse_mode=ParseMode.MARKDOWN_V2)
    friend_list = await user_account.get_friends_list()
    await m1.delete()
    if isinstance(friend_list, list):
        if friend_list:
            grouped_result = {}
            number_of_friends_to_display = 10
            for user in friend_list[:number_of_friends_to_display]:
                user_id = user.get('user').get('id')
                user_kind = user.get('kind')
                if user_id in grouped_result:
                    grouped_result.get(user_id).get('kind').append(user_kind)
                else:
                    grouped_result[user_id] = {'kind': [user_kind], 'name': user.get('user').get('name'),
                                               'avatar': user.get('user').get('avatar')}
            for user in grouped_result:
                user_id = user
                name = grouped_result.get(user).get('name')
                status = 'Друг' if 'FRIEND' in grouped_result.get(user).get('kind') else 'Запрос'
                avatar = grouped_result.get(user).get('avatar') if grouped_result.get(user).get(
                    'avatar') else os.getenv('AVATAR')
                text = f'*ID:*  `{user_id}`\n*Ник:*  `{escape_all(name)}`\n*{status}*'
                await call.message.answer_photo(photo=avatar, caption=text, parse_mode=ParseMode.MARKDOWN_V2)
        else:
            text = '*Нет Друзей*'
            await call.message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)
    else:
        text = '*Ошибка при попытки получить список друзей*'
        await call.message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)
