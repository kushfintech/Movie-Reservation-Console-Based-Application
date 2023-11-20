import json
from datetime import datetime
from typing import List
import inquirer

from models.reservation import Reservation
from controllers.customer_controller import load_customers, get_customer_by_id
from controllers.movie_controller import load_movies
from controllers.movie_session_controller import (get_all_shows_of_all_sessions, load_sessions, get_movie_session_by_id,
                                                  save_sessions)


def save_reservations(reservations):
    try:
        # Convert the reservations to a list of dictionaries
        reservations_data = [reservation.to_dict() for reservation in reservations]

        # Write the data to a file
        with open('reservations.dat', 'w') as file:
            json.dump(reservations_data, file, indent=4)

        print("Reservations saved successfully.")
    except Exception as e:
        print(f"An error occurred while saving reservations: {e}")


def load_reservations():
    try:
        # Assuming you store your reservations in 'reservations.dat'
        with open('reservations.dat', 'r') as f:
            reservations_data = json.load(f)

        # Load all related data
        all_customers = load_customers()  # You need to define this function
        all_movies_sessions = load_sessions()  # You need to define this function
        all_shows = get_all_shows_of_all_sessions()  # You need to define this function

        # Convert list of dictionaries to list of Reservation objects
        reservations = [
            Reservation.from_dict(
                reservation_data,
                all_customers,
                all_movies_sessions,
                all_shows
            ) for reservation_data in reservations_data
        ]

        return reservations
    except FileNotFoundError:
        # If the reservations file doesn't exist, return an empty list
        return []
    except json.JSONDecodeError:
        # If the file is not valid JSON (e.g., it's empty), return an empty list
        return []


def view_reservations():
    # Load reservations (assuming this is a function you have that loads all reservations)
    reservations = load_reservations()

    if len(reservations) <= 0:
        print("No reservations found")
        return None

    # Define the table headers
    headers = [
        "Reservation ID", "Customer ID", "Customer Name", "Movie ID",
        "Movie Title", "Reserved Seats", "Show Date", "Show Time", "Reserved Datetime"
    ]

    # Retrieve additional information like customer names and movie titles
    all_customers = load_customers()  # Load all customers
    all_movies = load_movies()  # Load all movies

    # Prepare rows for each reservation
    rows = []
    for reservation in reservations:
        customer = next((cust for cust in all_customers if cust.cust_id == reservation.customer.cust_id), None)
        movie = next((mv for mv in all_movies if mv.movie_id == reservation.movie_session.movie_id), None)

        row = {
            "Reservation ID": reservation.reservation_id,
            "Customer ID": reservation.customer.cust_id,
            "Customer Name": customer.name if customer else "Unknown",
            "Movie ID": reservation.movie_session.movie_id,
            "Movie Title": movie.title if movie else "Unknown",
            "Reserved Seats": [seat.seat_number for seat in reservation.seats],
            "Show Date": reservation.movie_session.show.show_date.strftime("%Y-%m-%d") if reservation.movie_session.show else "N/A",
            "Show Time": reservation.movie_session.show.show_time.strftime("%I:%M %p") if reservation.movie_session.show else "N/A",
            "Reserved Datetime": reservation.reserved_datetime.strftime("%Y-%m-%d %I:%M %p")
        }
        rows.append(row)

    # Find the maximum width for each column
    column_widths = {header: max(len(header), max(len(str(row[header])) for row in rows)) for header in headers}

    # Print table header
    header_row = " | ".join(header.ljust(column_widths[header]) for header in headers)
    print(header_row)
    print("-" * len(header_row))

    # Print each reservation row
    for row in rows:
        print(" | ".join(str(row[header]).ljust(column_widths[header]) for header in headers))


def generate_new_reservation_id(reservations: List[Reservation]):
    session_id = max(reservation.reservation_id for reservation in reservations) + 1 if reservations else 1
    return session_id


