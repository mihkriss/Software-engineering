from datetime import datetime

USERS_DATA = [
    {
        "username": "Иван Иванов",
        "role": "admin",
        "login": "admin",
        "password": "secret"
    },
    {
        "username": "Иван Петров",
        "role": "speaker",
        "login": "ivan11",
        "password": "speaker123"
    },

    {
        "username": "Елена Смирнова",
        "role": "speaker",
        "login": "elena11",
        "password": "elena11"
    },

    {
        "username": "Алексей Воронов",
        "role": "speaker",
        "login": "alex11",
        "password": "alex11"
    },

    {
        "username": "Николай Семенов",
        "role": "guest",
        "login": "nikolai123",
        "password": "nikolai123"
    },

    {
        "username": "Наталия Покрова",
        "role": "guest",
        "login": "nataliyat2",
        "password": "nataliyat2"
    },
    
    {
        "username": "Кирилл Лукошко",
        "role": "guest",
        "login": "kirill_lu",
        "password": "kirill_lu123"
    }
]

ROOMS_DATA = [
    {"title": "Room 1"},
    {"title": "Room 2"},
    {"title": "Room 3"}
]

DOCLADS_DATA = [
    {
        "title": "Как построить микросервис",
        "author": "Иван Петров",
        "content": "Рассматриваем архитектуру микросервисов",
        "room_id": 1,
        "created_at": datetime.utcnow()
    },
    {
        "title": "ML в промышленности",
        "author": "Елена Смирнова",
        "content": "Как применять машинное обучение на практике",
        "room_id": 2,
        "created_at": datetime.utcnow()
    },
    {
        "title": "DevOps практика",
        "author": "Алексей Воронов",
        "content": "CI/CD, Docker и Kubernetes",
        "room_id": 3,
        "created_at": datetime.utcnow()
    },
    {
        "title": "Искусственный интеллект в медицине",
        "author": "Иван Петров",
        "content": "Примеры использования ИИ в диагностике и лечении",
        "room_id": 1,
        "created_at": datetime.utcnow()
    },
    {
        "title": "Современные методы машинного обучения",
        "author": "Елена Смирнова",
        "content": "Глубокое обучение, ансамбли, transfer learning",
        "room_id": None,
        "created_at": datetime.utcnow()
    },
    {
        "title": "Будущее IT-инфраструктуры",
        "author": "Алексей Воронов",
        "content": "Облачные технологии и serverless-архитектура",
        "room_id": 2,
        "created_at": datetime.utcnow()
    },
    {
        "title": "Интернет вещей (IoT)",
        "author": "Елена Смирнова",
        "content": "Как соединить реальный мир с цифровым",
        "room_id": 3,
        "created_at": datetime.utcnow()
    }
]