from datetime import date, time, datetime
from typing import Optional


class Show:
    def __init__(self, show_id: int, show_date: date, show_time: time):
        self.show_id: int = show_id
        self.show_date: date = show_date
        self.show_time: time = show_time

    def to_dict(self):
        # Serialize the ShowTime to a dictionary
        return {
            'show_id': self.show_id,
            'show_date': self.show_date.strftime("%Y-%m-%d"),
            "show_time": self.show_time.strftime("%I:%M:%p")
        }

    @staticmethod
    def from_dict(data):
        # Deserialize a dictionary to a ShowTime object.
        return Show(
            show_id=data.get('show_id', None),
            show_date=datetime.strptime(data['show_date'], "%Y-%m-%d"),
            show_time=datetime.strptime(data['show_time'], "%I:%M:%p").time()
        )

