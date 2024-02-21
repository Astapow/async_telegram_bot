from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_callback_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


select_language = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Українська", callback_data="ukrainian"),
            InlineKeyboardButton(text="Русский", callback_data="russian")
        ]
    ],
    resize_keyboard=True
)

menu_answers = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Работа с сайтом", callback_data="work_to_site")
        ],
        [
            InlineKeyboardButton(text="Рассылка всем пользователям(или только вам)", callback_data="send_massage")
        ],
        [
            InlineKeyboardButton(text="Информация про пользателя", callback_data="info_to_user")
        ],
        [
            InlineKeyboardButton(text="Работа с таблицами", callback_data="work_to_table")
        ],
        [
            InlineKeyboardButton(text="Анализ сообщения", callback_data="analiz")
        ],
        [
            InlineKeyboardButton(text="Получить информацию из гугл таблици", callback_data="get_info_google")
        ],
        [
            InlineKeyboardButton(text="Особые возможности", callback_data="special_options")
        ]
    ],
    resize_keyboard=True
)

btn_form = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Заполнить форму", callback_data="create_form")]
    ]
)
