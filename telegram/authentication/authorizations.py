from telegram.utilities import tg_config


async def is_user_authorized(tg_user_id: int) -> bool:
    return True if tg_user_id in tg_config.AUTHORIZED_IDS else False
