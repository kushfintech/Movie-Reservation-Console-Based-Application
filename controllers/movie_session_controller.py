import inquirer

from models.movie_session import MovieSession
from models.seat import Seat
from controllers.customer_controller import load_customers
from controllers.movie_controller import load_movies, format_show_time_for_display, get_movie_using_id
from datetime import datetime
import json


def load_sessions():
    try:
        with open('seats.dat', 'r') as f:
            sessions_data = json.load(f)
            customers = load_customers()
        return [MovieSession.from_dict(movie, customers) for movie in sessions_data]
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist
    except json.JSONDecodeError:
        return []  # Return an empty list if the file is empty or not valid JSON


def save_sessions(sessions):
    with open('seats.dat', 'w') as f:
        # Ensure that we write an empty list to the file if there are no movies
        json.dump([session.to_dict() for session in sessions] or [], f)


def show_all_sessions():
    movie_sessions = load_sessions()
    all_movies = load_movies()
    if not movie_sessions:
        print("No Movie Sessions Found")
        return

    # Define the table headers
    headers = ["Session ID", "Movie Name", "Show Time", "Total Seats", "Available Seats"]

    # Calculate the maximum width for each column
    column_widths = {
        "Session ID": max(len(headers[0]), max(len(str(session.session_id)) for session in movie_sessions)),
        "Movie Name": max(len(headers[1]), max(len(next((movie.title for movie in all_movies if movie.movie_id == session.movie_id), "Unknown")) for session in movie_sessions)),
        "Show Time": max(len(headers[2]), max(len(session.show_time.strftime("%Y-%m-%d %H:%M:%S")) for session in movie_sessions)),
        "Total Seats": max(len(headers[3]), max(len(str(len(session.seats))) for session in movie_sessions)),
        "Available Seats": max(len(headers[4]), max(len(f"{sum(not seat.is_reserved for seat in session.seats)}/{len(session.seats)}") for session in movie_sessions))
    }

    # Print table header
    header_row = " | ".join(header.ljust(column_widths[header]) for header in headers)
    print(header_row)
    print("-" * len(header_row))  # Print a divider line

    # Print the movie session rows
    for session in movie_sessions:
        movie_name = next((movie.title for movie in all_movies if movie.movie_id == session.movie_id), "Unknown")
        total_seats = len(session.seats)
        available_seats = sum(not seat.is_reserved for seat in session.seats)
        session_details = [
            str(session.session_id).ljust(column_widths["Session ID"]),
            movie_name.ljust(column_widths["Movie Name"]),
            session.show_time.strftime("%I:%M:%p").ljust(column_widths["Show Time"]),
            str(total_seats).ljust(column_widths["Total Seats"]),
            f"{available_seats}/{total_seats}".ljust(column_widths["Available Seats"])
        ]
        row = " | ".join(session_details)
        print(row)



def parse_str_to_time(time_str):
    # Define the format for the time string
    time_format = "%I:%M %p"  # or "%I:%M %p" for 12-hour format with AM/PM
    try:
        return datetime.strptime(time_str, time_format).time()
    except ValueError:
        print(f"Time '{time_str}' is not in the correct format.")
        return None


def add_session(movie_id, show_time: datetime, total_seats):
    sessions = load_sessions()
    session_id = max(session.session_id for session in sessions) + 1 if sessions else 1
    seats = [Seat(seat_number=str(i+1), is_reserved=False) for i in range(total_seats)]
    new_session = MovieSession(session_id=session_id,movie_id=movie_id,show_time=show_time,seats= seats)
    sessions.append(new_session)
    save_sessions(sessions)
    print("Session Added Successfully!")


def remove_session(session_id):
    sessions = load_sessions()
    sessions = [session for session in sessions if session.session_id != session_id]
    save_sessions(sessions)
    show_all_sessions()


def get_session_id_using_interactive_console():
    sessions = load_sessions()
    # Ensure that all_movies is loaded only once, to optimize performance
    all_movies = load_movies()

    session_choices = [
        (f"{get_movie_using_id(session.movie_id).title} - {format_show_time_for_display(session.show_time)}", session.session_id)
        for session in sessions
    ]

    # Ask the user to select a session
    session_question = [
        inquirer.List('session',
                      message="Which session would you like to select?",
                      choices=session_choices,
                      carousel=True)
    ]
    selected_session_info = inquirer.prompt(session_question)['session']
    # The selected_session_info is now the session_id because that's what we paired with the label in the choices tuple
    return selected_session_info

#
# def add_showing_time(movie_id, time):
#     movies = load_movies()
#     for movie in movies:
#         if movie.movie_id == movie_id:
#             movie.showing_times.append(parse_showing_time(time))
#     save_movies(movies)
#
#
# def remove_showing_time(movie_id, time_str):
#     movies = load_movies()
#     # Parse the time string into a time object
#     time_to_remove = parse_str_to_time(time_str)
#     if time_to_remove is None:
#         return
#
#     for movie in movies:
#         if movie.movie_id == movie_id:
#             # Filter out showing times when the time part matches time_to_remove
#             movie.showing_times = [
#                 show_time for show_time in movie.showing_times
#                 if show_time.time() != time_to_remove
#             ]
#
#     save_movies(movies)
#     print("Showing time removed successfully.")
