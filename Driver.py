from Controller import *


def main():
    password = input("To Connect to Database\nEnter Password: ")
    controller = Controller(password)
    while True:
        choice = input("Enter as Admin\t\tPress 1\nEnter as Customer\tPress 2\nExit\t\t\t\tPress 3\nChoice: ")
        # ADMIN
        if choice == "1":
            while True:
                choice = input("\n\tto Sign Up\tPress 1\n\tto Sign In\tPress 2\n\tBack\t\tPress 3\n\tChoice: ")
                if choice == "1":
                    controller.sign_up("Admin")
                elif choice == "2":
                    controller.sign_in("Admin")
                elif choice == "3":
                    break
                else:
                    print("\n\tEnter Valid Choice!")
        # CUSTOMER
        elif choice == "2":
            while True:
                choice = input("\n\tto Sign Up\tPress 1\n\tto Sign In\tPress 2\n\tBack\t\tPress 3\n\tChoice: ")
                if choice == "1":
                    controller.sign_up("Customer")
                elif choice == "2":
                    controller.sign_in("Customer")
                elif choice=="3":
                    break
                else:
                    print("\n\tEnter Valid Choice!")
        # EXIT
        elif choice == "3":
            print("\n\t\tGoodBye OwO")
            break
        else:
            print("\n\tEnter Valid Choice!")
main()
