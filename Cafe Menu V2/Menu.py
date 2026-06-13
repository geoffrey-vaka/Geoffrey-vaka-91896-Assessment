import tkinter as tk
from tkinter import messagebox
from datetime import datetime

#user values 
user = ()

item_cost = {"pie":5,"chips":2.5,"hot_chocolate":2,"drink":1.5}#set price of items for sale
cart = {} #users cart 


#get total amount of each item in stock
def get_stock():
    item_stock = {}#items in stock at cafe
    with open("stock.txt","r") as stock:
        for lines, line in enumerate(stock, start=1):
            key, value = line.split(':', 1)  # Split only on first colon
            key = key.strip()
            value = value.strip()
            if key:  # Only add if key is not empty
                item_stock[key] = int(value)
        return(item_stock)
        
        

#-----Setting tab details-------
root = tk.Tk()
root.title("Cafe Menu")
root.geometry("500x400")


#swap frames function
def show_frame(frame):
    frame.tkraise()

#function to clear enter boxes
def clear(box):
    box.delete(0, tk.END)

#get list of users and passwords for login or sign up
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

#function to add new user
def add_user(name,password):
    with open("accounts.txt","a") as acc:
        acc.write(f"\n{name}:{password}")

#function to check username and password to log in
def login():
    accounts = open_accounts()
    account_name = username_enter.get()
    account_password = password_enter.get()

#checking login details
    #username not filled
    if account_name.strip() == "":
        messagebox.showerror(title="Error",message="Please enter username")
    #username not found
    elif account_name not in accounts.keys():
        messagebox.showerror(title="Error",message="Account not found")
    #password not filled
    elif account_password.strip() == "":
        messagebox.showerror(title="Error",message="Please enter password")
    #password incorrect
    elif accounts[account_name] != account_password:
        messagebox.showerror(title="Error",message="Username or password incorrect")
    else:
        global user
        user = account_name
        show_frame(order_frame)
        
    clear(username_enter)
    clear(password_enter)

def sign_up():
     accounts = open_accounts()
     account_name = username_enter2.get()
     account_password = password_enter2.get()

#checking login details
    #username not filled
     if account_name.strip() == "":
        messagebox.showerror(title="Error",message="Please enter username")
     #username taken
     elif account_name in accounts.keys():
        messagebox.showerror(title="Error",message="Username taken")
     #password not filled
     elif account_password.strip() == "":
        messagebox.showerror(title="Error",message="Please enter password")
     #password too short
     elif len(account_password) <=5:
        messagebox.showerror(title="Error",message="Password must be longer than 5 letters")
     else:
        add_user(account_name,account_password)
        global user
        user = account_name
        show_frame(order_frame)
     clear(username_enter)
     clear(password_enter)

#check if input is an int
def check_int(P):
    if P == "" or P.isdigit():
        return True
    
    messagebox.showerror(title="Error",message="please only enter full numbers")
    return False



# Register validation function
vcmd = root.register(check_int)

#add items to cart
def add_to_cart():
    cart = get_stock()
    for i in cart.keys():
        cart[i] = 0

    #check if input is a number equal to or less than stock
    value1 = pies_enter.get()
    value2 = chips_enter.get()
    value3 = hot_chocolate_enter.get()
    value4 = drink_enter.get()
    
    value1 = int(value1)
    value2 = int(value2)
    value3 = int(value3)
    value4 = int(value4)
    
    items_bought = {"pie":value1,"chips":value2,"hot_chocolate":value3,"drink":value4}
    total_cost = 0

    if value1 >= get_stock()["pie"]:
        messagebox.showerror(title="Error", message=f"There are only {get_stock()["pie"]} pies.")
    else:
        if value2 >= get_stock()["chips"]:
            messagebox.showerror(title="Error", message=f"There are only {get_stock()['chips']} chips.")
        else:
            if value3 >= get_stock()["hot_chocolate"]:
                messagebox.showerror(title="Error", message=f"There are only {get_stock()['hot_chocolate']} hot chocolate.")
            else:
                if value4 >= get_stock()["drink"]:
                    messagebox.showerror(title="Error", message=f"There are only {get_stock()['drink']} drinks.")
                else:
                    show_cart_item.delete(0, tk.END)
                    show_cart_item.insert(1,f"Pies : {pies_enter.get()}")
                    show_cart_item.insert(2,f"Chips : {chips_enter.get()}")
                    show_cart_item.insert(3,f"Hot chocolate : {hot_chocolate_enter.get()}")
                    show_cart_item.insert(4,f"Drinks : {drink_enter.get()}")
                    for key, value in items_bought.items():
                        total_cost += (value*item_cost[key])
                    show_cart_item.insert(5,f"Total cost : ${total_cost}")
                    show_frame(confirm_frame)

