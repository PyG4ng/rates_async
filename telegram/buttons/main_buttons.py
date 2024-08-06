from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_buttons() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text='Прокачка ✨', callback_data="katch")
    builder.button(text="Получить токен 💻", callback_data="get_tokens")
    builder.button(text="Перенести аккаунты 📲", callback_data="perenos")
    builder.button(text=" ❌ Закрыть меню", callback_data="close_menu")
    builder.adjust(1)
    return builder
