import inquirer

from models.movie_session import MovieSession
from models.seat import Seat
from models.show import Show
from controllers.customer_controller import load_customers
from controllers.movie_controller import load_movies, format_show_time_for_display, get_movie_using_id
from datetime import datetime, date, time
from typing import List
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
    headers = ["Session ID", "Movie Name", "Show Date", "Show Time", "Total Seats", "Available Seats"]

    # Calculate the maximum width for each column
    column_widths = {
        "Session ID": max(len(headers[0]), max(len(str(session.session_id)) for session in movie_sessions)),
        "Movie Name": max(len(headers[1]), max(len(next((movie.title for movie in all_movies if movie.movie_id ==
                                                         session.movie_id), "Unknown")) for session in movie_sessions)),
        "Show Date": max(len(headers[2]), max(len(session.show.show_date.strftime("%Y-%m-%d")) for session
                                              in movie_sessions)),
        "Show Time": max(len(headers[2]), max(len(session.show.show_time.strftime("%I:%M:%p")) for session
                                              in movie_sessions)),
        "Total Seats": max(len(headers[3]), max(len(str(len(session.seats))) for session in movie_sessions)),
        "Available Seats": max(len(headers[4]), max(len(f"{sum(not seat.is_reserved for seat in session.seats)}/"
                                                        f"{len(session.seats)}") for session in movie_sessions))
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
            session.show.show_date.strftime("%Y-%m-%d").ljust(column_widths["Show Date"]),
            session.show.show_time.strftime("%I:%M:%p").ljust(column_widths["Show Time"]),
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


def parse_str_to_date(date_str):
    # Define the format for the time string
    time_format = "%Y-%m-%d"
    try:
        return datetime.strptime(date_str, time_format).date()
    except ValueError:
        print(f"Time '{date_str}' is not in the correct format.")
        return None


def add_session(movie_id, show_date_str: str, show_time_str: str, total_seats: str):
    sessions = load_sessions()
    session_id = max(session.session_id for session in sessions) + 1 if sessions else 1
    seats = [Seat(seat_number=(i + 1), is_reserved=False) for i in range(int(total_seats))]
    show_id = generate_new_show_id()
    show_date = parse_str_to_date(date_str=show_date_str)
    show_time = parse_str_to_time(show_time_str)
    new_session = MovieSession(session_id=session_id, movie_id=movie_id, show=Show(show_id=show_id, show_date=show_date,
                                                                                   show_time=show_time), seats=seats)
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
        (f"{get_movie_using_id(session.movie_id).title} - {format_show_time_for_display(session.show.show_time)} "
         f"- {format_show_time_for_display(session.show.show_time)}",
         session.session_id)
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


def generate_new_session_id(movie_sessions: List[MovieSession]):
    session_id = max(movie_session.session_id for movie_session in movie_sessions) + 1 if movie_sessions else 1
    return session_id


def get_all_shows_of_all_sessions():
    # Load all sessions
    movie_sessions = load_sessions()  # This function needs to be defined to return all session objects

    # Collect all shows
    all_shows: List[Show] = []
    for session in movie_sessions:
        all_shows.append(session.show)
    return all_shows


def generate_new_show_id():
    shows = get_all_shows_of_all_sessions()
    show_id = max(show.show_id for show in shows) + 1 if shows else 1
    return show_id


def get_shows_for_movie_on_date_time(movie_id, show_date: date, show_time: time):
    # Load all movie sessions
    movie_sessions = load_sessions()  # Assumes a function that loads movie sessions
    # Filter sessions for the given movie ID and the specific date
    shows_on_date_time = [session for session in movie_sessions if
                          session.movie_id == movie_id and session.show.show_date == show_date and
                          session.show.show_time == show_time]

    return shows_on_date_time


def get_shows_for_movie_on_date(movie_id, show_date: date):
    # Load all movie sessions
    movie_sessions = load_sessions()  # Assumes a function that loads movie sessions
    # Filter sessions for the given movie ID and the specific date
    shows_on_date = [session for session in movie_sessions if
                     session.movie_id == movie_id and session.show.show_date == show_date]

    return shows_on_date


def get_show_time_for_movie_on_date(movie_id, show_date: date):
    # Load all movie sessions
    movie_sessions = load_sessions()  # Make sure to implement this function
    # Filter sessions by movie_id and the specific date
    sessions_on_date = [
        session for session in movie_sessions
        if session.movie_id == movie_id and session.show.show_date == show_date
    ]

    # Extract the show times for the filtered sessions
    show_times = [session.show.show_time for session in sessions_on_date]

    # Ensure show times are unique and sorted
    unique_show_times = sorted(set(show_times))

    return unique_show_times


def add_show_date_time_for_movie(movie_id, show_date_str, show_time_str):
    # Load all movie sessions
    movie_sessions = load_sessions()  # load_sessions() needs to be implemented
    # Convert the show date string to a date object
    show_date = datetime.strptime(show_date_str, "%Y-%m-%d").date()
    show_time = datetime.strptime(show_time_str, "%I:%M:%p").time()
    # Check if there is already a session for the given movie ID on the specified date
    existing_session = next((session for session in movie_sessions if session.movie_id ==
                             movie_id and session.show.show_date == show_date and
                             session.show.show_time == show_time), None)

    if existing_session:
        print(f"A show for movie ID {movie_id} already exists on {show_date_str}, {show_time_str}")
        return False  # Indicate that the show date was not added because it already exists

    # If no existing session is found, create a new session with the new show date
    show_id = generate_new_show_id()
    new_session_id = generate_new_session_id(movie_sessions)
    new_session = MovieSession(session_id=new_session_id, movie_id=movie_id,
                               show=Show(show_date=show_date, show_time=show_time, show_id=show_id), seats=[])
    movie_sessions.append(new_session)

    # Save the updated sessions
    save_sessions(movie_sessions)  # save_sessions() needs to be implemented
    print(f"New show date for movie ID {movie_id} added for {show_date_str}")
    return True  # Indicate that the show date was successfully added


def add_or_select_show_date(movie_id):
    # Load sessions
    movie_sessions = load_sessions()  # Make sure to implement this function
    # Filter sessions for the movie
    sessions_for_movie = [session for session in movie_sessions if session.movie_id == movie_id]

    # Get unique show dates
    unique_dates = list({session.show.show_date for session in sessions_for_movie})
    # Sort the dates
    unique_dates.sort()

    # Prepare choices for inquirer
    pre_special_options = [("Add a new Date", "ADD_NEW")]
    date_choices = [(date.strftime(new_date, "%Y-%m-%d")) for new_date in unique_dates]
    post_special_options = [("Cancel", "CANCEL")]
    choices = pre_special_options + date_choices + post_special_options

    # Ask user to select a date
    questions = [
        inquirer.List('show_date',
                      message="Select a show date:",
                      choices=choices,
                      carousel=True)
    ]
    selected_date = inquirer.prompt(questions)['show_date']

    return selected_date


def select_show_date(movie_id):
    # Load sessions
    movie_sessions = load_sessions()  # Make sure to implement this function
    # Filter sessions for the movie
    sessions_for_movie = [session for session in movie_sessions if session.movie_id == movie_id]

    # Get unique show dates
    unique_dates = list({session.show.show_date for session in sessions_for_movie})
    # Sort the dates
    unique_dates.sort()

    date_choices = [(date.strftime(new_date, "%Y-%m-%d")) for new_date in unique_dates]
    choices = date_choices

    if not date_choices:
        print("No sessions found for this movie.")
        return None

    # Ask user to select a date
    questions = [
        inquirer.List('show_date',
                      message="Select a show date:",
                      choices=choices,
                      carousel=True)
    ]
    selected_date = inquirer.prompt(questions)['show_date']

    return selected_date


def select_show_time(movie_id, show_date_str):
    # Load sessions
    movie_sessions = load_sessions()

    session_of_this_movie: List[MovieSession] = []
    for session in movie_sessions:
        if session.movie_id == movie_id and session.show.show_date.strftime("%Y-%m-%d") == show_date_str:
            session_of_this_movie.append(session)

    # Get unique show times for the selected date
    unique_times = list({session.show.show_time for session in session_of_this_movie})
    # Sort the times
    unique_times.sort()

    # Prepare choices for inquirer
    time_choices = [(time.strftime(my_time, "%I:%M %p")) for my_time in unique_times]

    if not time_choices:
        print(f"No sessions found for movie ID {movie_id} on {show_date_str}.")
        return None

    # Ask user to select a time
    questions = [
        inquirer.List('show_time',
                      message="Select a show time:",
                      choices=time_choices,
                      carousel=True)
    ]
    selected_time = inquirer.prompt(questions)['show_time']

    return selected_time


def get_movie_session_by_id(movie_session_id):
    sessions = load_sessions()
    # Find the Movie Session with the given movie_session_id
    movie_session = next((session for session in sessions if session.session_id == movie_session_id), None)
    if movie_session is not None:
        return movie_session
    else:
        print(f"No Movie Session found with ID {movie_session_id}")
        return None


def get_seats_by_ids(movie_session, seat_ids):
    # Assuming movie_session has an attribute 'seats' that is a list of Seat objects
    # And each Seat object has a 'seat_number' attribute
    return [seat for seat in movie_session.seats if seat.seat_number in seat_ids]


def display_seats_for_session(movie_id, show_date_str, show_time_str):
    # Load sessions
    movie_sessions = load_sessions()  # This function needs to be defined

    # Find the specific session
    session = next((s for s in movie_sessions if s.movie_id == movie_id and s.show.show_date.strftime("%Y-%m-%d") ==
                    show_date_str and s.show.show_time.strftime("%I:%M %p") == show_time_str), None)

    is_cancelled = is_session_cancelled(session.session_id)
    if is_cancelled:
        print("Session is Cancelled")
        return

    is_full = is_session_full(session.session_id)
    if is_full:
        print("Session is Full")
        return

    if session is None:
        print(f"No session found for movie ID {movie_id} on {show_date_str} at {show_time_str}")
        return

    # Extract seat details
    seat_details = [
        {"Seat Number": seat.seat_number, "Availability": "AVAILABLE" if not seat.is_reserved else "RESERVED"} for seat
        in session.seats]

    # Define the table headers
    headers = ["Seat Number", "Availability"]

    # Calculate the maximum width for each column
    column_widths = {header: max(len(header), max(len(str(detail[header])) for detail in seat_details)) for header in
                     headers}

    # Print table header
    header_row = " | ".join(header.ljust(column_widths[header]) for header in headers)
    print(header_row)
    print("-" * len(header_row))

    # Print each seat's details
    for detail in seat_details:
        row = " | ".join(str(detail[header]).ljust(column_widths[header]) for header in headers)
        print(row)

    return session.session_id


def is_session_full(movie_session_id):
    movie_sessions = load_sessions()  # Load movie sessions

    # Find the specific movie session
    movie_session = next((session for session in movie_sessions if session.session_id == movie_session_id), None)
    if not movie_session:
        print(f"No movie session found with ID {movie_session_id}")
        return False

    # Check if all seats are reserved
    return all(seat.is_reserved for seat in movie_session.seats)


def is_session_cancelled(movie_session_id):
    movie_sessions = load_sessions()  # Load movie sessions

    # Find the specific movie session
    movie_session = next((session for session in movie_sessions if session.session_id == movie_session_id), None)
    if not movie_session:
        print(f"No movie session found with ID {movie_session_id}")
        return False

    # Check if the session is cancelled
    return movie_session.status == 'cancelled'  # Assuming there's a 'status' attribute


def cancel_session(session_id):
    # Load existing movie sessions
    movie_sessions = load_sessions()  # Load all movie sessions

    # Find the movie session to cancel
    movie_session = next((session for session in movie_sessions if session.session_id == session_id), None)
    if not movie_session:
        print(f"No movie session found with ID {session_id}")
        return False

    # Change the movie session status to 'cancelled'
    movie_session.status = 'cancelled'  # Assuming there's a 'status' attribute

    # Optionally, handle related reservations
    # This might include setting their status to 'cancelled' and notifying the customers
    # Implement this as needed based on your application's requirements

    # Save the updated movie sessions
    save_sessions(movie_sessions)  # Make sure this function is defined to save movie sessions

    print("Movie session cancelled successfully.")
    return True
