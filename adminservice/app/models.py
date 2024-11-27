from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Text, func
from sqlalchemy.orm import relationship
from .database import Base


class Dron(Base):
    """
    Модель для описания дронов.
    """
    __tablename__ = "drons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())  # Автоматическая установка при создании
    updated_at = Column(DateTime, default=func.now(),
                        onupdate=func.now())  # Автообновление при изменении

    # Связь с таблицей данных дрона
    data = relationship("DronData", back_populates="dron", cascade="all, delete-orphan")


class DronData(Base):
    """
    Модель для описания данных, полученных с дронов.
    """
    __tablename__ = "dron_data"

    id = Column(Integer, primary_key=True, index=True)
    dron_id = Column(Integer, ForeignKey("drons.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    dron = relationship("Dron", back_populates="data")