def add_reservation(customer_id, movie_session_id, seat_numbers):
    # Load existing data
    reservations = load_reservations()
    movie_sessions = load_sessions()  # Assuming this function is defined

    # Find the requested movie session
    movie_session = next((session for session in movie_sessions if session.session_id == movie_session_id), None)
    if movie_session is None:
        print(f"No movie session found with ID {movie_session_id}")
        return False

    selected_seats = []
    # Reserve the seats
    for seat in movie_session.seats:
        if str(seat.seat_number) in seat_numbers:
            if seat.is_reserved:
                print(f"Seat {seat.seat_number} is already reserved.")
                return False
            else:
                seat.is_reserved = True
                seat.booked_by = get_customer_by_id(customer_id)
                selected_seats.append(seat)

    reservation_id = generate_new_reservation_id(reservations)

    # Create a new reservation with a unique ID
    new_reservation = Reservation(
        reservation_id=reservation_id,
        customer=get_customer_by_id(customer_id),
        movie_session=get_movie_session_by_id(movie_session_id),
        seats=selected_seats,
        reserved_datetime=datetime.now(),
        status="RESERVED"
    )
    reservations.append(new_reservation)

    # Save the updated reservations
    save_reservations(reservations)
    save_sessions(movie_sessions)

    print(f"Reservation added successfully with no {new_reservation.reservation_id}.")
    return True


def cancel_reservation(reservation_id):
    # Load existing data
    reservations = load_reservations()
    movie_sessions = load_sessions()

    # Find the reservation to cancel
    reservation = next((res for res in reservations if res.reservation_id == reservation_id), None)
    if reservation is None:
        print(f"No reservation found with ID {reservation_id}")
        return False

    # Change the reservation status to 'cancelled'
    reservation.status = 'CANCELLED'

    # Find the corresponding movie session
    movie_session = next((session for session in movie_sessions if session.session_id ==
                          reservation.movie_session.session_id),
                         None)
    if not movie_session:
        print(f"No movie session found for reservation ID {reservation_id}")
        return False

    # Update the seat status in the movie session
    for seat in movie_session.seats:
        if seat.seat_number in [s.seat_number for s in reservation.seats]:
            seat.is_reserved = False

    # Save the updated reservations and movie sessions
    save_reservations(reservations)
    save_sessions(movie_sessions)

    print("Reservation cancelled successfully.")
    return True


def check_and_show_reservation_details_of_customer(reservation_id, customer_id):
    # Load reservations, customers, and movie sessions
    reservations = load_reservations()
    customers = load_customers()
    movie_sessions = load_sessions()

    # Find the reservation
    reservation = next((r for r in reservations if r.reservation_id == reservation_id), None)
    if not reservation or reservation.customer.cust_id != customer_id:
        print(f"No valid reservation found for Reservation ID: {reservation_id} and Customer ID: {customer_id}")
        return

    # Find the customer and movie session details
    customer = next((c for c in customers if c.cust_id == customer_id), None)
    movie_session = next((ms for ms in movie_sessions if ms.session_id == reservation.movie_session.session_id), None)

    if not customer or not movie_session:
        print("Error fetching reservation details.")
        return

    # Define table headers
    headers = ["Reservation ID", "Customer ID", "Customer Name", "Movie Title", "Session Date", "Session Time", "Seats", "Availability", "Booked By"]
    reservation_data = {
        "Reservation ID": reservation.reservation_id,
        "Customer ID": customer.cust_id,
        "Customer Name": customer.name,
        "Movie Title": movie_session.movie.title,
        "Session Date": movie_session.show.show_date.strftime("%Y-%m-%d"),
        "Session Time": movie_session.show.show_time.strftime("%I:%M %p"),
        "Seats": ", ".join([seat.seat_number for seat in reservation.seats_reserved]),
        "Availability": "RESERVED" if all(seat.is_reserved for seat in reservation.seats_reserved) else "AVAILABLE",
        "Booked By": customer.name
    }

    # Calculate column widths
    column_widths = {header: max(len(header), len(str(reservation_data[header]))) for header in headers}

    # Print table header
    header_row = " | ".join(header.ljust(column_widths[header]) for header in headers)
    print(header_row)
    print("-" * len(header_row))

    # Print reservation details
    row = " | ".join(str(reservation_data[header]).ljust(column_widths[header]) for header in headers)
    print(row)


