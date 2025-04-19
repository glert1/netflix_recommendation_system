from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.models import Film, Kullanici
from ..schemas.schemas import FilmCreate, Film as FilmSchema, IzlemeCreate, Izleme as IzlemeSchema
from datetime import datetime

router = APIRouter(
    prefix="/filmler",
    tags=["filmler"]
)

@router.post("/", response_model=FilmSchema)
def create_movie(film: FilmCreate, db: Session = Depends(get_db)):
    db_film = Film(**film.dict())
    db.add(db_film)
    db.commit()
    db.refresh(db_film)
    return db_film

@router.get("/", response_model=List[FilmSchema])
def read_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movies = db.query(Film).offset(skip).limit(limit).all()
    return movies

@router.get("/{movie_id}", response_model=FilmSchema)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = db.query(Film).filter(Film.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Film bulunamadı")
    return db_movie

@router.post("/izleme/kaydet", response_model=IzlemeSchema)
def save_watching(izleme: IzlemeCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(Kullanici).filter(Kullanici.id == izleme.kullanici_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    # Check if movie exists
    movie = db.query(Film).filter(Film.id == izleme.film_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Film bulunamadı")
    
    # Add movie to user's watched movies
    user.izlemeler.append(movie)
    db.commit()
    
    return IzlemeSchema(
        id=len(user.izlemeler),
        kullanici_id=user.id,
        film_id=movie.id,
        izleme_tarihi=datetime.utcnow(),
        izlenme_suresi=izleme.izlenme_suresi
    ) 