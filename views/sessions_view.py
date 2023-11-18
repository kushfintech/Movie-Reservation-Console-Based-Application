from controllers.movie_session_controller import load_sessions,add_session
from controllers.movie_controller import (get_movie_id_using_interactive_console,
                                          get_movie_using_id, get_showing_times_of_movie,
                                          get_show_time_using_interactive_console)
from controllers.movie_session_controller import (show_all_sessions,get_session_id_using_interactive_console,
                                                  remove_session)


def manage_sessions_menu():
    while True:
        print("\nManage Movies Sessions")
        print("1. Add Session")
        print("2. View All Sessions")
        print("3. Remove Session")
        print("4. Back")
        print("5. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            # title = input("Enter movie title: ")
            # duration = input("Enter movie duration(in minutes): ")
            # showing_times = input("Enter showing times separated by comma without space between commas"
            #                       " e.g. 2:30 PM,3:00 AM: ").split(',')
            movie_id = get_movie_id_using_interactive_console()
            if movie_id:
                movie = get_movie_using_id(movie_id)
                if movie:
                    showing_times = get_showing_times_of_movie(movie)
                    if len(showing_times) > 0:
                        show_time = get_show_time_using_interactive_console(showing_times)
                        while True:
                            try:
                                num_seats = int(input("Enter the total number of seats for the session: "))
                                if num_seats <= 0:
                                    print("The number of seats must be a positive integer.")
                                else:
                                    add_session(movie_id, show_time=show_time, total_seats=num_seats)
                                    break
                            except ValueError:
                                print("Please enter a valid integer for the number of seats.")

        elif choice == "2":
            show_all_sessions()
        elif choice == "3":
            session_id = get_session_id_using_interactive_console()
            if session_id:
                remove_session(session_id)
            return
        elif choice == "4":
            return
        elif choice == "5":
            break
        else:
            print("Invalid choice, please try again.")

