import datetime
import json
from requests import JSONDecodeError


class Restaurant:
    def __init__(self, Rname):
        self.Rname = Rname

    def register_user(self,user_json, name, phone, email, adress, password):
        user = {'id': 1,
        'name': name,
        'phone': phone,
        'email': email,
        'adress': adress,
        'password': password,
        'order_history': {}
        }

        try:
            file = open(user_json,"r+")
            content = json.load(file)

            for i in range (len(content)):
                if content[i]['phone'] == phone:
                    print ("User already exists.")
                    break
            else:
                user['id']= len(content)+1
                content.append(user)
                print ("success")
        except JSONDecodeError:
            content = []
            content.append(user)
            print ("success")
        file.seek(0)
        file.truncate()
        json.dump(content,file,indent=4)
        file.close()

    def user_order_history(self,user_json, user_id):
        file = open(user_json, "r+")
        content = json.load(file)
        for i in range(len(content)):
            if content[i]["id"] == user_id:
                print(f"Hi {content[i]['name']}, Your Order History:")
                print("Date | Order, Quantity, Paid Ammount")
                for i,j in content[i]["order_history"].items():
                    print(f"{i} | {j}")
                file.close()
                return True
        file.close()
        return False

    def user_place_order(self, user_json, food_json, user_id, food_name, quantity):
        date = datetime.datetime.today().strftime('%m-%d-%Y')
        file = open(user_json, "r+")
        content = json.load(file)
        file1 = open(food_json, "r+")
        content1 = json.load(file1)
        for i in range(len(content1)):
            if content1[i]["name"] == food_name:
                if content1[i]["no of plates"] >= quantity:
                    for j in range(len(content)):
                        if content[j]["id"] == user_id:
                            print(f"Price: {content1[i]['price']}")
                            print(f"Discount: {content1[i]['discount']}")
                            final_price = (((content1[i]['price'])-(content1[i]['discount']))*quantity)
                            print(f'Final Price: {final_price}')
                            payment = int(input('Pay the Ammount: '))
                            if (payment == final_price):
                                content1[i]["no of plates"] -= quantity
                                print('success')
                                if date not in content[j]["order_history"]:
                                    content[j]["order_history"][date] = []
                                    content[j]["order_history"][date].extend([content1[i]["name"],quantity,final_price])
                                else:
                                    (content[j]["order_history"][date]).extend([content1[i]["name"],quantity,final_price])
                                    break
                            else:
                                print('Complete the Payment')
                else:
                    print("Pls Enter less quantity")
                    break


        file.seek(0)
        file.truncate()
        json.dump(content, file, indent=4)
        file.close()

        file1.seek(0)
        file1.truncate()
        json.dump(content1, file1, indent=4)
        file1.close()

    def add_food(self,food_json, food_name, no_plates, price, discount):
        food = {
            "id": 1,
            "name": food_name,
            "no of plates": no_plates,
            "price": price,
            "discount": discount
        }
        try:
            fp = open(food_json, "r+")
            content = json.load(fp)
            for i in range(len(content)):
                if content[i]["name"] == food_name:
                    print("Food Already Available")
                    break
            else:
                food["id"] = len(content) + 1
                for i in range(len(content)):
                    if content[i]['id'] == food['id']:
                        while True:
                            food['id'] += 1
                            if content[i]['id'] != food['id']:
                                break
                content.append(food)
                print("Success")

        except json.JSONDecodeError:
            content = []
            content.append(food)
            print("Success")


        fp.seek(0)
        fp.truncate()
        json.dump(content, fp, indent=4)
        fp.close()


    def update_food(self):  # no_plates=-1, price=-1):
        file = open('food.json', "r+")
        content = json.load(file)
        food_id = int(input('Enter the Food ID: '))
        no_plates = int(input('Enter the No. of plates: '))
        new_price = int(input('Enter the New Price: '))
        new_discount = int(input('Enter the New Discount: '))
        for i in range(len(content)):
            if (content[i]["id"] == food_id):
                content[i]["no of plates"] += no_plates
                content[i]["price"] = new_price
                content[i]["discount"] = new_discount
                print("success")
                break
        file.seek(0)
        file.truncate()
        json.dump(content, file, indent=4)
        file.close()

    def remove_food(self,food_json, food_id):
        file = open(food_json, "r+")
        content = json.load(file)
        for i in range(len(content)):
            if content[i]["id"] == food_id:
                print("success")
                del content[i]
                file.seek(0)
                file.truncate()
                json.dump(content, file, indent=4)
                file.close()
                break
        else:
            print("Pls Enter Valid ID")

    def read_food(self,food_json):
        file = open(food_json)
        content = json.load(file)
        print("Menu:")
        for i in range(len(content)):
            print("Id: ", content[i]["id"])
            print(f"---> Name: {content[i]['name']}")
            print(f"---> Number of Plates: {content[i]['no of plates']}")
            print(f"---> Price: {content[i]['price']}")
            print(f"---> Discount: {content[i]['discount']}")
        file.close()
        return True

    def update_profile(self, user_json, id, choice):
        file = open(user_json,"r+")
        content = json.load(file)

        for i in range (len(content)):
            if content[i]['id'] == id:
                if (choice == '1'):
                    new_name = input('Enter the New Name: ')
                    content[i]['name'] = new_name
                elif (choice == '2'):
                    new_phone = input('Enter the New Phone Number: ')
                    content[i]['phone'] = new_phone
                elif (choice == '3'):
                    new_adress = input('Enter the New Adress: ')
                    content[i]['adress'] = new_adress
                elif (choice == '4'):
                    new_email = input('Enter the New E-Mail ID: ')
                    content[i]['email'] = new_email
                elif (choice == '5'):
                    new_password = input('Enter the New Password: ')
                    content[i]['password'] = new_password
                elif (choice == '6'):
                    break
                print("Id: ", content[i]["id"])
                print(f"---> Name: {content[i]['name']}")
                print(f"---> Phone: {content[i]['phone']}")
                print(f"---> Adress: {content[i]['adress']}")
                print(f"---> Email: {content[i]['email']}")
                print(f"---> Password: {content[i]['password']}")
                break
        else:
            print ('Enter Valid ID')
        file.seek(0)
        file.truncate()
        json.dump(content, file, indent=4)
        file.close()
        return "success"


