from typing import Optional


class Customer:
    def __init__(self, cust_id: int, name: str, email: str, password: str, address: Optional[str] = None,
                 country: Optional[str] = None):
        self.cust_id: int = cust_id
        self.name: str = name
        self.email: str = email
        self.password: str = password
        self.address: str = address
        self.country: str = country

    def to_dict(self):
        return {
            "cust_id": self.cust_id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "address": self.address,
            "country": self.country
        }

    @staticmethod
    def from_dict(data):
        cust_id = data['cust_id']
        name = data['name']
        email = data['email']
        password = data['password']
        address = data.get('address', None)
        country = data.get('country', None)
        return Customer(cust_id=cust_id,name=name,email=email,password=password,address=address,country=country)
