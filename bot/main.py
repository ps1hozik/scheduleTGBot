import asyncio
import logging


from aiogram import Bot
from aiogram import Dispatcher
from aiogram.enums import ParseMode


from dotenv import load_dotenv
import os
import sys

load_dotenv()

from routers import router as main_router


paths = ["schedule"]
for path in paths:
    sys.path.insert(1, os.path.join(sys.path[0], path))


async def main():
    dp = Dispatcher()
    dp.include_router(main_router)

    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=os.getenv("BOT_TOKEN"),
        parse_mode=ParseMode.HTML,
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
