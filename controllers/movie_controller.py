from models.movie import Movie
from datetime import datetime
import json
import inquirer


def load_movies():
    try:
        with open('movies.dat', 'r') as f:
            movies_data = json.load(f)
        return [Movie.from_dict(movie) for movie in movies_data]
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist
    except json.JSONDecodeError:
        return []  # Return an empty list if the file is empty or not valid JSON


def save_movies(movies):
    with open('movies.dat', 'w') as f:
        # Ensure that we write an empty list to the file if there are no movies
        json.dump([movie.to_dict() for movie in movies] or [], f)

    # try:
    #     with open('customers.dat', 'wb', buffering=0) as f:
    #         # Ensure that we write an empty list to the file if there are no movies
    #         customers_json = json.dumps([customer.to_dict() for customer in customers] or []).encode('utf-8')
    #         f.write(customers_json)
    #         f.flush()
    # except Exception as e:
    #     print(f"An error occurred while saving customers: {e}")


def show_all_movies():
    movies = load_movies()
    if not movies:
        print("No Movies Found")
        return

    headers = ["Movie ID", "Title", "Duration", "Rating", "Showing Times"]
    column_widths = [max(len(header), max((len(str(getattr(movie, attr))) for movie in movies), default=0)) for header, attr in zip(headers, ['movie_id', 'title', 'duration', 'rating', 'showing_times'])]

    header_row = " | ".join(header.ljust(width) for header, width in zip(headers, column_widths))
    print(header_row)
    print("-" * len(header_row))

    for movie in movies:
        # Format each showing time to a string and join the list into a single string
        showing_times_formatted = ", ".join(show_time.strftime("%I:%M %p") for show_time in movie.showing_times)
        movie_details = [
            str(movie.movie_id),
            movie.title,
            f"{movie.duration} min",
            f"{movie.rating if movie.rating is not None else 'N/A'}",
            showing_times_formatted
        ]
        row = " | ".join(detail.ljust(width) for detail, width in zip(movie_details, column_widths))
        print(row)


def get_movie_id_using_interactive_console():
    movies = load_movies()
    movie_choices = [(movie.title, movie.movie_id) for movie in movies]

    # Ask the user to select a movie
    movie_question = [
        inquirer.List('movie',
                      message="Which movie would you like to create a session for?",
                      choices=movie_choices,
                      carousel=True)
    ]
    selected_movie_id = inquirer.prompt(movie_question)['movie']
    return selected_movie_id


def parse_showing_time(time_str):
    for fmt in ("%I:%M %p", "%H:%M"):  # Supports 12-hour and 24-hour formats
        try:
            return datetime.strptime(time_str, fmt).time()  # Returns a time object
        except ValueError:
            print(f"Time '{time_str}' is not in a recognized format.")
            pass
    raise ValueError(f"Time '{time_str}' is not in a recognized format.")


def parse_str_to_time(time_str):
    # Define the format for the time string
    time_format = "%I:%M %p"  # or "%I:%M %p" for 12-hour format with AM/PM
    try:
        return datetime.strptime(time_str, time_format).time()
    except ValueError:
        print(f"Time '{time_str}' is not in the correct format.")
        return None


def add_movie(title, duration, showing_times):
    movies = load_movies()
    movie_id = max(movie.movie_id for movie in movies) + 1 if movies else 1
    showing_times = [parse_showing_time(time_str) for time_str in showing_times]
    new_movie = Movie(movie_id=movie_id, title=title, duration=duration, showing_times=showing_times)
    movies.append(new_movie)
    save_movies(movies)
    print("Movie Added Successfully!")


def remove_movie(movie_id):
    movies = load_movies()
    movies = [movie for movie in movies if movie.movie_id != movie_id]
    save_movies(movies)
    show_all_movies()


def add_showing_time(movie_id, time):
    movies = load_movies()
    for movie in movies:
        if movie.movie_id == movie_id:
            movie.showing_times.append(parse_showing_time(time))
    save_movies(movies)


def remove_showing_time(movie_id, time_str):
    movies = load_movies()
    # Parse the time string into a time object
    time_to_remove = parse_str_to_time(time_str)
    if time_to_remove is None:
        return

    for movie in movies:
        if movie.movie_id == movie_id:
            # Filter out showing times when the time part matches time_to_remove
            movie.showing_times = [
                show_time for show_time in movie.showing_times
                if show_time.time() != time_to_remove
            ]

    save_movies(movies)
    print("Showing time removed successfully.")


def get_movie_using_id(movie_id):
    """
    Retrieve a movie from the list of all movies using its ID.

    :param movie_id: The unique identifier for the movie.
    :return: The movie object if found, otherwise None.
    """
    all_movies = load_movies()
    return next((movie for movie in all_movies if movie.movie_id == movie_id), None)


def get_showing_times_of_movie(movie: Movie):
    """
    Retrieve the showing times for a given movie.

    :param movie: The movie object.
    :return: A list of showing times for the movie.
    """
    if movie is not None:
        return movie.showing_times
    else:
        return []


def format_show_time_for_display(show_time):
    """Convert a datetime object to a nicely formatted string."""
    return show_time.strftime("%I:%M %p")


def get_show_time_using_interactive_console(showing_times):
    """
    Use inquirer to let the user select a showtime from a list.

    :param showing_times: A list of datetime objects representing show times.
    :return: The selected datetime object.
    """
    if not showing_times:
        print("No showing times available.")
        return None

    show_time_choices = [format_show_time_for_display(show_time) for show_time in showing_times]

    questions = [
        inquirer.List('show_time',
                      message="Choose a show time:",
                      choices=show_time_choices,
                      carousel=True)
    ]

    answer = inquirer.prompt(questions)

    # Convert the selected show time back to a datetime object
    selected_show_time_str = answer['show_time']
    selected_show_time = parse_showing_time(selected_show_time_str)

    return selected_show_time

