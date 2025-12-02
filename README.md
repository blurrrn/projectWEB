# 🌸 Магазин Цветов - Микросервисная Архитектура

## 📋 Технологический стек

- **Python 3.11+**
- **FastAPI** - веб-фреймворк
- **PostgreSQL** - основная БД
- **Redis** - кеширование
- **RabbitMQ** - шина сообщений
- **SQLAlchemy** - ORM
- **Pydantic** - валидация данных
- **Docker & Docker Compose** - контейнеризация
- **JWT** - авторизация

## 🏗️ Архитектура

### Монолит (начальная версия)
- Clean Architecture
- 10 доменных сущностей
- REST API

### Микросервисы
1. **auth-service** - авторизация и аутентификация (JWT)
2. **catalog-service** - каталог цветов и букетов
3. **ordering-service** - управление заказами (Saga оркестратор)
4. **payment-service** - обработка платежей
5. **delivery-service** - управление доставкой

### Доступ к сервисам

- **API Gateway**: http://localhost:8000
- **Auth Service**: http://localhost:8001
- **Catalog Service**: http://localhost:8002
- **Ordering Service**: http://localhost:8003
- **Payment Service**: http://localhost:8004
- **Delivery Service**: http://localhost:8005
- **RabbitMQ Management**: http://localhost:15672 (guest/guest)

### API Документация

После запуска доступна Swagger документация:
- http://localhost:8000/docs (API Gateway)
- http://localhost:8001/docs (Auth Service)
- http://localhost:8002/docs
- http://localhost:8003/docs
- http://localhost:8004/docs
- http://localhost:8005/docs

## 🔐 Тестовые пользователи

После первого запуска создаются тестовые пользователи:
- **admin@example.com** / **admin123** (роль: admin)
- **user@example.com** / **user123** (роль: user)

## 📝 Структура проекта

```
flower-shop/
├── services/          # Микросервисы
│   ├── auth-service/
│   ├── catalog-service/
│   ├── ordering-service/
│   ├── payment-service/
│   └── delivery-service/
├── shared/            # Общие утилиты
├── docker-compose.yml
└── README.md
```

## 🔄 Паттерны

- **Transaction Outbox** - гарантированная доставка событий
- **Saga (Orchestration)** - распределенные транзакции
- **API Gateway** - единая точка входа
- **JWT Authentication** - токен-базированная авторизация

