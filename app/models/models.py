from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

# Association table for many-to-many relationship between users and movies
user_movie_association = Table(
    'izlemeler',
    Base.metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('kullanici_id', Integer, ForeignKey('kullanicilar.id')),
    Column('film_id', Integer, ForeignKey('filmler.id')),
    Column('izleme_tarihi', DateTime, default=datetime.utcnow),
    Column('izlenme_suresi', Integer)  # in minutes
)

class Kullanici(Base):
    __tablename__ = "kullanicilar"

    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    yas = Column(Integer)
    cinsiyet = Column(String)
    
    # Relationships
    izlemeler = relationship("Film", secondary=user_movie_association, back_populates="izleyenler")
    tercihler = relationship("Tercih", back_populates="kullanici")

class Film(Base):
    __tablename__ = "filmler"

    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String, index=True)
    tur = Column(String)
    yil = Column(Integer)
    imdb_puani = Column(Float)
    
    # Relationships
    izleyenler = relationship("Kullanici", secondary=user_movie_association, back_populates="izlemeler")

class Tercih(Base):
    __tablename__ = "tercihler"

    id = Column(Integer, primary_key=True, index=True)
    kullanici_id = Column(Integer, ForeignKey('kullanicilar.id'))
    tur = Column(String)
    puan = Column(Float)
    
    # Relationships
    kullanici = relationship("Kullanici", back_populates="tercihler") 