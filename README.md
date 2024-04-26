# Charity_fund_with_googlesheets

## Описание
Приложение  Charity_fund_with_googlesheets - это API приложение для Благотворительного фонда, созданнное на базе фреймворка FastAPI.

В Фонде Charity_fund_with_googlesheets может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.

Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму.

Целевые проекты создаются администраторами сайта. 
Любой пользователь может видеть список всех проектов, включая требуемые и уже внесенные суммы. Это касается всех проектов — и открытых, и закрытых.
Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.

В приложение Charity_fund_with_googlesheets добавлена возможность формирования отчёта в гугл-таблице. В таблицу выводятся закрытые проекты, отсортированные по скорости сбора средств: от тех, что закрылись быстрее всего, до тех, что долго собирали нужную сумму.

## Технолгии
- Python 3.9
- FastAPI 0.78.
- FastAPI-Users 10.0
- Pydantic 1.9
- SQLAlchemy 1.4
- Alembic 1.7
- Google Sheets API
- Google Drive API

## Запуск проекта
Клонировать репозиторий и перейти в директорию проекта:
```
git clone https://github.com/KonstantinSKS/charity_fund_with_googlesheets.git
```
```
cd charity_fund_with_googlesheets
```
Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
### Команда для Windows:
```
source venv/Scripts/activate
```
### Для Linux и macOS:
```
source venv/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Создайте и заполните файл .env в корневой папке проекта:

Образец .env:
```
APP_TITLE=your_project_name
APP_DESCRIPTION=your_project_description
DATABASE_URL=your_database_url
SECRET=your_secret_key
FIRST_SUPERUSER_EMAIL=example_user@example.com
FIRST_SUPERUSER_PASSWORD=example
EMAIL=<ваша почта на>@gmail.com
```
(Далее необходимо ввести данные из JSON-файла с данными вашего сервисного аккаунта, предоставленные Google Cloud Platform.)
```
TYPE=
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
```

Выполнить миграции:
```
alembic upgrade head
```
Запустить проект:
```
uvicorn app.main:app --reload
```
После запуска документация проекта будет доступна по адресу: http://127.0.0.1:8000/docs

## Автор: 
Стеблев Константин