#function to complete purchase and print receipt
def complete_purchase():
    #setting value of items purchased
    value1 = pies_enter.get()
    value2 = chips_enter.get()
    value3 = hot_chocolate_enter.get()
    value4 = drink_enter.get()
    
    value1 = int(value1)
    value2 = int(value2)
    value3 = int(value3)
    value4 = int(value4)

    #updating stock values
    item_stock = get_stock()
    with open("stock.txt", "w") as stock:
        stock.write(f"pie:{item_stock['pie']-value1}\n")
        stock.write(f"chips:{item_stock['chips']-value2}\n")
        stock.write(f"hot_chocolate:{item_stock['hot_chocolate']-value3}\n")
        stock.write(f"drink:{item_stock['drink']-value4}\n")

    #print reciept
    items_bought = {"pie":value1,"chips":value2,"hot_chocolate":value3,"drink":value4}
    total_cost = 0

    #only items that have been purchased get added to receipt (if 1 or more of that item is purchased)
    with open("receipts.txt", "a") as receipt:
        receipt.write("-----------------------\n")
        receipt.write(f"User - {user}\n")
        for key, value in items_bought.items():
            if value != 0:
                receipt.write(f"{key} : {value}   ${value*item_cost[key]}\n")
            total_cost += (value*item_cost[key])
        receipt.write(f"Total : ${total_cost}\n")
        receipt.write("-----------------------\n")

    show_frame(end_frame)






#frames
intro_frame = tk.Frame(root)
sign_up_frame = tk.Frame(root)
log_in_frame = tk.Frame(root)
order_frame = tk.Frame(root)
confirm_frame = tk.Frame(root)
end_frame = tk.Frame(root)


intro_frame.grid(row=0, column=0, sticky="nsew") 
sign_up_frame.grid(row=0, column=0, sticky="nsew") 
log_in_frame.grid(row=0, column=0, sticky="nsew")
order_frame.grid(row=0, column=0, sticky="nsew")
confirm_frame.grid(row=0, column=0, sticky="nsew")
end_frame.grid(row=0, column=0, sticky="nsew")

#-------------Intro frame---------------#

title = tk.Label(intro_frame, text="Would you like to login or signup",font=("Arial", 16))
title.grid(row=0, column=0, columnspan=2, pady=20, padx=100)

#button to login
login_btn = tk.Button(
    intro_frame,
    text="Login",
    command=lambda: show_frame(log_in_frame) )
login_btn.grid(row=3, column=0, pady=100)

#button to sign up
sign_up_btn = tk.Button(
    intro_frame,
    text="Sign up",
    command=lambda: show_frame(sign_up_frame) )
sign_up_btn.grid(row=3, column=1, pady=100)

#----------------------------------------#

#---------------log in frame-------------#

#section for user to enter username
username = tk.Label(log_in_frame, text="Username:")
username.grid(row=0, column=0, sticky="w", padx=100, pady=20)

username_enter = tk.Entry(log_in_frame,)
username_enter.grid(row=0, column=1)

#section for user to enter password
password = tk.Label(log_in_frame, text="Password:")
password.grid(row=1, column=0, sticky="w", padx=100, pady=20)

password_enter = tk.Entry(log_in_frame,)
password_enter.grid(row=1, column=1)

