from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.models import Kullanici
from ..schemas.schemas import KullaniciCreate, Kullanici as KullaniciSchema

router = APIRouter(
    prefix="/kullanici",
    tags=["kullanicilar"]
)

@router.post("/ekle", response_model=KullaniciSchema)
def create_user(kullanici: KullaniciCreate, db: Session = Depends(get_db)):
    db_user = Kullanici(**kullanici.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=KullaniciSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(Kullanici).filter(Kullanici.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    return db_user

@router.get("/", response_model=List[KullaniciSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(Kullanici).offset(skip).limit(limit).all()
    return users 