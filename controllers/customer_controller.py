from typing import Optional
from models.customer import Customer
import json


def load_customers():
    try:
        with open('customers.dat', 'r') as f:
            customer_data = json.load(f)
        return [Customer.from_dict(customer) for customer in customer_data]
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist
    except json.JSONDecodeError:
        return []  # Return an empty list if the file is empty or not valid JSON


def save_customers(customers):
    with open('customers.dat', 'w') as f:
        # Ensure that we write an empty list to the file if there are no movies
        json.dump([customer.to_dict() for customer in customers] or [], f)


def show_all_customers():
    # Load movies and print all the details of the movie
    customers = load_customers()
    if not customers:
        print("No Customers Found")
        return

    # Define the table headers
    headers = ("Customer ID", "Name", "Email", "Password", "Address", "Country")

    # Find the maximum width for each column
    column_widths = [max(len(str(getattr(customer, attr))) for customer in customers) for attr in headers]
    column_widths = [max(len(header), width) for header, width in zip(headers, column_widths)]

    # Print table header
    header_row = " | ".join(header.ljust(width) for header, width in zip(headers, column_widths))
    print(header_row)
    print("-" * len(header_row))  # Print a divider line

    # Print the customer rows
    for customer in customers:
        customer_details = (
            str(customer.cust_id),
            customer.name,
            customer.email,
            '*' * len(customer.password),  # Replace password with asterisks for privacy
            customer.address,
            customer.country
        )
        row = " | ".join(detail.ljust(width) for detail, width in zip(customer_details, column_widths))
        print(row)


def register(name: str, email: str, password: str, address: Optional[str], country: Optional[str]):
    customers = load_customers()
    is_email_already_registered = any(customer.email == email for customer in customers)
    if is_email_already_registered:
        print("Email already exists")
    else:
        cust_id = max(customer.cust_id for customer in customers) + 1 if customers else 1
        new_customer = Customer(cust_id=cust_id, name=name, email=email, password=password, address=address,
                                country=country)
        customers.append(new_customer)
        save_customers(customers)
        print("Account Created Successfully!")


def delete_account(cust_id):
    customers = load_customers()
    customers = [customer for customer in customers if customer.movie_id != cust_id]
    save_customers(customers)


def update_profile(cust_id, name=None, email=None, password=None, address=None, country=None):
    customers = load_customers()
    customer = next((cust for cust in customers if cust.cust_id == cust_id), None)
    # If the customer is found, update the fields
    if customer:
        if name is not None:
            customer.name = name
        if email is not None:
            customer.email = email
        if password is not None:
            customer.password = password
        if address is not None:
            customer.address = address
        if country is not None:
            customer.country = country
        # Call save_customers to write the updates to the JSON file
        save_customers(customers)
        return True  # Return True to indicate success
    else:
        return False  # Return False if no customer was found with the given cust_id


def login(email: str, password: str):
    customers = load_customers()
    customer = next((cust for cust in customers if cust.email == email), None)
    # If the customer is found, check the password
    if customer:
        if customer.password == password:
            return True  # Return True to indicate success
        else:
            print("Password does not matched")
            return False  # Return False to indicate password does not matched.
    else:
        print("Account doesn't exists for this email")
        return False  # Return False to indicate account does not exist for this email

