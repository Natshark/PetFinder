from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

site_link = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Найти пропавшее животное',
            callback_data='sos'
        ),
        InlineKeyboardButton(
            text='Перейти на сайт',
            url='https://animals.admhmao.ru/animals/#/dashboard'
        )
    ]])


