import asyncio

from aiogram import Bot
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from bot import bot
from database import engine, redis
from dispatcher import dp
from settings import settings


async def on_startup(bot: Bot):
    me = await bot.get_me()
    print(f"https://t.me/{me.username} is started...")

    if settings.python_env == "production":
        await bot.set_webhook(f"{settings.base_webhook_url}{settings.webhook_path}")


async def on_shutdown():
    await engine.dispose()
    await redis.aclose()


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    if settings.python_env == "production":
        app = web.Application()
        webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
        webhook_requests_handler.register(app, path=str(settings.webhook_path))
        setup_application(app, dp, bot=bot)
        web.run_app(app, host=settings.web_server_host, port=settings.web_server_port)
        return

    await dp.start_polling(bot)  # type: ignore


asyncio.run(main())
