# Установка

## пк win10
1. скачать https://github.com/UB-Mannheim/tesseract/wiki

2. добавить *C:\Program Files\Tesseract-OCR* в PATH
3. чекнуть устновку *tesseract -v*
4. poetry shell
5. poetry install

# Запуск

1. получить/скопировать имеющийся api токен бота\
1.1 если нет токена зайти в тг в @BotFather\
    ввести /newbot и следовать инструкциям бота
2. создать в корне проекта файл .env
3. вставить токен в .env
4. запустить

# через докер
1. docker pull b0ond/img_to_text
2. добавить переменную BOT_TOKEN в образ и вставить токен бота
3. запустить