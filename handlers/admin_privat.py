from aiogram import Router, types
from aiogram.filters import Command

from buttons.reply import get_keyboard
from filters.chat_types import ChatTypeFilter, IsAdmin

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Изменить товар",
    "Удалисть товар",
    "Бездействие",
    placeholder="Выберите действие",
    sizes=(2, 1, 1),
)


@admin_router.message(Command("admin"))
async def admin(message: types.Message):
    await message.answer(f"Что хотите сделать?", reply_markup=ADMIN_KB)
