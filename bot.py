import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers import orderConstructor, start, repairCategories, moreInfo, designProject, aboutUs, portfolio

from misc.utils import pull_orders, pull_feedbacks

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
        level=logging.INFO,
        filename="bot.log",
        format="%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
bot = Bot(token=os.getenv('TOKEN'))


async def main(bot: Bot):
    dp = Dispatcher(storage=RedisStorage.from_url(os.getenv('REDIS_URL')))
    dp.include_routers(start.router, orderConstructor.router, repairCategories.router,
                       moreInfo.router, designProject.router, aboutUs.router, portfolio.router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(pull_orders, 'interval', minutes=30, args=[bot, ])
    scheduler.add_job(pull_feedbacks, 'interval', minutes=30, args=[bot, ])
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main(bot))
