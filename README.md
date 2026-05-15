# SpacedReader

Персональное приложение интервального повторения для прочитанного. Пользователь логирует материал с двухпредложечной заметкой; приложение планирует повторения по алгоритму SM-2; при повторении LLM генерирует вопрос по заметке; пользователь отвечает, выставляет оценку 0–5, SM-2 пересчитывает расписание. Еженедельные LLM-резюме.

## Архитектура

```
src/
├── domain/                # чистая доменная логика, без фреймворков
│   ├── reading/           # bounded context: материалы
│   ├── review/            # bounded context: карточки SM-2
│   ├── llm/               # абстракция LLM-клиента
│   ├── transaction.py     # ITransactionContext — граница транзакции
│   └── exceptions.py      # базовый DomainException
├── use_cases/             # application layer, по одному файлу на use case
│   ├── reading/
│   ├── review/
│   └── insights/
├── infrastructure/
│   ├── database/
│   │   ├── models/        # SQLAlchemy-модели с from_domain / to_domain
│   │   ├── dao/           # реализации DAO, наследуют BaseDAO
│   │   └── transaction.py # SqlAlchemyTransactionContext
│   └── llm/               # OpenAI-клиент и фейк для тестов
├── presentation/
│   └── api/v1/            # FastAPI-роуты и Pydantic-схемы с from_domain
├── settings/              # pydantic-settings по контексту
├── container.py           # punq DI-контейнер
└── main.py
streamlit_app/             # фронтенд, общается с бэкендом только через HTTP
```

**Стек:** FastAPI · SQLAlchemy async · asyncpg · Alembic · punq · OpenAI · Streamlit · Postgres

**Принципы:** DDD, SOLID, абсолютные импорты, типизированные сигнатуры, `ITransactionContext` на use case уровне, domain exception pattern, `.new()` на командах, `from_domain` / `to_domain` на моделях и схемах, router-level try/except.

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
# юнит-тесты (без БД)
pytest tests/unit -v

# интеграционные тесты (требуют Docker для testcontainers)
pytest tests/integration -v
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
