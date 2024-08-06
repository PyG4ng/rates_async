from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_wins_and_rate_buttons() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Обнулить счётчик побед и кредитов", callback_data="reset_wins_count")
    builder.button(text="Включить/Отключить ограничение побед 🏆", callback_data="activate_deactivate_wins_limit")
    builder.button(text="Настроить количество побед 🏆", callback_data="set_wins_limit")
    builder.button(text="Включить/Отключить ограничение рейтинга 🌟", callback_data="activate_deactivate_rate_limit")
    builder.button(text="Настроить рейтинг стоп 🌟", callback_data="set_rate_limit")
    builder.button(text="<< Назад", callback_data="settings")
    builder.adjust(1)
    return builder
