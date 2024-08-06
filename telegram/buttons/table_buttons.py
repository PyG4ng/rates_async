from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_table_buttons(all_button: bool = False, back_to_katch: bool = False) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="1", callback_data='1')
    builder.button(text="2", callback_data='2')
    builder.button(text="3", callback_data='3')
    builder.button(text="4", callback_data='4')
    builder.button(text="5", callback_data='5')
    if all_button is True:
        builder.button(text="Все столы", callback_data='all')
    back_to = "katch" if back_to_katch is True else "settings"
    builder.button(text="<< Назад", callback_data=back_to)
    builder.adjust(3, 2, 1, 1)
    return builder
