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

input_text = "Добрый день"

# Декоратор, регистрирующий обработчик для команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Приветик, {message.from_user.first_name}!")


# Декоратор, регистрирующий обработчик для команды /help
@dp.message(Command('help'))
async def f_help(message: Message):
    await message.answer(
        "Бот умеет выполнять команды:\n/start\n/help\n/photo\n/meteo\n/video\n/audio\n/voice\n/doc\n/training\n/beep")


# Декоратор, регистрирующий обработчик для сообщений, текст которых равен "Что такое ИИ?"
@dp.message(F.text == "Что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект – это свойство искусственных интеллектуальных систем выполнять'
                         ' творческие функции, которые традиционно считаются прерогативой человека; наука и технология'
                         ' создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')


@dp.message(Command('photo'))
async def photo(message: Message):
    photos = ["https://sr.gallerix.ru/_EX/1593896443/655331420.jpg",
              "https://sr.gallerix.ru/M/1161425349/2468.jpg",
              "https://sr.gallerix.ru/V/369985082/2129753821.jpg",
              "https://sr.gallerix.ru/D/825575191/1663997468.jpg",
              "https://sr.gallerix.ru/_EX/1124510458/768903337.jpg",
              ]
    random_photo = random.choice(photos)
    await message.answer_photo(photo=random_photo, caption='Это супер крутая картинка')


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

    tts = gTTS(text=random_training, lang='ru')
    tts.save("training.ogg")
    voice_file = FSInputFile("training.ogg")
    await bot.send_voice(message.chat.id, voice_file)
    os.remove("training.ogg")


@dp.message(Command('beep'))
async def beep(message: Message):
    sound = FSInputFile("media/sample.ogg")
    await message.answer_voice(sound)


@dp.message(Command('doc'))
async def doc(message: Message):
    doc_file = FSInputFile("media/doc.pdf")
    await bot.send_document(message.chat.id, doc_file)


# ---------- TG01 Прогноз погоды с использованием API ----------

def translate_text_ru(en_text):
    translator = Translator()
    ru_text = translator.translate(en_text, src='en', dest='ru').text
    return ru_text


@dp.message(Command('meteo'))
async def f_meteo(message: Message):
    city = "Москва"
    api_key = "bf599969fa3d07075ac981c3ba80fab8"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather = response.json()

    translated_city = translate_text_ru(weather['name'])
    text_1 = f"Погода в городе {translated_city}"
    text_2 = f"Температура: {weather['main']['temp']}°C"
    translated_weather = translate_text_ru(weather['weather'][0]['description'])
    text_3 = f"Погода: {translated_weather}"
    await message.answer(f"{text_1}:\n{text_2}\n{text_3}")


# ---------- TG02-1. Напишите код для сохранения всех фото, которые отправляет пользователь боту в папке img ----------

@dp.message(F.photo)
async def react_photo(message: Message):
    answer_list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answer = random.choice(answer_list)
    await message.answer(rand_answer)
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')


# ---------- TG02-2. Отправьте с помощью бота голосовое сообщение ----------

def text_to_voice(text_message):
    voice_file_name = "voice_message.ogg"
    tts = gTTS(text=text_message, lang='ru')
    tts.save(voice_file_name)
    voice_file = FSInputFile(voice_file_name)
    return voice_file, voice_file_name


@dp.message(Command('voice'))
async def voice(message: Message):
    voice_file, voice_file_name = text_to_voice(input_text)
    await message.answer_voice(voice_file)
    os.remove(voice_file_name)


# ---------- TG02-3. Напишите код для перевода любого текста, введённого пользователем, на английский язык ----------

def translate_text_en(ru_text):
    translator = Translator()
    en_text = translator.translate(ru_text, src='ru', dest='en').text
    return en_text


@dp.message()
async def start(message: Message):
    global input_text
    # Сохраняем текст для команды /voice
    input_text = message.text
    await message.answer(translate_text_en(message.text))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
