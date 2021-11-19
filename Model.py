import pymysql
from Classes import *
class Model:
    # CONSTRUCTOR - CONNECTING TO DATABASE
    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.bill = Order(None, None, None)
        # self.payment = 0
        try:
            self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                              database=self.database)
        except Exception as e:
            print("X : Error: Connection Failed", str(e))
            return

    # DESTRUCTOR - CLOSING CONNECTION
    def __del__(self) -> None:
        if self.connection is not None:
            self.connection.close()

    def check_password(self,user,password):
        cursor, f = None, False
        try:
            if self.connection is not None:
                cursor = self.connection.cursor()
                query=("select email,password from users where email=%s")
                args=user.email
                cursor.execute(query,args)
                emails = cursor.fetchall()
                for e in emails:
                    if user.email==e[0] and password == e[1]:
                        f = True
                        break
        except Exception as e:
            print("Error: Password Failure", str(e))
        finally:
            if cursor is not None:
                cursor.close()
                return f
    def check_user_exist(self, user):
        cursor, f = None, False
        try:
            if self.connection is not None:
                cursor = self.connection.cursor()
                cursor.execute("select email from users")
                emails = cursor.fetchall()
                for e in emails:
                    if user.email == e[0]:
                        f = True
                        break
        except Exception as e:
            print("Error: User Doesn't Exist", str(e))
        finally:
            if cursor is not None:
                cursor.close()
                return f

    def check_user_credentials(self, user):
        cursor, f = None, False
        try:
            if self.connection is not None:
                cursor = self.connection.cursor()
                cursor.execute("select email, password, status from users")
                credentials = cursor.fetchall()
                for c in credentials:
                    if user.email == c[0] and user.status == c[2]:
                        if user.password == c[1]:
                            f = True
                            break
                        else:
                            selection = input("Password is incorrect\nWant to reset your Password?(y/n): ")
                            if selection == "y" or selection == "Y":
                                passwrd = input("\nEnter New Password: ")
                                while len(passwrd) < 5:
                                    print("\nPassword can't be less than 5 characters")
                                    passwrd = input("\nEnter Password Again: ")
                                self.update_password(c[0], passwrd)
                                f = True
                                break
                            else:
                                break
        except Exception as e:
            print("Error: Invalid Credentials", str(e))
        finally:
            if cursor is not None:
                cursor.close()
                return f

    def update_password(self, email, passwrd):
        cursor = None
        try:
            if self.connection is not None:
                cursor = self.connection.cursor()
                query = "update users set password=%s where email=%s"
                args = (passwrd, email)
                cursor.execute(query, args)
                self.connection.commit()
        except Exception as e:
            print("X: Error: Password not Updated")
        finally:
            if cursor is not None:
                cursor.close()

    def check_medicine_name(self, medicines):
        cursor, f = None, False
        try:
            if self.connection is not None:
                cursor = self.connection.cursor()
                cursor.execute("select med_name from medicine")
                med = cursor.fetchall()
                for e in med:
                    if medicines == e[0]:
                        f = True
                        break
        except Exception as e:
            print("Error: Medicine Adding Error", str(e))
        finally:
            if cursor is not None:
                cursor.close()
                return f

    def insert_user(self, user):
        cursor, f = None, False
        try:
            if self.connection is not None:
                cursor = self.connection.cursor()
                query = "insert into users (email, password, status) values (%s, %s, %s)"
                args = (user.email, user.password, user.status)
                cursor.execute(query, args)
                self.connection.commit()
                f = True
            else:
                f = False
        except Exception as e:
            print("X : Error: Insert User Function", str(e))
            return f
        finally:
            if cursor is not None:
                cursor.close()
                return f

    def search_medicine_name_from_alternatives(self,alternatives, name):
        for a in alternatives:
            if(a[0]==name):
                return True
    def add_medicine(self, medicine, user):
        cursor, f = None, False
        try:
            if self.connection is not None:
                cursor = self.connection.cursor()
                query = "select user_id from users where email = %s"
                args = user.email
                cursor.execute(query, args)
                userid = cursor.fetchone()
                userid = userid[0]
                query = "insert into medicine (admin_id, med_name, price, description, formula, quantity) values (%s,%s,%s,%s,%s,%s)"
                arg = (userid, medicine.med_name, medicine.price, medicine.description, medicine.formula, medicine.quantity)
                cursor.execute(query, arg)
                self.connection.commit()
                f = True
            else:
                f = False
        except Exception as e:
            print("X : Error: Add Medicine Function", str(e))
            f = False
        finally:
            if cursor is not None:
                cursor.close()
                return f

    def delete_medicine_name(self, name):
        cursor, f = None, False
        try:
            if self.connection is not None:
                cursor = self.connection.cursor()
                query = "select med_name, quantity, price, formula from medicine where med_name=%s"
                args = name
                cursor.execute(query, args)
                check = cursor.fetchone()
                if check is None:
                    return False
                query = "delete from medicine where med_name = %s"
                arg = name
                cursor.execute(query, arg)
                self.connection.commit()
                f = True
            else:
                f = False
        except Exception as e:
            print("X : Error: Delete Medicine Name", str(e))
            f = False
        finally:
            if cursor is not None:
                cursor.close()
                return f

    def delete_medicine_formula(self, formula):
        cursor, f = None, False
        try:
            if self.connection is not None:
                cursor = self.connection.cursor()
                query = "select med_name, quantity, price, formula from medicine where formula=%s"
                args = formula
                cursor.execute(query, args)
                check = cursor.fetchone()
                if check is None:
                    return False
                query = "delete from medicine where formula = %s"
                arg = formula
                cursor.execute(query, arg)
                self.connection.commit()
                f = True
            else:
                f = False
        except Exception as e:
            print("X : Error: Delete Medicine formula", str(e))
            f = False
        finally:
            if cursor is not None:
                cursor.close()
                return f

    def search_medicine_name(self, name):
        cursor, check = None, []
        try:
            if self.connection is not None:
                cursor = self.connection.cursor()
                query = "select med_name, quantity, price, formula from medicine where med_name=%s"
                args = name
                cursor.execute(query, args)
                check = cursor.fetchone()
        except Exception as e:
            print("X : Error: Search: Name")
            if cursor is not None:
                cursor.close()
        finally:
            if cursor is not None:
                cursor.close()
            return check

    def display_all(self):
        cursor, check = None, []
        try:
            if self.connection is not None:
                cursor = self.connection.cursor()
                query = "select * from medicine"
                cursor.execute(query)
                check = cursor.fetchall()
        except Exception as e:
            print("X : Error: Display")
            if cursor is not None:
                cursor.close()
        finally:
            if cursor is not None:
                cursor.close()
            return check

    def alternative(self, name, formula):
        cursor, check = None, []
        try:
            if self.connection is not None:
                cursor = self.connection.cursor()
                query = "select med_name, quantity, price, formula from medicine where formula=%s and med_name!=%s"
                args = formula, name
                cursor.execute(query, args)
                check = cursor.fetchall()
        except Exception as e:
            print("X : Error: Alternative")
            if cursor is not None:
                cursor.close()
        finally:
            if cursor is not None:
                cursor.close()
            return check

    def quantity_update(self, name, quantity):
        cursor = None
        try:
            if self.connection is not None:
                cursor = self.connection.cursor()
                query = "update medicine set quantity=%s where med_name=%s"
                args = quantity, name
                cursor.execute(query, args)
                self.connection.commit()
        except Exception as e:
            print("X : Error: Quantity Update Failed")
            if cursor is not None:
                cursor.close()
        finally:
            if cursor is not None:
                cursor.close()

    def price_update(self, name, price):
        cursor = None
        try:
            if self.connection is not None:
                cursor = self.connection.cursor()
                query = "update medicine set price=%s where med_name=%s"
                args = price, name
                cursor.execute(query, args)
                self.connection.commit()
        except Exception as e:
            print("X : Error: Price Update Failed")
            return False
        finally:
            if cursor is not None:
                cursor.close()
                return True
    def order_to(self, medicines):
        ordering=[]
        flag=True
        try:
            if self.connection is not None:
                for med in medicines:
                    m = self.search_medicine_name(med.med_name)
                    if m is None:
                        print("Medicine Not Found")
                        return False
                    else:
                        if m[1] > med.quantity:
                            ordr=Order(m[0],med.quantity,m[2])
                            if ordering is not None:
                                for o in ordering:
                                    if o.med_name==m[0]:
                                       o.quantity = o.quantity + med.quantity
                                       self.payment = self.payment + (m[2] * med.quantity)
                                       self.quantity_update(m[0], (m[1] - med.quantity))
                                       flag=False
                                       break
                            if flag==True:
                                ordering.append(ordr)
                                self.payment = self.payment + (m[2] * med.quantity)
                                self.quantity_update(m[0], (m[1] - med.quantity))
                        else:
                            for_zero=m[1]-1
                            print("Not enough Quantity of ", med.med_name, " in Inventory\nWe can provide ",
                                  m[1] - 1)
                            if(for_zero==0):
                                print("Oops! We can't provide you")
                                break
                            choice = input("\nWant to Take it(y/n): ")
                            if choice == "y" or choice == "Y":
                                med.quantity = m[1] - 1
                                print(m[0], " in Cart, Quantity: ", med.quantity, " , Price: ", m[2])
                                self.quantity_update(m[0], (m[1] - med.quantity))
                            else:
                                choice = input("Want an alternative(y/n): ")
                                if choice == "y" or choice == "Y":
                                    alternatives = self.alternative(m[0], m[3])
                                    if alternatives is not None:
                                        print("Alternatives are:\n")
                                        print("+---------------+----------+-----------+--------------+")
                                        print("\t", end="")
                                        print('{:<13}{:<10}{:<11}{:<14}'.format("Name", "Quantity", "Price","Formula"))
                                        print("+---------------+----------+-----------+--------------+")
                                        for a in alternatives:
                                            print("\t", end="")
                                            print('{:<15}{:<6}{:<15}'.format(a[0],str(a[1]),str(a[2]),a[3]))
                                            print("+---------------+----------+-----------+--------------+")
                                        name = input("Which one you want?Enter Name: ")
                                        while True:
                                            try:
                                                quantity = int(input("Quantity: "))
                                                break
                                            except ValueError:
                                                print("Enter a Number!")
                                        for a in alternatives:
                                            if (a[0] == name):
                                                mmm = [Prescription(name, quantity)]
                                    self.payment = self.order_to(mmm)
            return ordering
            # return self.payment
        except Exception as error:
             print("X: Order Failed!", str(error))