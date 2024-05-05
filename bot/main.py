import asyncio
import logging

# from apscheduler.schedulers.asyncio import AsyncIOScheduler


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

# from download import download
# from upload import upload


# async def schedule_upload():
#     download()
#     await asyncio.sleep(10)
#     upload()


async def main():
    dp = Dispatcher()
    dp.include_router(main_router)

    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=os.getenv("BOT_TOKEN"),
        parse_mode=ParseMode.HTML,
    )
    # scheduler = AsyncIOScheduler()
    # scheduler.add_job(schedule_upload, "cron", day_of_week="fri", hour=17 - 3)
    # scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
