from typing import List
from models.seat import Seat
from models.show import Show


class MovieSession:
    def __init__(self, session_id: int, movie_id: str, show: Show, seats: List[Seat], status: str = "AVAILABLE"):
        self.session_id: int = session_id
        self.movie_id: str = movie_id
        self.seats: List[Seat] = seats
        self.show: Show = show
        self.status: str = status

    def to_dict(self):
        # Serialize the MovieSession to a dictionary, including the nested Seat objects.
        return {
            'session_id': self.session_id,
            'movie_id': self.movie_id,
            'seats': [seat.to_dict() for seat in self.seats],
            "show": self.show.to_dict(),
            "status": self.status
        }

    @staticmethod
    def from_dict(data, all_customers):
        # Deserialize a dictionary to a MovieSession object.
        seats = [Seat.from_dict(seat_data, all_customers) for seat_data in data['seats']]
        return MovieSession(
            session_id=data['session_id'],
            movie_id=data['movie_id'],
            seats=seats,
            show=Show.from_dict(data['show']),
            status=data['status']
        )
