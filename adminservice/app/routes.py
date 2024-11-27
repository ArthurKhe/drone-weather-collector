from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer
from .dependencies import validate_token
from .database import get_db
from .models import Dron, DronData

router = APIRouter()


# Получить список дронов с пагинацией и фильтрацией
@router.get("/dron")
def get_drons(
    db: Session = Depends(get_db),
    token: str = Depends(validate_token),
    name: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100),
):
    query = db.query(Dron)
    if name:
        query = query.filter(Dron.name.ilike(f"%{name}%"))
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return {"total": total, "items": items}


# Создать новый дрон
@router.post("/dron")
def create_dron(
    name: str,
    description: Optional[str] = None,
    db: Session = Depends(get_db),
    token: str = Depends(validate_token),
):
    dron = Dron(name=name, description=description)
    db.add(dron)
    db.commit()
    db.refresh(dron)
    return dron


# Получить информацию о дроне по ID
@router.get("/dron/{id}")
def get_dron(
    id: int,
    db: Session = Depends(get_db),
    token: str = Depends(validate_token),
):
    dron = db.query(Dron).filter(Dron.id == id).first()
    if not dron:
        raise HTTPException(status_code=404, detail="Dron not found")
    return dron


# Обновить информацию о дроне
@router.patch("/dron/{id}")
def update_dron(
    id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    db: Session = Depends(get_db),
    token: str = Depends(validate_token),
):
    dron = db.query(Dron).filter(Dron.id == id).first()
    if not dron:
        raise HTTPException(status_code=404, detail="Dron not found")
    if name:
        dron.name = name
    if description:
        dron.description = description
    db.commit()
    db.refresh(dron)
    return dron


# Удалить дрон
@router.delete("/dron/{id}")
def delete_dron(
    id: int,
    db: Session = Depends(get_db),
    token: str = Depends(validate_token),
):
    dron = db.query(Dron).filter(Dron.id == id).first()
    if not dron:
        raise HTTPException(status_code=404, detail="Dron not found")
    db.delete(dron)
    db.commit()
    return {"detail": "Dron deleted"}


# Получить данные с дрона с фильтрацией и пагинацией
@router.get("/dron/{id}/data")
def get_dron_data(
    id: int = None,
    db: Session = Depends(get_db),
    token: str = Depends(validate_token),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100),
):
    query = db.query(DronData).filter(DronData.dron_id == id)
    if start_date:
        query = query.filter(DronData.timestamp >= start_date)
    if end_date:
        query = query.filter(DronData.timestamp <= end_date)
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return {"total": total, "items": items}
