import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from handlers import orderConstructor

from dotenv import load_dotenv

load_dotenv()


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )

    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher(storage=RedisStorage.from_url(os.getenv('REDIS_URL')))
    dp.include_router(orderConstructor.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
