# Используем Python 3.12 как базовый образ
FROM python:3.12-slim

# Устанавливаем системные зависимости, включая Tesseract и языковые файлы
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-rus \
    libtesseract-dev \
    libjpeg-dev \
    libpng-dev \
    zlib1g-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt /app/requirements.txt

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем весь проект
COPY . /app

# Добавляем Tesseract в PATH и устанавливаем TESSDATA_PREFIX
ENV PATH="/usr/bin/tesseract:$PATH"
ENV TESSDATA_PREFIX="/usr/share/tesseract-ocr/5/tessdata/"

# Запускаем приложение
CMD ["python3", "img_to_text/main.py"]