def show_reservation_details_by_id(reservation_id):
    # Load reservations and other necessary data
    reservations = load_reservations()
    customers = load_customers()
    movie_sessions = load_sessions()
    all_movies = load_movies()

    # Find the reservation
    reservation = next((r for r in reservations if str(r.reservation_id) == reservation_id), None)
    if not reservation:
        print(f"No reservation found for Reservation ID: {reservation_id}")
        return

    # Find additional details
    customer = next((c for c in customers if c.cust_id == reservation.customer.cust_id), None)
    movie_session = next((ms for ms in movie_sessions if ms.session_id == reservation.movie_session.session_id), None)
    movie = next((mv for mv in all_movies if mv.movie_id == reservation.movie_session.movie_id), None)

    if not customer or not movie_session:
        print("Error fetching reservation details.")
        return

    reservation_data = {
        "Reservation ID": reservation.reservation_id,
        "Customer ID": reservation.customer.cust_id,
        "Customer Name": customer.name if customer else "Unknown",
        "Movie ID": reservation.movie_session.movie_id,
        "Movie Title": movie.title if movie else "Unknown",
        "Reserved Seats": [seat.seat_number for seat in reservation.seats],
        "Show Date": reservation.movie_session.show.show_date.strftime(
            "%Y-%m-%d") if reservation.movie_session.show else "N/A",
        "Show Time": reservation.movie_session.show.show_time.strftime(
            "%I:%M %p") if reservation.movie_session.show else "N/A",
        "Reserved Datetime": reservation.reserved_datetime.strftime("%Y-%m-%d %I:%M %p")
    }

    # Print table
    headers = reservation_data.keys()
    column_widths = {header: max(len(header), len(str(reservation_data[header]))) for header in headers}
    header_row = " | ".join(header.ljust(column_widths[header]) for header in headers)
    print(header_row)
    print("-" * len(header_row))
    row = " | ".join(str(reservation_data[header]).ljust(column_widths[header]) for header in headers)
    print(row)


def select_reservation():
    # Load reservations, assuming this function returns a list of Reservation objects
    reservations = load_reservations()
    all_movies = load_movies()

    if not reservations:
        print("No reservations found.")
        return None

    # Create a list of choices for inquirer, each choice should have enough information to identify the reservation
    reservation_choices = [
        (f"ID: {res.reservation_id}, Date: {res.movie_session.show.show_date}, Time: {res.movie_session.show.show_time}, "
         f"Customer: {res.customer.name}", res.reservation_id)
        for res in reservations
    ]

    post_special_options = [("Cancel", "CANCEL")]
    choices = reservation_choices + post_special_options

    question = [
        inquirer.List('reservation',
                      message="Select a reservation:",
                      choices=choices,
                      carousel=True)
    ]

    # Prompt the user to choose a reservation
    answers = inquirer.prompt(question)

    # Find and return the selected reservation
    selected_reservation_id = answers['reservation']
    if selected_reservation_id == "CANCEL":
        return None
    else:
        return next((res for res in reservations if res.reservation_id == selected_reservation_id), None)


def delete_reservation(reservation_id):
    # Load existing reservations
    reservations = load_reservations()  # Make sure this function is defined to load reservations

    # Find and remove the reservation with the given ID
    reservations = [res for res in reservations if res.reservation_id != reservation_id]

    # Save the updated list of reservations
    save_reservations(reservations)  # Make sure this function is defined to save reservations

    print(f"Reservation with ID {reservation_id} has been removed.")
