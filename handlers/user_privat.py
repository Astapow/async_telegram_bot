import asyncio

from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from buttons import reply, inline
from buttons.reply import get_keyboard
from connect_table.connect_to_google_table import (
    add_message_to_sheet_async,
    get_info_from_sheet_async,
)

user_private_router = Router()

LANGUAGE_UA = "ukrainian"
LANGUAGE_RU = "russian"


class ChangeLanguage(StatesGroup):
    language = State()


@user_private_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(
        "Приветствуем вас в боте, который представляет часть из доступных функций телеграмм. Выберите язык:",
        reply_markup=inline.select_language,
    )


@user_private_router.callback_query(F.data == LANGUAGE_UA)
async def step1_check(callback: CallbackQuery):
    await callback.message.answer(
        "Обрано <b>Українську</b> мову. \n\n"
        "Натисніть кнопку <b>Головне меню</b>, щоб перейти до головного меню.\n\n",
        reply_markup=reply.get_keyboard(
            "Головне Меню",
            sizes=(
                1,
                1,
            ),
        ),
    )


@user_private_router.callback_query(F.data == LANGUAGE_RU)
async def step1_check(callback: CallbackQuery):
    await callback.message.answer(
        "Выбран язык <b>Русский</b>.\n\n"
        "Нажмите кнопку <b>Главное меню</b>, чтобы перейти в головное меню.",
        reply_markup=reply.get_keyboard(
            "Главное меню",
            sizes=(
                1,
                1,
            ),
        ),
    )


class Form(StatesGroup):
    time_await = State()


@user_private_router.message(Command("menu"))
async def menu_command(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.time_await)
    await message.answer(
        "Отправьте мне время (в секундах 1-60) через которое мне отправить вам сообщение:",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@user_private_router.message(Form.time_await, F.text)
async def filters_text(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.time_await)
    await state.update_data(time_await=message.text)
    data = await state.get_data()
    time_await = int(data["time_await"])
    await asyncio.sleep(time_await)
    await message.answer(
        f"Прошло <b>{time_await}</b> секунд. Ваше сообщение:",
        reply_markup=get_keyboard("Главное меню", sizes=(1, 1)),
    )
    await state.clear()


@user_private_router.message(Form.time_await)
async def filters_text(message: types.Message, state: FSMContext) -> None:
    await message.answer("Вы ввели некоректные данные, отправьте цифру от 1 до 60")
    await state.clear()


@user_private_router.message(F.text == "Главное меню")
async def main_menu(message: types.Message, state: FSMContext) -> None:
    await message.answer("Главное меню", reply_markup=inline.menu_answers)


@user_private_router.callback_query(F.data == "work_to_site")
async def work_to_site(callback: CallbackQuery):
    await callback.message.answer(
        "Нажмите на кнопку ниже, и заполните форму", reply_markup=inline.btn_form
    )


class UserAction(StatesGroup):
    waiting_for_user_message = State()


@user_private_router.callback_query(F.data == "send_massage")
async def send_msg(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Отправьте мне сообщение, которое вы хотите отправить. "
        "Бот может обрабатывать любые сообщения (файлы, фотографии, видео, геолокацию, контакты и т.д.)."
    )
    await state.set_state(UserAction.waiting_for_user_message)


@user_private_router.message(
    UserAction.waiting_for_user_message,
    or_f(
        F.text
        | F.photo
        | F.video
        | F.document
        | F.location
        | F.contact
        | F.voice
        | F.audio
    ),
)
async def user_message_received(message: types.Message, state: FSMContext):
    await message.forward(message.chat.id)

    message_type = message.content_type
    await message.answer(f"Тип полученного сообщения: {message_type.capitalize()}")

    await state.clear()


@user_private_router.callback_query(F.data == "info_to_user")
async def info_user(callback: CallbackQuery):
    await callback.message.answer(
        "Вся информация про вас, которая доступна мне:\n"
        f"id: {callback.from_user.id}\n"
        f"first_name: {callback.from_user.first_name}\n"
        f"last_name: {callback.from_user.last_name}\n"
        f"username: {callback.from_user.username}\n"
        f"language_code: {callback.from_user.language_code}\n"
        f"is_premium: {callback.from_user.is_premium}\n"
        f"added_to_attachment_menu: {callback.from_user.added_to_attachment_menu}\n"
        f"can_join_groups: {callback.from_user.can_join_groups}"
        f"can_read_all_group_messages: {callback.from_user.can_read_all_group_messages}\n"
        f"supports_inline_queries: {callback.from_user.supports_inline_queries}\n"
    )


class EditMessageToTable(StatesGroup):
    message_text = State()



@user_private_router.callback_query(F.data == "work_to_table")
async def connect_google_table(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Напишите мне любое сообщение, которое я добавлю в таблицу."
    )
    await state.set_state(EditMessageToTable.message_text)


@user_private_router.message(EditMessageToTable.message_text, F.text)
async def message_input_handler(message: Message, state: FSMContext):
    new_id = await add_message_to_sheet_async(message.text)
    if new_id:
        await message.answer(
            f"Я внес это сообщение в таблицу под номером #{new_id}\n"
            "Таблица:\n"
            "https://docs.google.com/spreadsheets/d/1j8KGRO5Hv8z29IEOMhrg6RIG-ZUEoGZUwQe0RLVbhaE/edit#gid=0"
        )
    else:
        await message.answer("Произошла ошибка при добавлении сообщения в таблицу.")
    await state.clear()


class ReplyMessage(StatesGroup):
    callback_msg = State()


@user_private_router.callback_query(F.data == "analiz")
async def scan_message_text(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Скиньте мне сообщение любого типа данных: текст, фото-файл, аудио-файл, видео-файл, голосовое сообщение, .pdf."
    )
    await state.set_state(ReplyMessage.callback_msg)


@user_private_router.message(
    ReplyMessage.callback_msg,
    or_f(
        F.text
        | F.photo
        | F.video
        | F.document
        | F.location
        | F.contact
        | F.voice
        | F.audio
    ),
)
async def any_message_input_handler(message: Message, state: FSMContext):
    if message.text:
        await message.reply(message.text)

    elif message.photo:
        await message.answer_photo(message.photo[-1].file_id, caption="Вот ваше фото")

    elif message.audio:
        await message.answer_audio(message.audio.file_id, caption="Вот ваше аудио")

    elif message.video:
        await message.answer_video(message.video.file_id, caption="Вот ваше видео")

    elif message.voice:
        await message.answer_voice(
            message.voice.file_id, caption="Вот ваше голосовое сообщение"
        )
    elif message.document:
        await message.answer_document(
            message.document.file_id, caption="Вот ваш документ"
        )
    else:
        # Для других типов сообщений
        await message.answer("Этот тип сообщений я пока не умею обрабатывать.")

    await state.clear()


@user_private_router.callback_query(F.data == "get_info_google")
async def get_info_google(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Получаю информацию из таблицы...")
    data = await get_info_from_sheet_async()
    if data:
        response = "Данные из таблицы:\n\n"
        for row in data:
            response += ", ".join(row) + "\n"
        await callback.message.answer(
            response[:4096]
        )
    else:
        await callback.message.answer("Не удалось получить данные из таблицы.")
    await state.clear()


@user_private_router.callback_query(F.data == "special_options")
async def special_options(callback: CallbackQuery, state: FSMContext):
    await state.set_state("special_options")
    await callback.message.answer("<strong>Я могу вот так</strong>")
    await callback.message.answer("<b>Или так</b>")
    await callback.message.answer("<u>Или вот так</u>")
    await state.clear()
