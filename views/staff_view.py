from controllers.staff_controller import load_staffs, register, login
from views.movie_view import manage_movie_menu
from views.sessions_view import manage_sessions_menu
from views.customer_view import manage_customer_menu
from views.reservation_menu import manage_reservation_menu


def check_staff_exists_or_not():
    staffs = load_staffs()
    if not staffs:
        print("Please create first staff to start managing this system!")
        name = input("Enter Full Name: ")
        email = input("Enter Email Address: ")
        password = input("Enter New Password: ")
        c_password = input("Enter New Password Again: ")
        address = input("Enter Your Address(Optional): ")
        country = input("Enter Your Country Name(Optional): ")
        if password == c_password:
            register(name=name, email=email, password=password, address=address, country=country)
        else:
            print("Both password does not matched")


def staff_non_logged_in_menu():
    while True:
        print("\n MRS>Staffs")
        print("1. Login")
        print("2. Back")
        print("3. Main Menu")
        print("4. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            email = input("Enter your email address: ")
            password = input("Enter your password: ")
            result = login(email=email, password=password)
            if result:
                staff_logged_in_menu()
        elif choice == "2":
            return
        elif choice == "3":
            return
        elif choice == "4":
            break
        else:
            print("Invalid choice, please try again.")


def manage_staff_menu():
    while True:
        print("\n MRS>Staffs")
        print("1. Login")
        print("2. Back")
        print("3. Main Menu")
        print("4. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            email = input("Enter your email address: ")
            password = input("Enter your password: ")
            result = login(email=email, password=password)
            if result:
                staff_logged_in_menu()
        elif choice == "2":
            return
        elif choice == "3":
            return
        elif choice == "4":
            break
        else:
            print("Invalid choice, please try again.")


def staff_logged_in_menu():
    while True:
        print("\n MRS>Staffs>Menu")
        print("1. Movies")
        print("2. Movies Sessions")
        print("3. Reservations")
        print("4. Customers")
        print("5. Staffs")
        print("6. Back")
        print("8. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            manage_movie_menu()
        elif choice == "2":
            manage_sessions_menu()
        elif choice == "3":
            manage_reservation_menu()
        elif choice == "4":
            manage_customer_menu()
        elif choice == "5":
            manage_staff_menu()
        elif choice == "6":
            return
        elif choice == "7":
            break
        else:
            print("Invalid choice, please try again.")

