from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_settings_buttons() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Токены 🔄", callback_data="change_tokens")
    builder.button(text="Ставки 💸", callback_data="change_bets")
    builder.button(text="Сервера 🎮", callback_data="change_servers")
    builder.button(text="Перекидывание ↩️", callback_data="perekid")
    builder.button(text="Победы 🏆 или рейтинг 🌟", callback_data="change_wins_and_rate")
    builder.button(text="<< Назад", callback_data="katch")
    builder.adjust(1)
    return builder
