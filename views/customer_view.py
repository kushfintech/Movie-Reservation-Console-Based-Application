from controllers.customer_controller import login, register


def customer_non_logged_in_menu():
    while True:
        print("\n MRS>Customers")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            email = input("Enter your email address: ")
            password = input("Enter your password: ")
            login(email=email, password=password)
        elif choice == "2":
            name = input("Enter Your Full Name: ")
            email = input("Enter Your Email Address: ")
            password = input("Enter New Password: ")
            c_password = input("Enter Your New Password Again: ")
            address = input("Enter Your Living Address(Optional): ")
            country = input("Enter Your Country Name(Optional): ")
            if password == c_password:
                register(name=name, email=email, password=password, address=address, country=country)
            else:
                print("Both password does not matched")
        elif choice == "3":
            break
        else:
            print("Invalid choice, please try again.")



def manage_customer_menu():
    while True:
        print("\n MRS>Customers")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            email = input("Enter your email address: ")
            password = input("Enter your password: ")
            login(email=email, password=password)
        elif choice == "2":
            name = input("Enter Your Full Name: ")
            email = input("Enter Your Email Address: ")
            password = input("Enter New Password: ")
            c_password = input("Enter Your New Password Again: ")
            address = input("Enter Your Living Address(Optional): ")
            country = input("Enter Your Country Name(Optional): ")
            if password == c_password:
                register(name=name, email=email, password=password, address=address, country=country)
            else:
                print("Both password does not matched")
        elif choice == "3":
            break
        else:
            print("Invalid choice, please try again.")
