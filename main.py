import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
import requests, random
from gtts import gTTS
import os
from googletrans import Translator
from config import TOKEN

# lesson_TG01_bot
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video_file = FSInputFile('media/video.mp4')
    await bot.send_video(message.chat.id, video_file)


@dp.message(Command('audio'))
async def audio(message: Message):
    audio_file = FSInputFile('media/audio.mp3')
    await bot.send_audio(message.chat.id, audio_file)


@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "Вариант 1\n1. Приседания – 3х12 раз\n2. Жим лежа – 3х12 раз\n3. Планка – 3х45 секунд",
        "Вариант 2\n1. Жим лежа – 3х12 раз\n2. Планка – 3х45 секунд\n3. Жим ногами – 3х12 раз",
        "Вариант 3\n1. Планка – 3х45 секунд\n2. Жим ногами – 3х12 раз\n3. Подтягивания – 3х12 раз"
    ]
    random_training = random.choice(training_list)
    await message.answer(f"Это ваша тренировка на сегодня:\n{random_training}")

    # tts = gTTS(text=random_training, lang='ru')
    # tts.save("training.mp3")
    # audio_file = FSInputFile("training.mp3")
    # await bot.send_audio(message.chat.id, audio_file)
    # os.remove("training.mp3")

    tts = gTTS(text=random_training, lang='ru')
    tts.save("training.ogg")
    voice_file = FSInputFile("training.ogg")
    await bot.send_voice(message.chat.id, voice_file)
    os.remove("training.ogg")


@dp.message(Command('voice'))
async def voice(message: Message):
    sound = FSInputFile("media/sample.ogg")
    await message.answer_voice(sound)


@dp.message(Command('doc'))
async def doc(message: Message):
    doc_file = FSInputFile("media/doc.pdf")
    await bot.send_document(message.chat.id, doc_file)


# ----------------------------------------------------------------------
def translate_text(en_text):
    translator = Translator()
    ru_text = translator.translate(en_text, src='en', dest='ru').text
    return ru_text


# Декоратор, регистрирующий обработчик для команды /meteo
@dp.message(Command('meteo'))
async def f_meteo(message: Message):
    city = "Москва"
    api_key = "bf599969fa3d07075ac981c3ba80fab8"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather = response.json()

    translated_city = translate_text(weather['name'])
    text_1 = f"Погода в городе {translated_city}"
    text_2 = f"Температура: {weather['main']['temp']}°C"
    translated_weather = translate_text(weather['weather'][0]['description'])
    text_3 = f"Погода: {translated_weather}"
    await message.answer(f"{text_1}:\n{text_2}\n{text_3}")


# Декоратор, регистрирующий обработчик для сообщений, текст которых равен "Что такое ИИ?"
@dp.message(F.text == "Что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект – это свойство искусственных интеллектуальных систем выполнять'
                         ' творческие функции, которые традиционно считаются прерогативой человека; наука и технология'
                         ' создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')


# Декоратор, регистрирующий обработчик для сообщений, содержащих фотографии
@dp.message(F.photo)
async def react_photo(message: Message):
    answer_list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answer = random.choice(answer_list)
    await message.answer(rand_answer)
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')


# @dp.message(Command('photo', prefix='&'))
@dp.message(Command('photo'))
async def photo(message: Message):
    photos = ["https://gallerix.ru/pic/_EX/1593896443/655331420.jpeg",
              "https://sr.gallerix.ru/M/1161425349/2468.jpg",
              "https://sr.gallerix.ru/V/369985082/2129753821.jpg",
              "https://sr.gallerix.ru/D/825575191/1663997468.jpg",
              "https://sr.gallerix.ru/_EX/1124510458/768903337.jpg",
              ]
    random_photo = random.choice(photos)
    await message.answer_photo(photo=random_photo, caption='Это супер крутая картинка')


# Декоратор, регистрирующий обработчик для команды /help
@dp.message(Command('help'))
async def f_help(message: Message):
    await message.answer(
        "Этот бот умеет выполнять команды:\n/start\n/help\n/photo\n/meteo\n/video\n/audio\n/training\n/voice\n/doc")


# Декоратор, регистрирующий обработчик для команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Приветик, {message.from_user.first_name}!")


# @dp.message()
# async def start(message: Message):
#     await message.answer("Я тебе ответил")

# @dp.message()
# async def start(message: Message):
#     await message.send_copy(chat_id=message.chat.id)

@dp.message()
async def start(message: Message):
    if message.text.lower() == 'test':
        await message.answer('Тестируем')


# Асинхронная функция, которая запускает поллинг бота. Поллинг – это метод получения новых сообщений от сервера Telegram
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
