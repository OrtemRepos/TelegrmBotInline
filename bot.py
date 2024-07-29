import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from data_for_choise.handler import user_handlers, only_admin_handlers

from config_reader import config



async def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    bot = Bot(config.bot_token.get_secret_value())
    dp.include_routers(only_admin_handlers.router, user_handlers.router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())