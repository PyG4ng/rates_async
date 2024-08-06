from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_perekid_buttons() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Достижение побед 🏆", callback_data="activate_wins_perekid")
    builder.button(text="Достижение рейтинга 🌟", callback_data="activate_rate_perekid")
    builder.button(text="Кредиты (меньше 10к) 💰", callback_data="activate_points_perekid")
    builder.button(text="🅾️ Отключить автоперекидывание", callback_data="deactivate_auto_perekid")
    builder.button(text="Перекинуть определённую сумму", callback_data="manually_perekid")
    builder.button(text="<< Назад", callback_data="settings")
    builder.adjust(1)
    return builder