#button to log user in
login_finish = tk.Button(
    log_in_frame,
    text="Log in",
    command=lambda: login()
    )
login_finish.grid(row=4,column=0)

#return button
return_to_start = tk.Button(
    log_in_frame,
    text="return",
    command=lambda:show_frame(intro_frame)
)
return_to_start.grid(row=4, column=1)

#----------------------------------------#

#---------sign up frame------------------#

#section for user to enter username
username = tk.Label(sign_up_frame, text="Username:")
username.grid(row=0, column=0, sticky="w", padx=100, pady=20)

username_enter2 = tk.Entry(sign_up_frame,)
username_enter2.grid(row=0, column=1)

#section for user to enter password
password = tk.Label(sign_up_frame, text="Password:")
password.grid(row=1, column=0, sticky="w", padx=100, pady=20)

password_enter2 = tk.Entry(sign_up_frame,)
password_enter2.grid(row=1, column=1)

#button to sign user ip
sign_up_finish = tk.Button(
    sign_up_frame,
    text="Sign up",
    command=lambda: sign_up()
    )
sign_up_finish.grid(row=4,column=0)

#return button
return_to_start = tk.Button(
    sign_up_frame,
    text="return",
    command=lambda:show_frame(intro_frame)
)
return_to_start.grid(row=4, column=1)

#----------------------------------------#

#------------order frame-----------------#

pies = tk.Label(order_frame, text=f"Pies ${item_cost['pie']}. Stock:{get_stock()['pie']}")
pies.grid(row=0, column=0, sticky="w", padx=100, pady=20)

pies_enter = tk.Entry(order_frame,validate="key",validatecommand=(vcmd,"%P"))
pies_enter.grid(row=0, column=1)
pies_enter.insert(0,"0")

chips = tk.Label(order_frame, text=f"Chips ${item_cost['chips']}. Stock:{get_stock()['chips']}")
chips.grid(row=1, column=0, sticky="w", padx=100, pady=20)

chips_enter = tk.Entry(order_frame,)
chips_enter.grid(row=1, column=1)
chips_enter.insert(0,"0")

hot_chocolate = tk.Label(order_frame, text=f"Hot chocolate ${item_cost['hot_chocolate']}. Stock:{get_stock()['hot_chocolate']}")
hot_chocolate.grid(row=2, column=0, sticky="w", padx=100, pady=20)

hot_chocolate_enter = tk.Entry(order_frame,)
hot_chocolate_enter.grid(row=2, column=1)
hot_chocolate_enter.insert(0,"0")

drink = tk.Label(order_frame, text=f"Drinks ${item_cost['drink']}. Stock:{get_stock()['drink']}")
drink.grid(row=3, column=0, sticky="w", padx=100, pady=20)

drink_enter = tk.Entry(order_frame,)
drink_enter.grid(row=3, column=1)
drink_enter.insert(0,"0")

#add to cart button
add_to_cart_btn = tk.Button(
    order_frame,
    text="Add to cart",
    command=lambda: add_to_cart()
    )
add_to_cart_btn.grid(row=4, column=1)

#----------------------------------------------#

#----------------confirm frame-----------------#
show_cart = tk.Label(confirm_frame,text=f"Your total cart is ")
show_cart_item = tk.Listbox(confirm_frame,)

show_cart.grid(row=0,column=1, )
show_cart_item.grid(row=1,column=1, )

to_cart = tk.Button(
    confirm_frame,
    text="return to cart",
    command=lambda: show_frame(order_frame)
    )
to_cart.grid(row=3,column=0)

finish_order = tk.Button(
    confirm_frame,
    text="confirm order",
    command=lambda: complete_purchase()
)
finish_order.grid(row=3,column=2)

#-------------------------------------------#

#--------------end frame----------------#

complete = tk.Label(end_frame, text="Order placed")
complete.grid(row=0,column=0,padx=100)

close = tk.Button(end_frame, text="Close", command=lambda: root.destroy())
close.grid(row=1,column=0,padx=100)



#Start program
show_frame(intro_frame)

root.mainloop()