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

    headers = ["Movie ID", "Title", "Duration", "Rating"]
    column_widths = [max(len(header), max((len(str(getattr(movie, attr))) for movie in movies), default=0)) for header, attr in zip(headers, ['movie_id', 'title', 'duration', 'rating'])]

    header_row = " | ".join(header.ljust(width) for header, width in zip(headers, column_widths))
    print(header_row)
    print("-" * len(header_row))

    for movie in movies:
        # Format each showing time to a string and join the list into a single string
        movie_details = [
            str(movie.movie_id),
            movie.title,
            f"{movie.duration} min",
            f"{movie.rating if movie.rating is not None else 'N/A'}"
        ]
        row = " | ".join(detail.ljust(width) for detail, width in zip(movie_details, column_widths))
        print(row)


def show_movie_details_by_name(movie_title):
    # Load movies
    movies = load_movies()  # Assuming this function is defined to load movie data

    # Find the movie with the given title
    movie = next((mv for mv in movies if mv.title.lower() == movie_title.lower()), None)
    if not movie:
        print(f"No movie found with title '{movie_title}'")
        return

    # Prepare movie data for display
    movie_data = {
        "Movie ID": movie.movie_id,
        "Title": movie.title,
        "Duration": f"{movie.duration} min",
        # Add other relevant fields as necessary, e.g., director, genre, etc.
    }

    # Define table headers
    headers = movie_data.keys()

    # Calculate column widths
    column_widths = {header: max(len(header), len(str(movie_data[header]))) for header in headers}

    # Print table header
    header_row = " | ".join(header.ljust(column_widths[header]) for header in headers)
    print(header_row)
    print("-" * len(header_row))

    # Print movie details
    row = " | ".join(str(movie_data[header]).ljust(column_widths[header]) for header in headers)
    print(row)


def select_movie():
    # Load movies, assuming this function returns a list of Movie objects
    movies = load_movies()

    if not movies:
        print("No movies found.")
        return None

    # Create a list of choices for inquirer
    movie_choices = [(f"{movie.title} ({movie.duration} minutes)", movie.movie_id) for movie in movies]

    question = [
        inquirer.List('movie',
                      message="Select a movie:",
                      choices=movie_choices,
                      carousel=True)
    ]

    # Prompt the user to choose a movie
    answers = inquirer.prompt(question)

    # Find and return the selected movie
    selected_movie_id = answers['movie']
    return next((movie for movie in movies if movie.movie_id == selected_movie_id), None)


def get_movie_id_using_interactive_console():
    movies = load_movies()
    movie_choices = [(movie.title, movie.movie_id) for movie in movies]

    # Ask the user to select a movie
    movie_question = [
        inquirer.List('movie',
                      message="Select Movie",
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


def add_movie(title, duration):
    movies = load_movies()
    movie_id = max(movie.movie_id for movie in movies) + 1 if movies else 1
    new_movie = Movie(movie_id=movie_id, title=title, duration=duration)
    movies.append(new_movie)
    save_movies(movies)
    print("Movie Added Successfully!")


def remove_movie(movie_id):
    movies = load_movies()
    movies = [movie for movie in movies if movie.movie_id != movie_id]
    save_movies(movies)
    show_all_movies()


def update_movie(movie_id, title=None, duration=None, rating=None):
    """
    Update the details of an existing movie.

    :param movie_id: The ID of the movie to update.
    :param title: The new title of the movie.
    :param duration: The new duration of the movie.
    :param rating: The new rating of the movie.
    """
    movies = load_movies()
    updated = False

    for movie in movies:
        if movie.movie_id == movie_id:
            if title != "":
                movie.title = title
            if duration != "":
                movie.duration = duration
            if rating != "":
                movie.rating = rating
            updated = True
            break

    if updated:
        save_movies(movies)
        print(f"Movie with ID {movie_id} has been updated successfully.")
    else:
        print(f"Movie with ID {movie_id} not found.")


def get_movie_using_id(movie_id):
    """
    Retrieve a movie from the list of all movies using its ID.

    :param movie_id: The unique identifier for the movie.
    :return: The movie object if found, otherwise None.
    """
    all_movies = load_movies()
    return next((movie for movie in all_movies if movie.movie_id == movie_id), None)


def format_show_time_for_display(show_time):
    """Convert a datetime object to a nicely formatted string."""
    return show_time.strftime("%I:%M %p")
