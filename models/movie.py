from typing import List, Optional
from datetime import time, datetime


class Movie:
    """
    Movie will contain the name of movie, duration of movie in minutes, rating of movie, available showing times
    title: string
    duration: integer,
    rating: float,
    """
    def __init__(self, movie_id: int, title: str, duration: int,
                 rating: Optional[float] = None):
        self.movie_id: int = movie_id
        self.title: str = title
        self.duration: int = duration
        self.rating: Optional[float] = rating

    def to_dict(self):
        return {
            "movie_id": self.movie_id,
            "title": self.title,
            "duration": self.duration,
            "rating": self.rating,
        }

    @staticmethod
    def from_dict(data):
        movie_id = data['movie_id']
        title = data['title']
        duration = data['duration']
        rating = data.get('rating', None)
        return Movie(movie_id, title, duration, rating)
