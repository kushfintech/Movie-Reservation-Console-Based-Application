from controllers.movie_controller import (add_movie, remove_movie, update_movie,
                                          show_all_movies, load_movies, get_movie_id_using_interactive_console)


def manage_movie_menu():
    while True:
        print("\nManage Movie")
        print("1. Add Movie")
        print("2. View All Movies")
        print("3. Update Movie")
        print("4. Remove Movie")
        print("5. Back")
        choice = input("Enter choice: ")
        if choice == "1":
            title = input("Enter movie title: ")
            duration = input("Enter movie duration(in minutes): ")
            add_movie(title=title, duration=duration)
        elif choice == "2":
            show_all_movies()
        elif choice == "3":
            print("Which movie would you like to update?")
            movie_id = get_movie_id_using_interactive_console()
            if movie_id:
                title = input("Enter movie title: ")
                duration = input("Enter movie duration(in minutes): ")
                update_movie(movie_id=movie_id, title=title, duration=duration)
            else:
                print("No Movies Found to Delete.")
        elif choice == "4":
            movies = load_movies()
            if len(movies) > 0:
                show_all_movies()
                movie_id = int(input("Enter movie ID to remove: "))
                remove_movie(movie_id)
            else:
                print("No Movies Found to Delete.")
        elif choice == "5":
            break
        else:
            print("Invalid choice, please try again.")
