from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base, Kullanici, Film, Tercih
from datetime import datetime

# Veritabanı bağlantısı
DATABASE_URL = "postgresql://postgres:{db_password}@localhost:5432/NetflixRecommendation"
engine = create_engine(DATABASE_URL)

# Tabloları oluştur
Base.metadata.create_all(bind=engine)

# Session oluştur
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Örnek veriler
kullanicilar = [
    Kullanici(ad="Ahmet Yılmaz", email="ahmet@example.com", yas=25, cinsiyet="Erkek"),
    Kullanici(ad="Ayşe Demir", email="ayse@example.com", yas=30, cinsiyet="Kadın"),
    Kullanici(ad="Mehmet Kaya", email="mehmet@example.com", yas=28, cinsiyet="Erkek"),
    Kullanici(ad="Zeynep Şahin", email="zeynep@example.com", yas=22, cinsiyet="Kadın"),
    Kullanici(ad="Ali Öztürk", email="ali@example.com", yas=35, cinsiyet="Erkek")
]

filmler = [
    Film(ad="Inception", tur="Bilim Kurgu", yil=2010, imdb_puani=8.8),
    Film(ad="The Dark Knight", tur="Aksiyon", yil=2008, imdb_puani=9.0),
    Film(ad="Pulp Fiction", tur="Suç", yil=1994, imdb_puani=8.9),
    Film(ad="The Shawshank Redemption", tur="Drama", yil=1994, imdb_puani=9.3),
    Film(ad="Fight Club", tur="Drama", yil=1999, imdb_puani=8.8),
    Film(ad="The Matrix", tur="Bilim Kurgu", yil=1999, imdb_puani=8.7),
    Film(ad="Interstellar", tur="Bilim Kurgu", yil=2014, imdb_puani=8.6),
    Film(ad="The Godfather", tur="Suç", yil=1972, imdb_puani=9.2),
    Film(ad="Forrest Gump", tur="Drama", yil=1994, imdb_puani=8.8),
    Film(ad="The Silence of the Lambs", tur="Gerilim", yil=1991, imdb_puani=8.6)
]

tercihler = [
    Tercih(kullanici_id=1, tur="Bilim Kurgu", puan=4.5),
    Tercih(kullanici_id=1, tur="Aksiyon", puan=4.0),
    Tercih(kullanici_id=2, tur="Drama", puan=4.8),
    Tercih(kullanici_id=2, tur="Romantik", puan=4.2),
    Tercih(kullanici_id=3, tur="Aksiyon", puan=4.7),
    Tercih(kullanici_id=3, tur="Bilim Kurgu", puan=4.3),
    Tercih(kullanici_id=4, tur="Drama", puan=4.6),
    Tercih(kullanici_id=4, tur="Gerilim", puan=4.4),
    Tercih(kullanici_id=5, tur="Suç", puan=4.9),
    Tercih(kullanici_id=5, tur="Aksiyon", puan=4.5)
]

# Verileri veritabanına ekle
try:
    # Kullanıcıları ekle
    for kullanici in kullanicilar:
        db.add(kullanici)
    db.commit()

    # Filmleri ekle
    for film in filmler:
        db.add(film)
    db.commit()

    # Tercihleri ekle
    for tercih in tercihler:
        db.add(tercih)
    db.commit()

    # Bazı izleme kayıtları ekle
    kullanici1 = db.query(Kullanici).filter(Kullanici.id == 1).first()
    kullanici1.izlemeler.extend([filmler[0], filmler[1], filmler[5]])  # Inception, The Dark Knight, The Matrix

    kullanici2 = db.query(Kullanici).filter(Kullanici.id == 2).first()
    kullanici2.izlemeler.extend([filmler[3], filmler[8]])  # The Shawshank Redemption, Forrest Gump

    kullanici3 = db.query(Kullanici).filter(Kullanici.id == 3).first()
    kullanici3.izlemeler.extend([filmler[1], filmler[5], filmler[6]])  # The Dark Knight, The Matrix, Interstellar

    db.commit()
    print("Veritabanı başarıyla oluşturuldu ve örnek veriler eklendi!")

except Exception as e:
    db.rollback()
    print(f"Hata oluştu: {e}")
finally:
    db.close() 