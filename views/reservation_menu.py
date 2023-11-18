from controllers.movie_controller import (add_movie, remove_movie, add_showing_time, remove_showing_time,
                                          show_all_movies, load_movies)


def reservation_menu():
    while True:
        print("\nMovie Reservation System")
        print("1. Add Movie")
        print("2. View All Movies")
        print("3. Remove Movie")
        print("4. Add Showing Time")
        print("5. Remove Showing Time")
        print("6. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            title = input("Enter movie title: ")
            duration = input("Enter movie duration(in minutes): ")
            showing_times = input("Enter showing times separated by comma without space between commas"
                                  " e.g. 2:30 PM,3:00 AM: ").split(',')
            add_movie(title=title, duration=duration, showing_times=showing_times)
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
            movie_id = int(input("Enter movie ID to add showing time: "))
            time = input("Enter showing time (YYYY-MM-DD HH:MM): ")
            add_showing_time(movie_id, time)
        elif choice == "5":
            movie_id = int(input("Enter movie ID to remove showing time: "))
            time = input("Enter showing time (YYYY-MM-DD HH:MM): ")
            remove_showing_time(movie_id, time)
        elif choice == "6":
            break
        else:
            print("Invalid choice, please try again.")



def manage_reservation_menu():
    while True:
        print("\nMovie Reservation System")
        print("1. Add Movie")
        print("2. View All Movies")
        print("3. Remove Movie")
        print("4. Add Showing Time")
        print("5. Remove Showing Time")
        print("6. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            title = input("Enter movie title: ")
            duration = input("Enter movie duration(in minutes): ")
            showing_times = input("Enter showing times separated by comma without space between commas"
                                  " e.g. 2:30 PM,3:00 AM: ").split(',')
            add_movie(title=title, duration=duration, showing_times=showing_times)
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
            movie_id = int(input("Enter movie ID to add showing time: "))
            time = input("Enter showing time (YYYY-MM-DD HH:MM): ")
            add_showing_time(movie_id, time)
        elif choice == "5":
            movie_id = int(input("Enter movie ID to remove showing time: "))
            time = input("Enter showing time (YYYY-MM-DD HH:MM): ")
            remove_showing_time(movie_id, time)
        elif choice == "6":
            break
        else:
            print("Invalid choice, please try again.")

