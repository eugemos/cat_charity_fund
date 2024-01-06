# Проект QRKot
Приложение для Благотворительного фонда поддержки котиков предоставляет API для создания благотворительных проектов и внесения пожертвований.

### Автор
Москалянов Евгений

### Технологии
Python 3.10,
FastAPI 0.78,
SQLAlchemy 1.4
Alembic 1.7
Uvicorn 0.17

### Запуск проекта в dev-режиме
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/eugemos/cat_charity_fund.git
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

Обновить утилиту pip:

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
alembic upgrade head
```

Запустить проект:

```
uvicorn app.main:app
```

### Использование
Проект доступен по адресу http://127.0.0.1:8000
Для обращения к эндпойнтам API следует использовать утилиту для обмена данными
по протоколу HTTP. Например, **postman** https://www.postman.com

Документация к API сожержится в файле openapi.json, её можно посмотреть в браузере с помощью сайта https://redocly.github.io/redoc/

Кроме того, к API можно обращаться через пользовательский интерфейс, расположенный по адресу http://127.0.0.1:8000/docs
