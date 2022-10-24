import re
from aiogram import (Bot, Dispatcher, types, executor)
from nopik_query import (Day, Week)
from nopik_db import *

TOKEN = '5615465282:AAEHUGtODW-uMJRbwMaZhMLOz9BPMzfPff4'


bot = Bot(TOKEN)

dp: Dispatcher = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def on_message(msg: types.Message):
    print(msg.from_user)
    await bot.send_message(msg.from_user.id, f"Hello , \n{msg.from_user.username}")


@dp.message_handler(commands=['rasp'])
async def on_message(msg: types.Message):
    if(create_event(msg.from_user.id, "date")):
        await bot.send_message(msg.from_user.id, f"Выберите периуд")
    else:
        if (create_event(msg.from_user.id, "rasp")):
            await bot.send_message(msg.from_user.id, f"Введите группу\n(пример: 'ИС 2.20' не забудьте пожалуйста пробел)")
        else:
            await bot.send_message(msg.from_user.id, f"Введите группу")


@dp.message_handler()
async def on_message(msg: types.Message):

    if (get_event(msg.from_user.id, "rasp")):
        if (re.search("[А-Я][А-Я]\s((\d.\d\d)|(\d.\d))", msg.text)):
            delete_event(msg.from_user.id, "rasp")
            create_event(msg.from_user.id, "date")
            kb = [
                [
                    types.KeyboardButton(text="сегодня"),
                    types.KeyboardButton(text="завтра"),
                    types.ReplyKeyboardMarkup(text="на неделю")
                ],
            ]
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
                input_field_placeholder="Выберите периуд"
            )
            await bot.send_message(msg.from_user.id, f"Введите на какой периуд вам нужно расписание\nПример: 'сегодня' , 'завтра' , 'на неделю'")
        else:
            await bot.send_message(msg.from_user.id, f"Данные не корректны\nПример группы: 'ИС 1.20' 'ИС 2.20'")
    else:
        await bot.send_message(msg.from_user.id, f"Я не понимаю что вы хотите сделать , _,.\n\nВведите /help для получения помощи")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
