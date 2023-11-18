from typing import List
from models.seat import Seat
from datetime import datetime


class ShowTime:
    def __init__(self, session_id: str, movie_id: str, show_time: datetime, seats: List[Seat]):
        self.session_id: str = session_id
        self.movie_id: str = movie_id
        self.seats: List[Seat] = seats
        self.show_time = show_time

    def to_dict(self):
        # Serialize the MovieSession to a dictionary, including the nested Seat objects.
        return {
            'session_id': self.session_id,
            'movie_id': self.movie_id,
            'seats': [seat.to_dict() for seat in self.seats],
            "show_time": self.show_time.strftime("%Y-%m-%d %I:%M:%p")

        }

    @classmethod
    def from_dict(cls, data, all_customers):
        # Deserialize a dictionary to a MovieSession object.
        # The all_customers list is needed to correctly associate seats with customers.
        seats = [Seat.from_dict(seat_data, all_customers) for seat_data in data['seats']]
        return cls(
            session_id=data['session_id'],
            movie_id=data['movie_id'],
            seats=seats,
            show_time=datetime.strptime(data['show_time'], "%Y-%m-%d %I:%M:%p")
        )

