from typing import Optional


class Staff:
    def __init__(self, staff_id: int, name: str, email: str, password: str, address: Optional[str] = None,
                 country: Optional[str] = None):
        self.staff_id: int = staff_id
        self.name: str = name
        self.email: str = email
        self.password: str = password
        self.address: str = address
        self.country: str = country

    def to_dict(self):
        return {
            "staff_id": self.staff_id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "address": self.address,
            "country": self.country
        }

    @staticmethod
    def from_dict(data):
        staff_id = data['staff_id']
        name = data['name']
        email = data['email']
        password = data['password']
        address = data.get('address', None)
        country = data.get('country', None)
        return Staff(staff_id=staff_id, name=name, email=email, password=password, address=address, country=country)
