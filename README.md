#Projeyi Yapanlar
Gül ERTEN & Tuba SARIKAYA -- GYK1



# Netflix Benzeri Film/Dizi Öneri Sistemi

Bu proje, kullanıcıların izleme geçmişi ve tercihleri doğrultusunda film/dizi önerileri sunan bir API sistemidir. Netflix tarzı bir öneri motoru mantığıyla çalışır ve KMeans kümeleme algoritması kullanarak kişiselleştirilmiş öneriler sunar.

## Özellikler

- Kullanıcı profil yönetimi
- Film/dizi veritabanı
- İzleme geçmişi takibi
- Tür bazlı kullanıcı tercihleri
- KMeans algoritması ile kişiselleştirilmiş öneriler
- RESTful API endpoints

## Teknolojiler

- **Backend Framework:** FastAPI
- **Veritabanı:** PostgreSQL
- **ORM:** SQLAlchemy
- **Machine Learning:** scikit-learn (KMeans)
- **Veri İşleme:** Pandas, NumPy

## Kurulum

1. Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

2. PostgreSQL veritabanını oluşturun:
```sql
CREATE DATABASE "NetflixRecommendation";
```

3. `.env` dosyasını oluşturun ve veritabanı bağlantı bilgilerini ekleyin:
```env
DATABASE_URL=postgresql://postgres:{database şifrenizi buraya yazın}@localhost:5432/NetflixRecommendation
```

4. Örnek verileri yükleyin:
```bash
python create_database.py
```

5. Uygulamayı başlatın:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Kullanıcı İşlemleri
- `GET /kullanici/`: Tüm kullanıcıları listele
- `GET /kullanici/{user_id}`: Belirli bir kullanıcının bilgilerini getir
- `POST /kullanici/ekle`: Yeni kullanıcı ekle

### Film İşlemleri
- `GET /filmler/`: Tüm filmleri listele
- `GET /filmler/{movie_id}`: Belirli bir filmin bilgilerini getir
- `POST /filmler/`: Yeni film ekle
- `POST /filmler/izleme/kaydet`: Film izleme kaydı ekle

### Öneri Sistemi
- `GET /recommendations/{user_id}`: Kullanıcıya özel film önerileri al

## Kullanım Örnekleri

### Yeni Kullanıcı Ekleme
```json
POST /kullanici/ekle
{
    "ad": "Ahmet Yılmaz",
    "email": "ahmet@example.com",
    "yas": 25,
    "cinsiyet": "Erkek"
}
```

### Film İzleme Kaydı Ekleme
```json
POST /filmler/izleme/kaydet
{
    "kullanici_id": 1,
    "film_id": 1,
    "izlenme_suresi": 120
}
```

### Önerileri Görüntüleme
```
GET /recommendations/1
```

## Veritabanı Şeması

### Kullanicilar Tablosu
- id (Primary Key)
- ad
- email
- yas
- cinsiyet

### Filmler Tablosu
- id (Primary Key)
- ad
- tur
- yil
- imdb_puani

### Izlemeler Tablosu
- id (Primary Key)
- kullanici_id (Foreign Key)
- film_id (Foreign Key)
- izleme_tarihi
- izlenme_suresi

### Tercihler Tablosu
- id (Primary Key)
- kullanici_id (Foreign Key)
- tur
- puan

## Öneri Algoritması

Sistem, kullanıcıların film tercihleri ve izleme geçmişlerini analiz ederek KMeans kümeleme algoritması ile benzer kullanıcıları gruplar. Her kullanıcı için:
1. Tür bazlı tercih vektörü oluşturulur
2. Benzer kullanıcılar kümelenir
3. Kümedeki diğer kullanıcıların beğendiği ve hedef kullanıcının henüz izlemediği filmler önerilir

## Geliştirme

1. Repository'yi klonlayın
2. Gerekli paketleri yükleyin
3. Veritabanını oluşturun
4. Örnek verileri yükleyin
5. Uygulamayı başlatın


 