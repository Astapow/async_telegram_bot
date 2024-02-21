import asyncio
import logging
import os
import sys

from aiogram.enums import ParseMode
from aiogram.types import BotCommandScopeAllPrivateChats
from dotenv import load_dotenv
from aiogram import Dispatcher, Bot

from common.bot_commands_list import private
from handlers.admin_privat import admin_router
from handlers.user_privat import user_private_router

load_dotenv()

dp = Dispatcher()
dp.include_router(user_private_router)
dp.include_router(admin_router)

ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query']


async def main() -> None:
    bot = Bot(os.environ["BOT_TOKEN"], parse_mode=ParseMode.HTML)
    bot.my_admins_list = []
    await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
