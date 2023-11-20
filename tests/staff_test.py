import unittest
from controllers.staff_controller import register, login


class TestStaffController(unittest.TestCase):

    def test_register_new_staff(self):
        result = register(name="Alice Smith", email="alice@example.com", password="securepassword", address="456 Avenue", country="Utopia")
        self.assertTrue(result)

    def test_login_existing_staff(self):
        result = login(email="alice@example.com", password="securepassword")
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
