import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from handlers import orderConstructor, start, repairCategories, moreInfo, designProject, aboutUs, portfolio

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
    dp.include_routers(start.router, orderConstructor.router, repairCategories.router, moreInfo.router,
                       designProject.router, aboutUs.router, portfolio.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main(bot))
