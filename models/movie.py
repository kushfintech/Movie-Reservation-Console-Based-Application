from typing import List, Optional
from datetime import time, datetime

"""
Movie will contain the name of movie, duration of movie in minutes, rating of movie, available showing times
title: string
duration: integer,
rating: float,
showing_times: List[time]
"""


class Movie:
    def __init__(self, movie_id: int, title: str, duration: int, showing_times: List[datetime],
                 rating: Optional[float] = None):
        self.movie_id: int = movie_id
        self.title: str = title
        self.duration: int = duration
        self.rating: Optional[float] = rating
        self.showing_times: List[datetime] = showing_times

    def to_dict(self):
        return {
            "movie_id": self.movie_id,
            "title": self.title,
            "duration": self.duration,
            "rating": self.rating,
            "showing_times": [show_time.strftime("%Y-%m-%d %H:%M:%S") for show_time in self.showing_times]
        }

    @staticmethod
    def from_dict(data):
        movie_id = data['movie_id']
        title = data['title']
        duration = data['duration']
        rating = data.get('rating', None)
        showing_times = [datetime.strptime(show_time, "%Y-%m-%d %H:%M:%S") for show_time in data['showing_times']]
        return Movie(movie_id, title, duration, showing_times, rating)
