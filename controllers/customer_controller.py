from typing import Optional

import inquirer

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
    customers = load_customers()
    if not customers:
        print("No Customers Found")
        return

    # Define the table headers and corresponding attribute names in the Customer class
    headers = ["Customer ID", "Name", "Email", "Address", "Country"]
    attributes = ["cust_id", "name", "email", "address", "country"]  # Update these according to your Customer class

    # Calculate the maximum width for each column
    column_widths = [
        max(len(header), max((len(str(getattr(customer, attr))) for customer in customers), default=0))
        for header, attr in zip(headers, attributes)
    ]

    # Print table header
    header_row = " | ".join(header.ljust(column_widths[idx]) for idx, header in enumerate(headers))
    print(header_row)
    print("-" * len(header_row))  # Print a divider line

    # Print the customer rows
    for customer in customers:
        customer_details = [str(getattr(customer, attr)) for attr in attributes]
        row = " | ".join(detail.ljust(column_widths[idx]) for idx, detail in enumerate(customer_details))
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
    customers = [customer for customer in customers if customer.cust_id != cust_id]
    save_customers(customers)
    return True


def update_profile(cust_id, name=None, email=None, password=None, address=None, country=None):
    customers = load_customers()
    customer = next((cust for cust in customers if cust.cust_id == cust_id), None)
    # If the customer is found, update the fields
    if customer:
        if name is not "":
            customer.name = name
        if email is not "":
            customer.email = email
        if password is not "":
            customer.password = password
        if address is not "":
            customer.address = address
        if country is not "":
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


def get_cust_id():
    customers = load_customers()
    customer_choices = [(f"{customer.cust_id} - {customer.name} - {customer.email}", customer.cust_id) for customer in customers]

    # Ask the user to select a movie
    customer_question = [
        inquirer.List('customer',
                      message="Select Customer",
                      choices=customer_choices,
                      carousel=True)
    ]
    selected_cust_id = inquirer.prompt(customer_question)['customer']
    return selected_cust_id


def get_customer_by_id(customer_id):
    customers = load_customers()
    # Find the customer with the given customer_id
    customer = next((cust for cust in customers if cust.cust_id == customer_id), None)
    if customer is not None:
        return customer
    else:
        print(f"No customer found with ID {customer_id}")
        return None


def show_customer_details_by_id(cust_id):
    # Load customers
    customers = load_customers()  # Assuming this function is defined to load customer data

    # Find the customer with the given ID
    customer = next((cust for cust in customers if str(cust.cust_id) == cust_id), None)
    if not customer:
        print(f"No customer found with ID {cust_id}")
        return

    # Prepare customer data for display
    customer_data = {
        "Customer ID": customer.cust_id,
        "Name": customer.name,
        "Email": customer.email,
        "Address": customer.address,
        "Country": customer.country
        # Add other relevant fields as necessary
    }

    # Define table headers
    headers = customer_data.keys()

    # Calculate column widths
    column_widths = {header: max(len(header), len(str(customer_data[header]))) for header in headers}

    # Print table header
    header_row = " | ".join(header.ljust(column_widths[header]) for header in headers)
    print(header_row)
    print("-" * len(header_row))

    # Print customer details
    row = " | ".join(str(customer_data[header]).ljust(column_widths[header]) for header in headers)
    print(row)

