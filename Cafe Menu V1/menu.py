'''Opening accounts text file to get our list of accounts and passwords,
then place them in a dictionary for later use in login/signup.'''
def open_accounts():
    user_list  = {}

    with open("accounts.txt", "r") as acc:
        #adds all lines into keys and values of the userlist
        for lines, line in enumerate(acc, start=1):
            key, value = line.split(':', 1)  # Split only on first colon
            key = key.strip()
            value = value.strip()
            if key:  # Only add if key is not empty
                user_list[key] = value
    return(user_list)

#function to update user list with new user

def update_user(username,password):
    with open("accounts.txt","a") as acc:
        acc.write(f"\n{username}:{password}")

#login function to let user choose between logging in or making a new account

def login():
    #loops function until user has been signed in
    while True:
        choice = ""
        #checks if user has correctly selected login or sign up
        while choice.strip() != "1" and choice.strip() != "2":
            choice = input("Would you like to 1.login or 2.Sign up ? ")
            if choice != "1" and choice != "2":
                print("please enter 1 or 2")

        #check user login details to sign in if correct
        if choice == "1":
            while True:
                username = input("Enter Username : ")
                password = input("Enter Password : ")
                accounts = open_accounts()
                if username not in accounts:
                    #username not found
                    print("Error user not found")
                    go_back = input("would you like to sign up instead? y/n : ")
                    if go_back.lower() == "y":
                        break
                else:
                    #username exists
                    if password != accounts[username]:
                        #username and password dont match
                        print("Username or Password incorrect")
                    else:
                        #username and password match
                        print(f"Welcome {username}.")
                        return(username)

        elif choice == "2":
            #user sign up
            while True:
                username = input("Enter Username : ")
                password = input("Enter Password : ")
                accounts = open_accounts()
                if username in accounts:
                    #username in use already
                    print("Error username is taken")
                elif len(password) <= 5:
                    #password too short
                    print("Password must be longer than 5 letters")
                else:
                    #creates new user and adds them to user list
                    update_user(username,password)
                    print(f"Welcome {username}")
                    return(username)

item_cost = {"pie":5,"chips":2.5,"hot_chocolate":2,"drink":1.5}#set price of items for sale
cart = {} #users cart 
item_stock = {} #items in stock at cafe

#function to empty cart
def reset_cart():
    cart = item_stock
    for item in cart:
        cart[item] = 0

#function to show total amount of each item in stock
def current_stock():
    with open("stock.txt","r") as stock:
        for lines, line in enumerate(stock, start=1):
            key, value = line.split(':', 1)  # Split only on first colon
            key = key.strip()
            value = value.strip()
            if key:  # Only add if key is not empty
                item_stock[key] = int(value)
    return(item_stock)
    


#function to add items to users cart
def add_to_cart(item):
    while True:
        amount = int(input("how many would you like : "))
        if amount > item_stock[item]:
            print(f"Sorry there are only {item_stock[item]} in stock")
        else:
            cart[item] = amount
            print("added to cart")
            break

#updates the stock values
def complete_purchase():
    with open("stock.txt", "w") as stock:
        
        for i in item_stock.keys():
            if i in cart.keys():
                stock.write(f"{i}:{item_stock[i] - cart[i]}\n")
            else:
                stock.write(f"{i}:{item_stock[i]}\n")

#function to allow user to choose what item they would like to add to cart
def purchase():
    current_stock()
    while True:
        num = 1
        print("item:stock")
        for key, value in item_stock.items():
            print(f"{num}.{key} ${item_cost[key]}: {value}")
            num += 1
        buy_choice = input("What would you like to purchase : ")
        #check what item user selected
        if buy_choice == "1":
            add_to_cart("pie")
            break
        elif buy_choice == "2":
            add_to_cart("chips")
            break
        elif buy_choice == "3":
            add_to_cart("hot_chocolate")
            break
        elif buy_choice == "4":
            add_to_cart("drink")
            break
        #invalid choice
        else:
            print("please enter number of item")

#writes receipt of items ordered to receipt.txt
def print_receipt():
    with open("receipts.txt","a") as receipt:
        receipt.write("\n------------------------------------")
        receipt.write(f"\nUser - {user}")
        for item in cart.keys():
            if cart[item] == 0:
                continue
            else:
                receipt.write(f"\n{item} x {cart[item]} : ${cart[item]*item_cost[item]}")
        receipt.write("\n------------------------------------")

#function to allow user to complete or cancel their order
def complete_order():
    #shows user their current cart
    print(f"your cart is:")
    for item in cart.keys():
        if cart[item] == 0:
            continue
        else:
            print(f"{item}:{cart[item]}")
    print("would you like to: \n1.cancel order \n2.complete order")
    order = 0
    while order != "1" and order != "2":
        order = input()
        #invalid input
        if order != "1" and order != "2":
            print("Please enter number of selection")
    #user wants to clear cart
    if order == "1":
        reset_cart()
        print("order cancelled")
    #user wants to complete order
    elif order == "2":
        print_receipt()
        complete_purchase()
        print("order placed")

#run program or  main routine

user = login()
purchase()
complete_order()