from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_tokens_buttons(back_to_katch: bool = False) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Бот 🤖", callback_data='bot_token')
    builder.button(text="Клиент 🏃‍♂", callback_data='client_token')
    back_to = "katch" if back_to_katch is True else "settings"
    builder.button(text="<< Назад", callback_data=back_to)
    builder.adjust(1)
    return builder
