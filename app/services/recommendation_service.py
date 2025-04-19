from sklearn.cluster import KMeans
import numpy as np
from sqlalchemy.orm import Session
from ..models.models import Kullanici, Film, Tercih
from ..schemas.schemas import RecommendationResponse
from typing import List

class RecommendationService:
    def __init__(self, db: Session):
        self.db = db
        self.kmeans = KMeans(n_clusters=5, random_state=42)
        self.user_vectors = None
        self.user_clusters = None

    def _create_user_vectors(self):
        """Create user preference vectors for clustering"""
        users = self.db.query(Kullanici).all()
        genres = self._get_all_genres()
        
        user_vectors = []
        for user in users:
            vector = np.zeros(len(genres))
            preferences = self.db.query(Tercih).filter(Tercih.kullanici_id == user.id).all()
            
            for pref in preferences:
                if pref.tur in genres:
                    idx = genres.index(pref.tur)
                    vector[idx] = pref.puan
            
            user_vectors.append(vector)
        
        self.user_vectors = np.array(user_vectors)
        return self.user_vectors

    def _get_all_genres(self) -> List[str]:
        """Get all unique genres from the database"""
        movies = self.db.query(Film).all()
        genres = set()
        for movie in movies:
            genres.add(movie.tur)
        return list(genres)

    def train_model(self):
        """Train the KMeans model with user preference vectors"""
        if self.user_vectors is None:
            self._create_user_vectors()
        
        self.kmeans.fit(self.user_vectors)
        self.user_clusters = self.kmeans.labels_
        return self.user_clusters

    def get_recommendations(self, user_id: int, limit: int = 10) -> List[RecommendationResponse]:
        """Get movie recommendations for a user"""
        if self.user_clusters is None:
            self.train_model()
        
        # Get user's cluster
        user = self.db.query(Kullanici).filter(Kullanici.id == user_id).first()
        if not user:
            return []
        
        user_idx = user.id - 1  # Assuming user IDs start from 1
        user_cluster = self.user_clusters[user_idx]
        
        # Get movies watched by users in the same cluster
        cluster_users = [u.id for u, c in zip(self.db.query(Kullanici).all(), self.user_clusters) if c == user_cluster]
        
        # Get movies not watched by the target user
        watched_movies = [movie.id for movie in user.izlemeler]
        recommended_movies = []
        
        for cluster_user_id in cluster_users:
            cluster_user = self.db.query(Kullanici).filter(Kullanici.id == cluster_user_id).first()
            for movie in cluster_user.izlemeler:
                if movie.id not in watched_movies and movie not in recommended_movies:
                    recommended_movies.append(movie)
        
        # Sort by similarity score (using IMDB rating as a proxy)
        recommended_movies.sort(key=lambda x: x.imdb_puani, reverse=True)
        
        # Convert to response format
        recommendations = []
        for movie in recommended_movies[:limit]:
            recommendations.append(RecommendationResponse(
                film_id=movie.id,
                film_adi=movie.ad,
                tur=movie.tur,
                yil=movie.yil,
                imdb_puani=movie.imdb_puani,
                benzerlik_puani=movie.imdb_puani  # Using IMDB rating as similarity score
            ))
        
        return recommendations 