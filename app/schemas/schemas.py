from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TercihBase(BaseModel):
    tur: str
    puan: float

class TercihCreate(TercihBase):
    pass

class Tercih(TercihBase):
    id: int
    kullanici_id: int

    class Config:
        from_attributes = True

class KullaniciBase(BaseModel):
    ad: str
    email: str
    yas: int
    cinsiyet: str

class KullaniciCreate(KullaniciBase):
    pass

class Kullanici(KullaniciBase):
    id: int
    tercihler: List[Tercih] = []

    class Config:
        from_attributes = True

class FilmBase(BaseModel):
    ad: str
    tur: str
    yil: int
    imdb_puani: float

class FilmCreate(FilmBase):
    pass

class Film(FilmBase):
    id: int

    class Config:
        from_attributes = True

class IzlemeBase(BaseModel):
    kullanici_id: int
    film_id: int
    izlenme_suresi: int

class IzlemeCreate(IzlemeBase):
    pass

class Izleme(IzlemeBase):
    id: int
    izleme_tarihi: datetime

    class Config:
        from_attributes = True

class RecommendationResponse(BaseModel):
    film_id: int
    film_adi: str
    tur: str
    yil: int
    imdb_puani: float
    benzerlik_puani: float 