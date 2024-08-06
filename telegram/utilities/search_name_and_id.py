from typing import Optional

import aiohttp
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, FSInputFile
from loguru import logger

from configs import config
from databases.database import Database
from katch.system.api_async import DurakAsync
from telegram.utilities.get_credits import get_rang_color, get_angle_mak
from telegram.utilities.special_characters import frmt, escape_all


async def search_by_name(msg: Message, user_account: DurakAsync, db: Database):
    nick = msg.text
    m2 = await msg.answer(text='Выполняю посик...')
    search_result = await user_account.search_username(nick)
    await m2.delete()
    if search_result:
        await parse_name_result(search_result, msg, db)
    else:
        await msg.answer(text='*Нет результатов*', parse_mode=ParseMode.MARKDOWN_V2)


def parse_user_caption(user_id: int, user_name: str, user_score: int, pw: int) -> str:
    text = f'🆔: `{user_id}`\n' \
           f'👤: `{escape_all(user_name)}`\n' \
           f'✨: {frmt(user_score)}\n' \
           f'{get_rang_color(user_score)}: {get_angle_mak(user_score)}\n' \
           f'📶: {pw}'
    return text


async def download_picture(url: str, filename: str, db: Database) -> Optional[str]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.read()
                    with open(filename, 'wb') as f:
                        f.write(data)
                else:
                    logger.info(f"Error downloading picture {url}: {response.status}")
                    return db.get_file_id(uid=1)
        except Exception as e:
            logger.info(f"Error downloading picture {url}: {e}")
            return db.get_file_id(uid=1)


async def parse_name_result(search_result: dict, msg: Message, db: Database) -> None:
    all_users = search_result.get('users')
    group_by_10_users = [all_users[x:x + 10] for x in range(0, len(all_users), 10)]
    for users in group_by_10_users:
        media = []
        for user in users:
            user_id = user.get('id')
            avatar = user.get('avatar') if user.get('avatar') else db.get_file_id(uid=1)
            name = user.get('name')
            score = user.get('score')
            pw = user.get('pw')
            text = parse_user_caption(user_id=user_id, user_name=name, user_score=score, pw=pw)
            media.append(types.InputMediaPhoto(media=avatar, caption=text, parse_mode=ParseMode.MARKDOWN_V2))
        try:
            await msg.answer_media_group(media=media)
        except TelegramBadRequest as e:
            error_message = str(e)
            logger.info(f"Exception caught: {error_message}")

            if "WEBPAGE_MEDIA_EMPTY" in error_message or "Wrong file" in error_message:
                media, file_names = [], []
                for user in users:
                    user_id = user.get('id')
                    avatar = user.get('avatar')
                    filename = config.ROOT_FOLDER / f'telegram/utilities/{user_id}_{msg.from_user.id}.jpg'
                    dwn_result = await download_picture(url=avatar, filename=filename, db=db)
                    photo = dwn_result
                    if dwn_result is None:
                        file_names.append(filename)
                        photo = FSInputFile(filename)
                    name = user.get('name')
                    score = user.get('score')
                    pw = user.get('pw')
                    text = parse_user_caption(user_id=user_id, user_name=name, user_score=score, pw=pw)
                    media.append(types.InputMediaPhoto(media=photo, caption=text, parse_mode=ParseMode.MARKDOWN_V2))
                await msg.answer_media_group(media=media)
                for filename in file_names:
                    try:
                        filename.unlink()
                    except OSError as e:
                        logger.info(f'OSError while deleting: {filename} - {e}')
                        pass


async def search_by_id(msg: Message, user_account: DurakAsync, db: Database):
    user_id_to_search = msg.text
    if not user_id_to_search.isdigit():
        await msg.answer(text='❌: 🆔 состоит только из чисел!')
        return
    m2 = await msg.answer(text='Выполняю посик...')
    user = await user_account.get_user_info(int(user_id_to_search))
    await m2.delete()
    if user:
        await parse_user_id_result(user=user, msg=msg, db=db)
    else:
        await msg.answer(text='*Нет результатов*', parse_mode=ParseMode.MARKDOWN_V2)


async def parse_user_id_result(user: dict, msg: Message, db: Database) -> None:
    user_id = user.get('id')
    avatar = user.get('avatar') if user.get('avatar') else db.get_file_id(uid=1)
    name = user.get('name').replace("\\", "\\\\")
    score = user.get('score')
    pw = user.get('pw')
    text = parse_user_caption(user_id=user_id, user_name=name, user_score=score, pw=pw)
    try:
        await msg.answer_photo(photo=avatar, caption=text, parse_mode=ParseMode.MARKDOWN_V2)
    except TelegramBadRequest as e:
        if str(e) == 'Telegram server says - Bad Request: wrong file identifier/HTTP URL specified':
            filename = config.ROOT_FOLDER / f'telegram/utilities/{user_id}_{msg.from_user.id}.jpg'
            dwn_result = await download_picture(url=avatar, filename=filename, db=db)
            file = FSInputFile(filename) if dwn_result is None else db.get_file_id(uid=1)
            await msg.answer_photo(photo=file, caption=text, parse_mode=ParseMode.MARKDOWN_V2)
            if dwn_result is None:
                try:
                    filename.unlink()
                except OSError as e:
                    logger.info(f'OSError while deleting: {filename} - {e}')
                    pass
