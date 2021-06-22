"""
Принцип работы бота:
    При старте бота или написании команды /start, пользователь получает ответное сообщение
    с тремя кнопками. Пользователь может выбрать одну из трёх представленных валют.
    В противном случае он получит сообщение с ошибкой.
    После выбора валюты, выполняется функция get_exchange_rates, получаются актуальные данные
    с сайта https://blockchain.info/ru/ticker и формируется ответное сообщение. И пользователь
    получает ответное сообщение в формате '1 BTC = [значение] [символ валюты]'
"""


import requests  # Библотека для работы с запросами

from config import TOKEN # Импортируем токен бота
from aiogram import Bot, Dispatcher, types  # Методы из библиотеки aiogram для работы с Telegram Bot API
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = TOKEN  # Токен бота

bot = Bot(token=BOT_TOKEN)  # Создаем бота с введенным токеном

dp = Dispatcher(bot)  # Создаем диспатчер для работы с командами

async def get_exchange_rates():  # Асинхронная функция получения значений курса обмена в формате json
    try:
        # Получаем данные
        r = requests.get(
            "https://blockchain.info/ru/ticker"
        )
        data = r.json()  # Переводим в формат json
    except Exception as ex:
        pass
    return data

async def exchange_kb():  # Функция создания клавиатуры
    bt_rub = KeyboardButton('RUB')  # Создаем кнопки
    bt_usd = KeyboardButton('USD')
    bt_eur = KeyboardButton('EUR')
    kb = ReplyKeyboardMarkup(resize_keyboard=True)  # Создаем клавиатуру
    kb.add(bt_rub, bt_usd, bt_eur)  # Добавляем кнопки
    return kb  # Возвращаем клавиатуру

@dp.message_handler(commands=['start'])  # Функция выполянется при старте бота или при написании команды /start
async def with_start(message: types.Message):
    kb = await exchange_kb()  # Создаем клавиатуру
    # Отправляем сообщение и кнопки пользователю при старте
    await message.reply("Данный бот позволяет узнать курс биткоина\nВыберите валюту:", reply=False, reply_markup=kb)

@dp.message_handler(content_types=['text'])  # Функция выполняется при получении сообщения
async def choose_contry(message: types.Message):
    buff = await get_exchange_rates()  # Получаем json со значениями курса валют
    if message.text == 'RUB':  # Если нажали кнопку RUB
        ans = buff['RUB']['last']  # Получаем значение «last» - самая последняя рыночная цена
        cur = buff['RUB']['symbol']  # Получаем символ валюты
        answer = '1 BTC = %s %s' % (ans, cur)  # Формируем ответное сообщение
        await message.reply(answer, reply=False)  # Отправляем это сообщение
    elif message.text == 'USD':
        ans = buff['USD']['last']
        cur = buff['USD']['symbol']
        answer = '1 BTC = %s %s' % (ans, cur)
        await message.reply(answer, reply=False)
    elif message.text == 'EUR':
        ans = buff['EUR']['last']
        cur = buff['EUR']['symbol']
        answer = '1 BTC = %s %s' % (ans, cur)
        await message.reply(answer, reply=False)
    else:  # В случае, если пользователь не нажимает кнопку или отправляет неверное сообщение
        await message.reply("Ошибка! Выберите одну из трёх валют.", reply=False)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)  # Запускаем бота

