from models.customer import Customer

from typing import Optional


class Seat:
    def __init__(self, seat_number: int, is_reserved: bool = False, booked_by: Optional[Customer] = None):
        self.seat_number: int = seat_number
        self.is_reserved: bool = is_reserved
        self.booked_by: Optional[Customer] = booked_by

    def to_dict(self):
        # Convert the Seat instance to a dictionary for serialization.
        # If the seat is booked, we store the customer ID instead of the Customer object.
        return {
            'seat_number': self.seat_number,
            'is_reserved': self.is_reserved,
            'booked_by': self.booked_by.cust_id if self.booked_by else None
        }

    @staticmethod
    def from_dict(data, all_customers):
        # Convert a dictionary back to a Seat instance.
        # The all_customers parameter is a list of all Customer instances, used to find the Customer by ID.
        booked_by = next((cust for cust in all_customers if cust.cust_id == data['booked_by']), None)\
            if data['booked_by'] else None
        return Seat(
            seat_number=data['seat_number'],
            is_reserved=data['is_reserved'],
            booked_by=booked_by
        )

