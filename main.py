from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from core.handlers.basic import get_start
from core.handlers.basic import get_site
from core.handlers.basic import load_photo
from aiogram.filters.callback_data import CallbackQuery
from aiogram import F
from core.keyboards.Inline import site_link

import asyncio

TOKEN_API = "6742857616:AAE9cbUJBzUnF0v7p9XmKelpCfTzb9mykFw"


async def start():
    bot = Bot(token=TOKEN_API)

    dp = Dispatcher()

    @dp.callback_query(F.data == "sos")
    async def find(callback: CallbackQuery):
        await callback.message.answer('Пришлите фотографию животного')

    dp.message.register(get_start, Command('start'))
    dp.message.register(get_site, Command('site'))
    dp.message.register(load_photo)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
