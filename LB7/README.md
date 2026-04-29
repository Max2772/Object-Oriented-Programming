# Finance Tracker API

Backend-приложение «Трекер личных финансов» на **FastAPI** с архитектурой **Clean Architecture**.

---

## Запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Запуск сервера

```bash
python main.py
```

### 3. Swagger UI

Откройте в браузере: **http://localhost:8000/docs**

### 4. Запуск тестов

```bash
pytest tests/ -v
```

---

## Структура проекта

```
src/
├── api/          # Хендлеры (обработка входящих запросов)
├── controllers/  # Бизнес-логика
├── clients/      # Работа с БД (репозитории)
├── models/       # Сущности и DTO
└── shared/       # Конфиг, исключения, схемы ответов
```

---

## API

### Аутентификация

| Метод | URL | Описание |
|-------|-----|----------|
| `POST` | `/api/v1/auth/register` | Регистрация |
| `POST` | `/api/v1/auth/login` | Вход, получение JWT |

### Счета

| Метод | URL | Описание |
|-------|-----|----------|
| `POST` | `/api/v1/accounts/` | Создать счёт |
| `GET` | `/api/v1/accounts/` | Список счетов |
| `GET` | `/api/v1/accounts/{id}` | Счёт по ID |
| `PUT` | `/api/v1/accounts/{id}` | Обновить |
| `DELETE` | `/api/v1/accounts/{id}` | Удалить |

### Транзакции

| Метод | URL | Описание |
|-------|-----|----------|
| `POST` | `/api/v1/transactions/` | Создать транзакцию |
| `GET` | `/api/v1/transactions/` | Список с фильтрами |
| `DELETE` | `/api/v1/transactions/{id}` | Удалить с откатом баланса |

### Бюджеты

| Метод | URL | Описание |
|-------|-----|----------|
| `POST` | `/api/v1/budgets/` | Установить/обновить лимит |
| `GET` | `/api/v1/budgets/` | Статус лимитов за месяц |
| `DELETE` | `/api/v1/budgets/{id}` | Удалить лимит |

### Аналитика

| Метод | URL | Описание |
|-------|-----|----------|
| `GET` | `/api/v1/analytics/summary` | Сводка за период по категориям |

---

## Паттерны проектирования

| Паттерн | Где применён | Обоснование |
|---------|-------------|-------------|
| **Repository** | `clients/repositories.py` | Изоляция доступа к данным от бизнес-логики |
| **Dependency Injection** | `api/dependencies.py` | Хендлеры получают сессию БД и пользователя извне |
| **Facade** | `controllers/auth_controller.py` | Скрывает сложность JWT и хеширования за простым интерфейсом |
| **Template Method** | `SQLAlchemyRepository` | Базовые CRUD-операции в родителе, специфика — в наследниках |
| **Singleton** | `shared/config.py` | Единственный экземпляр `Settings` через `pydantic-settings` |
| **Strategy** | `controllers/analytics_controller.py` | Разные стратегии агрегации (по категории, по типу) |