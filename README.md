# Flask Web App — Кино и отзывы

## Описание

Веб-приложение на Flask для просмотра информации о фильмах, написания 
и модерации отзывов, а также управления пользователями. Содержит как 
веб-интерфейс, так и полноценное RESTful API.

## Технологии

- Backend: Flask, Flask-RESTful, Flask-WTF, SQLAlchemy
- Frontend: HTML, CSS (или Bootstrap), Jinja2
- Аутентификация: Flask-Login
- Тестирование: unittest
- API: REST, разделение на v1 и v2
- ORM: SQLAlchemy

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/yourusername/film-review-flask.git
cd film-review-flask
``

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Запустите приложение:

```bash
python app/app.py
```

Приложение будет доступно по адресу `http://127.0.0.1:5000`.

## Функциональность

### Для пользователей:
- Регистрация / Авторизация
- Просмотр фильмов
- Добавление / редактирование отзывов

### Для API:
- `GET /api/v1/films` — список фильмов
- `POST /api/v1/reviews` — добавить отзыв
- `GET /api/v2/users` — получить пользователей
- и другие...

## Тестирование

```bash
python -m unittest discover test
```

## Структура проекта

```
pythonProject2/
│
├── api/
│   ├── v1/  # REST API v1
│   └── v2/  # REST API v2
├── app/     # Веб-интерфейс
├── data/    # Модели и БД
├── forms/   # Flask-WTF формы
├── test/    # Тесты
├── requirements.txt
└── README.md
```

Проект создан в образовательных целях.
