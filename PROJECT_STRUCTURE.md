# 📂 Структура проекта

```
flower-shop/
│
├── shared/                          # Общие модули для всех сервисов
│   ├── __init__.py
│   ├── database.py                  # SQLAlchemy setup
│   ├── redis_client.py              # Redis клиент
│   ├── rabbitmq_client.py           # RabbitMQ клиент
│   └── jwt_utils.py                 # JWT утилиты
│
├── services/                        # Микросервисы
│   │
│   ├── auth-service/               # Сервис авторизации (порт 8001)
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py             # FastAPI приложение
│   │   │   ├── models.py           # SQLAlchemy модели (User)
│   │   │   ├── schemas.py          # Pydantic схемы
│   │   │   ├── routes.py           # API endpoints
│   │   │   ├── services.py         # Бизнес-логика
│   │   │   └── init_data.py        # Инициализация тестовых данных
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── catalog-service/            # Сервис каталога (порт 8002)
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── models.py           # Flower, Category, Bouquet
│   │   │   ├── schemas.py
│   │   │   ├── routes.py
│   │   │   ├── services.py         # CRUD + Redis кеширование
│   │   │   └── init_data.py        # Тестовые цветы и букеты
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── ordering-service/          # Сервис заказов (порт 8003)
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── models.py           # Order, OrderItem, OutboxMessage
│   │   │   ├── schemas.py
│   │   │   ├── routes.py
│   │   │   ├── services.py         # CRUD + Saga логика
│   │   │   ├── background_tasks.py  # Outbox worker
│   │   │   ├── event_handlers.py   # Обработчики событий
│   │   │   └── rabbitmq_consumer.py # RabbitMQ consumer
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── payment-service/           # Сервис платежей (порт 8004)
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── models.py           # Payment, OutboxMessage
│   │   │   ├── schemas.py
│   │   │   ├── routes.py
│   │   │   ├── services.py         # Обработка платежей
│   │   │   ├── background_tasks.py # Outbox worker
│   │   │   ├── event_handlers.py   # Обработчик OrderCreated
│   │   │   └── rabbitmq_consumer.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── delivery-service/          # Сервис доставки (порт 8005)
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── models.py           # Shipment, OutboxMessage
│   │   │   ├── schemas.py
│   │   │   ├── routes.py
│   │   │   ├── services.py         # Управление доставкой
│   │   │   ├── background_tasks.py # Outbox worker
│   │   │   ├── event_handlers.py   # Обработчик OrderPaid
│   │   │   └── rabbitmq_consumer.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── api-gateway/               # API Gateway (порт 8000)
│       ├── app/
│       │   ├── __init__.py
│       │   └── main.py            # Проксирование запросов
│       ├── Dockerfile
│       └── requirements.txt
│
├── docker-compose.yml             # Docker Compose конфигурация
├── .dockerignore                  # Игнорируемые файлы для Docker
├── .env.example                   # Пример переменных окружения
│
├── README.md                      # Основная документация
├── INSTRUCTIONS.md                # Подробная инструкция
├── QUICK_START.md                 # Быстрый старт
├── ARCHITECTURE.md                # Описание архитектуры
└── PROJECT_STRUCTURE.md           # Этот файл
```

## Доменные сущности

### Auth Service
- **User**: пользователь системы

### Catalog Service
- **Flower**: цветок
- **Category**: категория
- **Bouquet**: букет

### Ordering Service
- **Order**: заказ
- **OrderItem**: элемент заказа
- **OutboxMessage**: сообщение для публикации (Transaction Outbox)

### Payment Service
- **Payment**: платеж
- **OutboxMessage**: сообщение для публикации

### Delivery Service
- **Shipment**: доставка
- **OutboxMessage**: сообщение для публикации

**Всего: 10 доменных сущностей** ✅

## Технологии

- **Python 3.11**
- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM
- **PostgreSQL** - БД
- **Redis** - кеширование
- **RabbitMQ** - шина сообщений
- **Pydantic** - валидация
- **Docker & Docker Compose** - контейнеризация

## Паттерны

1. ✅ **Clean Architecture** - разделение на слои
2. ✅ **Микросервисы** - 5 независимых сервисов
3. ✅ **Saga (Orchestration)** - распределенные транзакции
4. ✅ **Transaction Outbox** - гарантированная доставка событий
5. ✅ **Event-Driven** - асинхронное взаимодействие
6. ✅ **API Gateway** - единая точка входа
7. ✅ **JWT Authentication** - токен-базированная авторизация
8. ✅ **Redis Caching** - кеширование данных

## Порты

- **8000** - API Gateway
- **8001** - Auth Service
- **8002** - Catalog Service
- **8003** - Ordering Service
- **8004** - Payment Service
- **8005** - Delivery Service
- **5432** - PostgreSQL
- **6379** - Redis
- **5672** - RabbitMQ (AMQP)
- **15672** - RabbitMQ Management UI

