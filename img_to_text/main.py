import os
import pytesseract
from PIL import Image, UnidentifiedImageError
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Проверка токена
if not TOKEN:
    raise ValueError("Не указан BOT_TOKEN в .env файле.")

# Создаем директорию для загрузок, если она отсутствует
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Создаем бот и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция OCR
def ocr_image(image_path: str, language: str) -> str:
    """
    Выполняет OCR на изображении и возвращает распознанный текст.
    """
    try:
        # Открываем изображение
        image = Image.open(image_path)

        # Выполняем OCR
        text = pytesseract.image_to_string(image, lang=language)

        return text.strip()
    except UnidentifiedImageError:
        raise ValueError("Файл не является изображением.")
    except Exception as e:
        raise ValueError(f"Ошибка при выполнении OCR: {e}")

# Хэндлер команды /start
@dp.message(CommandStart())
async def command_start(message: Message):
    """
    Обработчик команды /start.
    """
    await message.answer(
        "Привет! Я бот для распознавания текста с изображений. "
        "Отправь мне картинку, и я извлеку из неё текст. 😊"
    )

# Хэндлер для обработки изображений
@dp.message(lambda msg: msg.photo)
async def handle_photo(message: Message):
    """
    Обработчик сообщений с изображениями.
    """
    # Берем изображение с максимальным разрешением
    photo = message.photo[-1]

    try:
        # Получаем файл с помощью get_file
        file = await bot.get_file(photo.file_id)
        file_path = os.path.join(DOWNLOAD_DIR, f"{photo.file_id}.jpg")

        # Загружаем файл
        await bot.download_file(file.file_path, destination=file_path)

        # Выполняем OCR
        language = "rus"  # Укажите языки OCR
        text = ocr_image(file_path, language)

        # Отправляем результат пользователю
        if text:
            await message.answer(f"Распознанный текст:\n\n{text}")
        else:
            await message.answer("Не удалось распознать текст на изображении.")
    except ValueError as e:
        await message.answer(f"Ошибка: {e}")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
    finally:
        # Удаляем файл после обработки
        if os.path.exists(file_path):
            os.remove(file_path)


# Хэндлер для некорректных данных
@dp.message()
async def handle_invalid_data(message: Message):
    """
    Обработчик некорректных данных (например, текст вместо фото).
    """
    await message.answer("Пожалуйста, отправьте изображение для обработки.")

# Запуск бота
async def main():
    """
    Запуск бота.
    """
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
