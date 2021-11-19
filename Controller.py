import Model
from Model import *


class Controller:
    # CONSTRUCTOR
    def __init__(self, password) -> None:
        self.password = password
        self.model = Model("localhost", "root", password, "pharmacy")

    def sign_up(self, status):
        email = input("\n\t\tEnter username: ")
        password = input("\t\tEnter Password: ")
        while len(password) < 5:
            password = input("\t\tLength should be greater than 5\n\t\t>: ")
        user = Users(email, password, status)
        taken = self.model.check_user_exist(user)
        if taken is False:
            insert = self.model.insert_user(user)
            while True:
                if insert:
                    password = input(("\t\tConfirm Password:"))
                    checking = self.model.check_password(user, password)
                    if checking is True:
                        print("\t\tO : Signup Successful!")
                        return
                    else:
                        print("\t\tX: Error! Password is incorrect\n")
                        password = input("\t\tEnter new Password: ")
                        while len(password) < 5:
                            password = input("\t\tLength should be greater than 5\n\t\t>: ")
                        self.model.update_password(email, password)

            else:
                print("\t\tX : Signup Failed!")
        else:
            print("\t\tX : Sorry! username Taken!")

    def sign_in(self, status):
        email = input("\n\t\tEnter Email: ")
        password = input("\t\tEnter Password: ")
        user = Users(email, password, status)
        valid = self.model.check_user_credentials(user)
        if valid:
            print('\t\tO : SignIn Successful!')
            if status == "Admin":
                while True:
                    choice = input("\n\t\tto Add Medicine\t\tPress 1\n\t\tto Delete Medicine\tPress 2\n\t\tDisplay "
                                   "Medicines\tPress 3\n\t\tBack\t\t\t\tPress 4\n\t\tChoice: ")
                    while (choice != "1" and choice != "2" and choice != "3" and choice != "4"):
                        choice = input("\n\t\tEnter valid Choice: ")
                    if choice == "1":
                        name = input("\n\t\t\tAdding Medicine...\n\t\t\tName: ")
                        exists = self.model.check_medicine_name(name)
                        if exists is False:
                            while True:
                                try:
                                    price = int(input("\t\t\tPrice: "))
                                    while price <= 0:
                                        price = int(input("\t\t\tEnter Price again: "))
                                    break
                                except ValueError:
                                    print("\t\t\tEnter a Number!")
                            while True:
                                try:
                                    quantity = int(input("\t\t\tQuantity: "))
                                    while quantity <= 0:
                                        quantity = int(input("\t\t\tEnter Quantity again: "))
                                    break
                                except ValueError:
                                    print("\t\t\tEnter a Number!")
                            formula = input("\t\t\tFormula: ")
                            description = input("\t\t\tDescription: ")
                            medicine = Medicine(name, price, description, formula, quantity)
                            add = self.model.add_medicine(medicine, user)
                            if add:
                                print("\t\t\tO : Medicine Added!")
                            else:
                                print("\t\t\tX : Error: Addition Failure")
                        else:
                            choice = input("\n\t\t\tMedicine name already exist\n\t\t\tWant to update Price or "
                                           "Quantity(y/n): ")
                            if choice == "y" or choice == "Y":
                                choice = input("\n\t\t\tto Update Price\tPress 1\n\t\t\tto Update "
                                               "Quantity\tPress 2\n\t\t\tChoice:")
                                if choice == "1":
                                    while True:
                                        try:
                                            price = int(input("\t\t\tPrice: "))
                                            while price <= 0:
                                                price = int(input("\t\t\tEnter Price again: "))
                                            break
                                        except ValueError:
                                            print("\t\t\tEnter a Number!")
                                    addP = self.model.price_update(name, price)
                                    if addP:
                                        print("\t\t\tO: Price Updated")
                                    else:
                                        print("\t\t\tX: Price Update Failure")
                                else:
                                    while True:
                                        try:
                                            quantity = int(input("\t\t\tQuantity: "))
                                            while quantity <= 0:
                                                quantity = int(input("\t\t\tEnter Quantity again: "))
                                            break
                                        except ValueError:
                                            print("\t\t\tEnter a Number!")
                                    addQ = self.model.quantity_update(name, quantity)
                                    if addQ:
                                        print("\t\t\tO: Quantity Updated")
                                    else:
                                        print("\t\t\tX: Quantity Update Failure")
                    elif choice == "2":
                        choice = input("\t\t\tDeleting Medicine...\n\t\t\tBy Name\t\tPress 1\n\t\t\tBy Formula\tPress "
                                       "2\n\t\t\tChoice: ")
                        if choice == "1":
                            name = input("\n\t\t\tEnter Name: ")
                            delete = self.model.delete_medicine_name(name)
                            if delete:
                                print("\t\t\tO : Medicine Deleted!")
                            else:
                                print("\t\t\tX : Error: Delete Failure")
                        if choice == "2":
                            formula = input(
                                "\n\t\t\t🚨 Warning! Will delete all with this Formula\n\t\t\tEnter Formula: ")
                            delete = self.model.delete_medicine_formula(formula)
                            if delete:
                                print("\t\t\tO : Medicine Deleted!")
                            else:
                                print("\t\t\tX : Error: Delete Failure")
                    elif choice == "3":
                        medicines = self.model.display_all()
                        print("+---------------+------+---------------+--------------+---------------")
                        print("\t", end="")
                        print('{:<13}{:<8}{:<15}{:<15}{:<6}'.format("Name", "Price", "Description", "Formula",
                                                                    "Quantity"))
                        print("+---------------+------+---------------+--------------+---------------")
                        for m in medicines:
                            print("\t", end="")
                            print('{:<15}{:<6}{:<15}{:<15}{:<6}'.format(m[2], m[3], m[4], m[5], m[6]))
                        print("+---------------+------+---------------+--------------+---------------\n")
                    elif choice=="4":
                        return
            elif status == "Customer":
                payment = 0
                while True:
                    choice = input("to Give Prescription\tPress 1\nBack\t\t\t\t\tPress 2\nChoice: ")
                    while (choice != "1" and choice != "2"):
                        choice = input("\n\t\tEnter valid Choice: ")
                    if choice == "1":
                        while True:
                            try:
                                many = int(input("How many medicine you wanna buy? "))
                                break
                            except ValueError:
                                print("Enter a Number!")
                        medicines = []
                        for i in range(many):
                            name = input("Details of Medicine you want to buy!\nName: ")
                            while True:
                                try:
                                    quantity = int(input("Quantity: "))
                                    break
                                except ValueError:
                                    print("Enter a Number!")
                            med = Prescription(name, quantity)
                            medicines.append(med)
                        listing = self.model.order_to(medicines)
                        self.model.payment = 0
                        if listing is not None and listing is not False:
                            print("+---------------+----------+-----------+-------------+")
                            print("\t", end="")
                            print('{:<13}{:<10}{:<19}{:<13}'.format("Name", "Quantity", "Price", "Total"))
                            print("+---------------+----------+-----------+-------------+")
                            for m in listing:
                                print("\t", end="")
                                print('{:<15}{:<6}{:<15}{:<17}'.format(m.med_name, str(m.quantity), str(m.price),
                                                                       m.quantity * m.price))
                                payment = payment + (m.quantity * m.price)
                            print("+---------------+------+---------------+----------------+\n")
                        print("Total Bill: Rs.", payment)
                        if(payment!=0):
                            choice = input("Do you want to pay the bill(y/n): ")
                            if (choice == "y" or choice == "Y"):
                                input("Press Any key to Pay...")
                                print("Bill Payment Successful!")
                            payment = 0
                    elif choice=="2":
                        return
        else:
            print('\t\tO : SignIn Failed!')
