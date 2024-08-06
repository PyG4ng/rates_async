from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_account_management_buttons() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Купить премиум 🌟", callback_data="buy_prem")
    builder.button(text="Добавить в друзья ➕", callback_data="add_friend")
    builder.button(text="Принять заявку ✅", callback_data="accept_friend")
    builder.button(text="Удалить из друзей 🗑", callback_data="delete_friend")
    builder.button(text="Поиск по нику 🔍", callback_data="search_by_name")
    builder.button(text="Поиск по айди 🆔", callback_data="search_by_id")
    builder.button(text="Список друзей 📄", callback_data="friends_list")
    builder.button(text="Поменять ник 🧬", callback_data="change_name")
    builder.button(text="<< Назад", callback_data="katch")
    builder.adjust(1)
    return builder
