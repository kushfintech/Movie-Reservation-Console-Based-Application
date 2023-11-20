from models.customer import Customer
from models.movie_session import MovieSession
from models.seat import Seat
from models.show import Show

from typing import List
from datetime import datetime


class Reservation:
    def __init__(self, reservation_id: int, customer: Customer, movie_session: MovieSession, seats: List[Seat],
                 reserved_datetime: datetime, status: str):
        self.reservation_id: int = reservation_id
        self.customer: Customer = customer
        self.movie_session: MovieSession = movie_session
        self.seats: List[Seat] = seats
        self.reserved_datetime: datetime = reserved_datetime
        self.status: str = status

    def to_dict(self):
        return {
            'reservation_id': self.reservation_id,
            'customer_id': self.customer.cust_id,
            'movie_session': self.movie_session.session_id,
            'seats': [seat.to_dict() for seat in self.seats],
            'reserved_datetime': self.reserved_datetime.strftime("%Y-%m-%d %I:%M:%p"),
            'status': self.status,
        }

    @classmethod
    def from_dict(cls, data, all_customers, all_movies_sessions, all_shows):
        reservation_id = data["reservation_id"]
        customer = next((cust for cust in all_customers if cust.cust_id == data['customer_id']), None)
        movie_session = next((session for session in all_movies_sessions if session.session_id ==
                              data['movie_session']), None)
        seats = [Seat.from_dict(seat_data, all_customers) for seat_data in data.get('seats', [])]
        reserved_datetime = datetime.strptime(data['reserved_datetime'], "%Y-%m-%d %I:%M:%p")
        status = data["status"]

        return cls(reservation_id, customer, movie_session, seats, reserved_datetime, status)
