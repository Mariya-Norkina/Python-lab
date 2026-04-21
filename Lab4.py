import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.client.session.aiohttp import AiohttpSession

# Токен, полученный от BotFather
TOKEN = "8639420632:AAHXqzC0SmQvG599f4KLQPKpTMchQAEbEhA"

# Словарь азбуки Морзе (парсинг/константа)
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    'А': '.-', 'Б': '-...', 'В': '.--', 'Г': '--.', 'Д': '-..', 'Е': '.', 'Ё': '.',
    'Ж': '...-', 'З': '--..', 'И': '..', 'Й': '.---', 'К': '-.-', 'Л': '.-..',
    'М': '--', 'Н': '-.', 'О': '---', 'П': '.--.', 'Р': '.-.', 'С': '...',
    'Т': '-', 'У': '..-', 'Ф': '..-.', 'Х': '....', 'Ц': '-.-.', 'Ч': '---.',
    'Ш': '----', 'Щ': '--.-', 'Ъ': '--.--', 'Ы': '-.--', 'Ь': '-..-', 'Э': '..-..',
    'Ю': '..--', 'Я': '.-.-',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ' ': '/'
}

# Создаем обратный словарь аккуратно (чтобы коды не пропадали)
REVERSE_DICT = {v: k for k, v in MORSE_CODE_DICT.items() if k != ' '}

dp = Dispatcher()

def get_main_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🆘 Отправить SOS")
    builder.button(text="❓ Помощь")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Приветствие по имени (п. 1.1.4)
    await message.answer(
        f"Привет, {message.from_user.first_name}! Я бот-переводчик азбуки Морзе.",
        reply_markup=get_main_kb()
    )

@dp.message(Command("help"))
@dp.message(F.text == "❓ Помощь")
async def cmd_help(message: types.Message):
    # Обязательный help и грустный смайлик (п. 1.1.3)
    await message.answer("Просто отправь мне текст, и я переведу его в Морзе! ☹")

@dp.message(F.text == "🆘 Отправить SOS")
async def send_sos(message: types.Message):
    # Реализация функции SOS (п. 1.1.5 и Вариант 20)
    await message.answer("SOS > ...---...")

@dp.message()
async def translate_text(message: types.Message):
    text = message.text.upper().strip()
    # Проверка: если в сообщении только точки, тире, пробелы и слэши — это Морзе
    if all(char in ".- /" for char in text):
        # Декодируем из Морзе в Текст
        words = text.split(" / ")
        decoded_phrase = []
        for word in words:
            decoded_word = "".join(REVERSE_DICT.get(symbol, "?") for symbol in word.split())
            decoded_phrase.append(decoded_word)
        res = " ".join(decoded_phrase)
    else:
        # Кодируем из Текста в Морзе
        res = " ".join(MORSE_CODE_DICT.get(char, "?") for char in text)
    
    await message.answer(f"Результат:\n`{res}`", parse_mode="Markdown")

async def main():
    # Настройка логирования (поможет увидеть ошибки подключения)
    logging.basicConfig(level=logging.INFO)

    # Инициализируем бота с сессией
    bot = Bot(token=TOKEN)

    print("Бот запущен через прокси...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")