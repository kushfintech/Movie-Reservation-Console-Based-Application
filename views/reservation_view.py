from controllers.movie_controller import (add_movie, remove_movie,
                                          show_all_movies, load_movies, get_movie_id_using_interactive_console
                                          )
from controllers.movie_session_controller import select_show_date, select_show_time, display_seats_for_session

from controllers.reservation_controller import (view_reservations, add_reservation, show_reservation_details_by_id,
                                                select_reservation, cancel_reservation, delete_reservation)
from controllers.customer_controller import get_cust_id


def reservation_menu():
    while True:
        print("\nMovie Reservation System")
        print("1. Add Movie")
        print("2. View All Movies")
        print("3. Remove Movie")
        print("4. Back")
        choice = input("Enter choice: ")
        if choice == "1":
            title = input("Enter movie title: ")
            duration = input("Enter movie duration(in minutes): ")
            showing_times = input("Enter showing times separated by comma without space between commas"
                                  " e.g. 2:30 PM,3:00 AM: ").split(',')
            add_movie(title=title, duration=duration)
        elif choice == "2":
            show_all_movies()
        elif choice == "3":
            movies = load_movies()
            if len(movies) > 0:
                show_all_movies()
                movie_id = int(input("Enter movie ID to remove: "))
                remove_movie(movie_id)
            else:
                print("No Movies Found to Delete.")

        elif choice == "4":
            break
        else:
            print("Invalid choice, please try again.")


def manage_reservation_menu():
    while True:
        print("\nManage Reservations")
        print("1. View Reservations")
        print("2. Add New Reservation")
        print("3. Search Reservations")
        print("4. Cancel Reservation")
        print("5. Delete Reservation")
        print("6. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            view_reservations()
        elif choice == "2":
            movie_id = get_movie_id_using_interactive_console()
            if movie_id:
                show_date = select_show_date(movie_id)
                if show_date:
                    print("Select Show")
                    show_time = select_show_time(movie_id=movie_id, show_date_str=show_date)
                    if show_time:
                        session_id = display_seats_for_session(movie_id, show_date, show_time)
                        while True:
                            if session_id:
                                selected_seats = input("Enter seat numbers seperated by comma: ").split(',')
                                if len(selected_seats) > 0 and selected_seats[0] is not "":
                                    customer_id = get_cust_id()
                                    result = add_reservation(customer_id=customer_id, movie_session_id=session_id,
                                                             seat_numbers=selected_seats)
                                    if result:
                                        break

                                else:
                                    print("No Seats Selected")

        elif choice == "3":
            while True:
                print("Search Reservations")
                reservation_id = input("Enter your reservation id to search and C to Cancel: ")
                if reservation_id:
                    if reservation_id.lower() == "c":
                        break
                    else:
                        show_reservation_details_by_id(reservation_id)
        elif choice == "4":
            while True:
                print("Select Reservation to Cancel")
                reservation = select_reservation()
                if reservation:
                    cancel_reservation(reservation.reservation_id)
                else:
                    break
        elif choice == "5":
            while True:
                print("Select Reservation to Delete")
                reservation = select_reservation()
                if reservation:
                    delete_reservation(reservation.reservation_id)
                else:
                    break
        elif choice == "6":
            break
        else:
            print("Invalid choice, please try again.")
