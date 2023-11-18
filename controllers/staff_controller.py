from typing import Optional
from models.staff import Staff
import json


def load_staffs():
    try:
        with open('staffs.dat', 'r') as f:
            staff_data = json.load(f)
        return [Staff.from_dict(staff) for staff in staff_data]
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist
    except json.JSONDecodeError:
        return []  # Return an empty list if the file is empty or not valid JSON


def save_staffs(staffs):
    with open('staffs.dat', 'w') as f:
        # Ensure that we write an empty list to the file if there are no movies
        json.dump([staff.to_dict() for staff in staffs] or [], f)


def show_all_staffs():
    # Load movies and print all the details of the movie
    staffs = load_staffs()
    if not staffs:
        print("No Staffs Found")
        return

    # Define the table headers
    headers = ("Staff ID", "Name", "Email", "Password", "Address", "Country")
    # Find the maximum width for each column
    column_widths = [max(len(str(getattr(staff, attr))) for staff in staffs) for attr in headers]
    column_widths = [max(len(header), width) for header, width in zip(headers, column_widths)]

    # Print table header
    header_row = " | ".join(header.ljust(width) for header, width in zip(headers, column_widths))
    print(header_row)
    print("-" * len(header_row))  # Print a divider line

    # Print the staff rows
    for staff in staffs:
        staff_details = (
            str(staff.staff_id),
            staff.name,
            staff.email,
            '*' * len(staff.password),  # Replace password with asterisks for privacy
            staff.address,
            staff.country
        )
        row = " | ".join(detail.ljust(width) for detail, width in zip(staff_details, column_widths))
        print(row)


def register(name: str, email: str, password: str, address: Optional[str], country: Optional[str]):
    staffs = load_staffs()
    is_email_already_registered = any(staff.email == email for staff in staffs)
    if is_email_already_registered:
        print("Email already exists")
    else:
        staff_id = max(staff.staff_id for staff in staffs) + 1 if staffs else 1
        new_staff = Staff(staff_id=staff_id, name=name, email=email, password=password, address=address,
                                country=country)
        staffs.append(new_staff)
        save_staffs(staffs)
        print("Account Created Successfully!")


def delete_account(staff_id):
    staffs = load_staffs()
    staffs = [staff for staff in staffs if staff.movie_id != staff_id]
    save_staffs(staffs)


def update_profile(staff_id, name=None, email=None, password=None, address=None, country=None):
    staffs = load_staffs()
    staff = next((staff for staff in staffs if staff.staff_id == staff_id), None)
    # If the staff is found, update the fields
    if staff:
        if name is not None:
            staff.name = name
        if email is not None:
            staff.email = email
        if password is not None:
            staff.password = password
        if address is not None:
            staff.address = address
        if country is not None:
            staff.country = country
        # Call save_staffs to write the updates to the JSON file
        save_staffs(staffs)
        return True  # Return True to indicate success
    else:
        return False  # Return False if no staff was found with the given staff_id


def login(email: str, password: str):
    staffs = load_staffs()
    staff = next((staff for staff in staffs if staff.email == email), None)
    # If the staff is found, check the password
    if staff:
        if staff.password == password:
            print(f"Welcome "+staff.name)
            return True  # Return True to indicate success
        else:
            print("Password does not matched")
            return False  # Return False to indicate password does not matched.
    else:
        print("Account doesn't exists for this email")
        return False  # Return False to indicate account does not exist for this email

