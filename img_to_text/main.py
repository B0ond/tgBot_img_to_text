import pytesseract
from PIL import Image
import os


# Укажите путь к исполняемому файлу Tesseract, если он не находится в PATH
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Пример для Unix
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Пример для Windows

def ocr_image(image_path, language):
    """
    Выполняет OCR на изображении и возвращает распознанный текст.
    """
    try:
        # Открываем изображение
        image = Image.open(image_path)

        # Выполняем OCR
        text = pytesseract.image_to_string(image, language)  # Укажите язык, если нужно

        return text
    except Exception as e:
        print(f"Ошибка при выполнении OCR: {e}")
        return None


def main():
    # Укажите путь к изображению
    image_path = r'C:\Users\mz-admin\Desktop\123.jpeg'

    # Проверяем существование файла
    if not os.path.exists(image_path):
        print(f"Файл {image_path} не существует.")
        return

    #язык
    language = 'rus+eng'

    # Выполняем OCR
    text = ocr_image(image_path, language)

    if text:
        print("------------------------------")
        print(text)
    else:
        print("Не удалось распознать текст.")


if __name__ == "__main__":
    main()

