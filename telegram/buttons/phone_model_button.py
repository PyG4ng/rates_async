from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_phone_model_buttons() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Айфон 🍎", callback_data="iphone")
    builder.button(text="Андроид 📱", callback_data="android")
    builder.button(text="<< Назад", callback_data="back_to_menu")
    builder.adjust(1)
    return builder
