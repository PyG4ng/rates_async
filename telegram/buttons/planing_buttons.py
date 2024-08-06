from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_planing_buttons() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Запланировать Остановку 🅾️", callback_data="planing_stop_table")
    builder.button(text="Запланировать Запуск ✅", callback_data="planing_start_table")
    builder.button(text="Отключить", callback_data="stop_planing")
    builder.button(text="<< Назад", callback_data="katch")
    builder.adjust(1)
    return builder
