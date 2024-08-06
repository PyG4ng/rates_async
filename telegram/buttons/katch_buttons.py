from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_katch_buttons() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Настройки ⚙️", callback_data="settings")
    builder.button(text="Запустить ✅", callback_data="start_table")
    builder.button(text="Остановить 🅾️", callback_data="stop_table")
    builder.button(text="Скорость 🚀", callback_data="speed")
    builder.button(text="Состояние столов 🧾", callback_data="get_status")
    builder.button(text="Получить баланс 💰", callback_data="check_balance")
    builder.button(text="Управление Аккаунтами 🧑‍💻", callback_data="manage_accounts")
    builder.button(text="Планировать ⌛️ Старт✅ Стоп🅾️", callback_data="planing")
    builder.button(text="<< Назад", callback_data="back_to_menu")
    builder.adjust(1)
    return builder


def get_back_to_katch_button() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="<< Назад", callback_data="katch")
    builder.adjust(1)
    return builder
