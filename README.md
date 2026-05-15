# SpacedReader

Персональное приложение интервального повторения для прочитанного. Пользователь логирует материал с двухпредложечной заметкой; приложение планирует повторения по алгоритму SM-2; при повторении LLM генерирует вопрос по заметке; пользователь отвечает, выставляет оценку 0–5, SM-2 пересчитывает расписание. Еженедельные LLM-резюме.

## Архитектура

```
src/
├── domain/          # чистая доменная логика, без фреймворков
│   ├── reading/     # bounded context: материалы
│   └── review/      # bounded context: карточки SM-2
├── use_cases/       # application layer, по одному файлу на use case
├── infrastructure/  # SQLAlchemy, aiosql, LLM-клиенты
├── presentation/    # FastAPI-роуты и схемы
└── main.py
streamlit_app/       # фронтенд, общается с бэкендом только через HTTP
```

**Стек:** FastAPI · SQLAlchemy async · asyncpg · Alembic · punq · aiosql · OpenAI · Streamlit · Postgres

**Принципы:** DDD, SOLID, абсолютные импорты, типизированные сигнатуры, внешние SQL-файлы, domain exception pattern, `.new()` на командах, router-level try/except.

## Запуск локально

```bash
cp .env.example .env
# заполнить OPENAI_API_KEY в .env

docker compose up --build
```

- Бэкенд: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Фронтенд: http://localhost:8501

Alembic-миграции запускаются автоматически при старте бэкенда.

## Тесты

```bash
pip install -e ".[dev]"

# юнит-тесты (без БД)
pytest tests/unit -v

# интеграционные тесты (требуют Docker для testcontainers)
pytest tests/integration -v

# все
pytest -v
```

## Переменные окружения

| Переменная | Описание | По умолчанию |
|---|---|---|
| `POSTGRES_HOST` | хост БД | `db` |
| `POSTGRES_PORT` | порт БД | `5432` |
| `POSTGRES_DB` | имя БД | `spacedreader` |
| `POSTGRES_USER` | пользователь | `spacedreader` |
| `POSTGRES_PASSWORD` | пароль | `spacedreader` |
| `OPENAI_API_KEY` | ключ OpenAI | — |
| `OPENAI_MODEL` | модель | `gpt-4o-mini` |
| `OPENAI_TIMEOUT_SECONDS` | таймаут запросов | `30.0` |
| `APP_DEBUG` | режим отладки | `false` |
| `APP_BACKEND_URL` | URL бэкенда для фронтенда | `http://backend:8000` |