try:
    def main():
        obj = Restaurant("LA KHALSA")
        print(f"*^*^*^*^*^*^*^*^*^EATZZ*^*^*^*^*^*^*^*^*^*\n")
        print(f"__/\__  Welcome To {obj.Rname} Restaurant  __/\__\n")
        print("!!**********************************************************************")
        val = input("Do you Want to order Food Y/n: ")
        print("***********************************************************************!!\n")
        while val.lower() == "y":
            print("Menu: ")
            print("1) Register")
            print("2) Login")
            print("3) Exit")
            val1 = input("Choose one value from the above: ")
            if val1 == "1":
                #--------------Register----------------#
                print()
                name = input("Enter the name: ")
                phone = input("Enter the Phone number: ")
                email = input("Enter your E-Mail: ")
                adress = input("Enter the Adress: ")
                password = input("Enter the password: ")
                obj.register_user('user.json', name, phone, email, adress, password)
            elif val1 == "2":
                while True:
                    print("1. Admin\n2. User\n3. Exit\n")
                    x = input('Enter You Choice: ')
                    if x == "1":
                        print("$--------Admin------$")
                        user = input("Enter name: ")
                        password = input("Enter Password: ")
                        file = open("admin.json", "r+")
                        content = json.load(file)
                        if content["name"] == user:
                            if content["password"] == password:
                                while True:
                                    print()
                                    print("1) Add New Food")
                                    print("2) Edit Food")
                                    print("3) View Food")
                                    print("4) Remove Food")
                                    print("5) Exit")
                                    val3 = input("Enter Your Choice Admin!!")
                                    if val3 == "1":
                                        food_name = input("Enter Food Name: ")
                                        no_plates = int(input("Enter the Stock Value: "))
                                        price = int(input("Enter Price: "))
                                        discount = int(input("Enter discount: "))
                                        obj.add_food('food.json', food_name, no_plates, price, discount)
                                        break
                                    elif val3 == "2":
                                        obj.update_food()
                                        break
                                    elif val3 == '3':
                                        obj.read_food('food.json')
                                    elif val3 == '4':
                                        food_id = int(input("Enter The Food ID: "))
                                        obj.remove_food('food.json',food_id)

                                                # Implement ViewFood and Remove Food
                                    else:
                                        file.close()
                                        print("%%%%Bye Bye%%%%%")
                                        break
                            else:
                                print("Wrong Password!!")
                        else:
                            print("Wrong Username!!")

                    elif x == "2":
                        print("---------USER--------")
                        user = input("Enter name: ")
                        password = input("Enter Password: ")
                        file = open("user.json", "r+")
                        content = json.load(file)
                        for i in range(len(content)):
                            if content[i]["name"] == user:
                                if content[i]["password"] == password:
                                    while True:
                                        print()
                                        print("1) View Menu")
                                        print("2) Place New Order")
                                        print("3) Show History of order")
                                        print("4) Update Profile")
                                        print("5) View Profile")
                                        print("6) Exit")
                                        val3 = input("Enter your Choice User!! ")
                                        if val3 == "1":
                                            obj.read_food("food.json")
                                        elif val3 == "2":
                                            user_id = int(input("Enter User Id:"))
                                            food_name = input("Enter the Food You want to Eat: ")
                                            quantity = int(input("Enter the quantity of food: "))
                                            obj.user_place_order("user.json", "food.json", user_id, food_name, quantity)
                                        elif val3 == "3":
                                            user_id = int(input("Enter User Id:"))
                                            obj.user_order_history('user.json', user_id)
                                        elif val3 == "4":
                                            id = int(input('Enter ID: '))
                                            print('Menu:\n')
                                            print("1) change New Name")
                                            print("2) change Phone Number")
                                            print("3) change Adress")
                                            print("4) change E-Mail")
                                            print("5) change Password")
                                            print("6) Exit")
                                            choice = input('Enter Your Choice: ')
                                            obj.update_profile('user.json', id, choice)
                                        elif val3 == '5':
                                            Usr_id = int(input('Enter Your User ID: '))
                                            file = open('user.json')
                                            content = json.load(file)
                                            for i in range(len(content)):
                                                if (content[i]['id'] == Usr_id):
                                                    print("Id: ", content[i]["id"])
                                                    print(f"---> Name: {content[i]['name']}")
                                                    print(f"---> Phone: {content[i]['phone']}")
                                                    print(f"---> Adress: {content[i]['adress']}")
                                                    print(f"---> Email: {content[i]['email']}")
                                                    print(f"---> Password: {content[i]['password']}")
                                                    break
                                        # Have implemented show order historyand update profile
                                        else:
                                            print("Thanks FOr Your Visit")
                                            break
                        else:
                            print('Wrong Username or Password')
                    elif x == "3":
                        break
                    else:
                        print("Invalid Number")
except Exception as e:
    print("something went wrong please give input carefully")

    # calling the main function

if __name__ == '__main__':
    main()

