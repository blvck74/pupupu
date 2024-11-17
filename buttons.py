from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Основное меню
main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить текст")],
        [KeyboardButton(text="Удалить текст")],
        [KeyboardButton(text="Посмотреть текст")],
        [KeyboardButton(text="Сравнить текст")]
    ],
    resize_keyboard=True
)

# Меню для добавления текста
add_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Раздел 1"), KeyboardButton(text="Раздел 2")],
        [KeyboardButton(text="Раздел 3"), KeyboardButton(text="Раздел 4")],
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True
)

# Меню для удаления текста
delete_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Раздел 1"), KeyboardButton(text="Раздел 2")],
        [KeyboardButton(text="Раздел 3"), KeyboardButton(text="Раздел 4")],
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True
)

# Меню для просмотра текста
view_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Раздел 1"), KeyboardButton(text="Раздел 2")],
        [KeyboardButton(text="Раздел 3"), KeyboardButton(text="Раздел 4")],
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True
)

# Меню для сравнения текста
compare_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Раздел 1"), KeyboardButton(text="Раздел 2")],
        [KeyboardButton(text="Раздел 3"), KeyboardButton(text="Раздел 4")],
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True
)
