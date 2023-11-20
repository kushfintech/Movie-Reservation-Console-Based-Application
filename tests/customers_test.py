import unittest
from controllers.customer_controller import register, login


class TestCustomerController(unittest.TestCase):

    def test_register_new_customer(self):
        result = register(name="John Doe", email="johndoe@example.com", password="password123", address="123 Street", country="Wonderland")
        self.assertTrue(result)

    def test_login_existing_customer(self):
        result = login(email="johndoe@example.com", password="password123")
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
