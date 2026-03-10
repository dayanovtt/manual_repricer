import asyncio

from aiogram import Bot, Dispatcher

from app.config import load_env_file, get_token
from app.handlers import register_handlers


async def main() -> None:
    load_env_file()
    token = get_token()

    bot = Bot(token=token)
    dp = Dispatcher()

    register_handlers(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
