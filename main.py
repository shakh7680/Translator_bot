import logging
from oxford_lookup import getDefinitions

from aiogram import Bot, Dispatcher, executor, types

from googletrans import Translator
translator = Translator()

API_TOKEN = '5744521427:AAGS9wofm5KB99La3bF1k5veyptHZDnghyc'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Tarjima botga xush kelibsiz")


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Bu bot tarjima bot")


@dp.message_handler()
async def tarjimon(message: types.Message):
    lan = translator.detect(message.text).lang
    if len(message.text.split()) > 2:
        dest = 'uz' if lan == 'en' else 'en'
        await message.reply(translator.translate(message.text, dest).text)
    else:
        if lan == 'en':
            word_id = message.text
        else:
            word_id = translator.translate(message.text, dest='en').text
        lookup = getDefinitions(word_id)
        if lookup:
            await message.reply(f"Word {word_id} \nDefinitions:\n{lookup['definitions']}")
            if lookup.get('audio'):
                await message.reply_voice(lookup['audio'])
        else:
            await message.reply("Bynday so'z topilmadi")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)