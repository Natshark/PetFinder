from aiogram import Bot
from aiogram.types import Message

from core.keyboards.Inline import site_link
import parse_and_algorithm as pal
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def sent_mail(lost_animal, found_animal):
    print(1)
    msg = MIMEMultipart()

    msg['Subject'] = 'Питомец найден!'
    msg['From'] = 'petfinder86@mail.ru'
    msg['To'] = lost_animal.mail


    text = 'Здравствуйте, вашего питомца нашли, просьба связаться с ' + found_animal.mail
    msg.attach(MIMEText(text))

    with open(r"C:\Users\modin\PycharmProjects\PetFinder\found_animals_img\\" + found_animal.fname, 'rb') as image_file:
        img = MIMEImage(image_file.read())
        img.add_header('Content-Disposition', 'attachment', filename=found_animal.fname)
        msg.attach(img)

    with smtplib.SMTP('smtp.mail.ru', 587) as server:
        server.starttls()
        server.login('petfinder86@mail.ru', 'pi4ZPi822wFfJDhkV6hp')
        server.sendmail('petfinder86@mail.ru', lost_animal.mail, msg.as_string())


async def get_start(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id,f'Привет, {message.from_user.first_name}! Представляю вашему вниманию сервис для идентификации пропавших животных.',reply_markup= site_link)


async def get_site(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f'Перейти на наш сайт вы можете по ссылке ниже', reply_markup=site_link)


async def i_found_animal(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, 'Отправьте найденного питомца!')


async def load_photo(message: Message):
    if message.content_type == 'photo':
        found_animal = pal.Card()
        found_animal.fname = ''.join(str(datetime.datetime.now()).split(':')) + ".png"
        found_animal.mail = "modin.ru2@mail.ru"
        await message.bot.download(message.photo[-1], r"C:\Users\modin\PycharmProjects\PetFinder\found_animals_img\\" + found_animal.fname)
        sent_mail(pal.find_match(found_animal, pal.lost_animals, "found_animals_img\\", "lost_animals_img\\"), found_animal)
