# DigiStore — интернет-магазин цифровых услуг

Учебный проект на Django. Автор: Sasuke Uchiha.

## Стек

- Python 3.10+
- Django 5.2
- SQLite

## Установка и запуск

1. Клонируйте репозиторий и перейдите в папку проекта:
```commandline
   git clone <ссылка на репозиторий>
   cd SU_DigistoreProject
```
2. Создайте и активируйте виртуальное окружение:
```commandline
   python -m venv venv
   venv\Scripts\activate          # Windows
   source venv/bin/activate       # Linux / macOS
```
3. Установите зависимости:
```commandline
   pip install -r requirements.txt
```
4. Запустите сервер:
```commandline
   python manage.py runserver
```
5. Откройте http://127.0.0.1:8000/