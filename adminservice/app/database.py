from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# URL базы данных
DATABASE_URL = os.getenv("DATABASE_URL")

# Асинхронное подключение
database = Database(DATABASE_URL)

# Синхронное подключение
engine = create_engine(DATABASE_URL, echo=True)

# Сессии для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()


# Функция для создания всех таблиц
def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


# Зависимость для работы с сессиями базы данных
def get_db():
    """
    Генератор сессий базы данных для использования в FastAPI-зависимостях.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
