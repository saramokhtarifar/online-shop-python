import tkinter as tk
from tkinter import messagebox
from models import (Store,Admin,Product,Customer,User)
from PIL import Image,ImageTk
import os
store=Store()

try:
    store.load_products("products.csv")
except FileNotFoundError as e:
    messagebox.showerror("Loading Error")

try:
    store.load_users("users.csv")
except FileNotFoundError as e:
    messagebox.showerror("Loading Error")
    
try:
    store.load_orders("orders.csv")
except FileNotFoundError as e:
    messagebox.showerror("Loading Error")

try:
    store.load_comments("comments.csv")
except FileNotFoundError as e:
    messagebox.showerror("Loading Error")

root=tk.Tk()
root.title("Online Shop")
root.geometry("700x550")
root.config(bg="#D8CBBA")
logo_label=tk.Label(root,text="ONLINE SHOP",font=("Calibri",22,"bold"),bg="#F1E3D6",fg="#8F6C58")
logo_label.pack(pady=20)
username_label=tk.Label(root,text="Username:",font=("Calibri",12),bg="#F1E3D6",fg="#8F6C58")
username_label.pack(pady=5)
username_entry=tk.Entry(root,width=30)
username_entry.pack()

password_label=tk.Label(root,text="Password:",font=("Calibri",12),bg="#F1E3D6",fg="#8F6C58")
password_label.pack(pady=5)
password_entry=tk.Entry(root,show="*",width=30)
password_entry.pack()
login_label=tk.Label(root,text="",bg="#D8CBBA")
#login
def handle_login():
    username=username_entry.get()
    password=password_entry.get()
    user=store.login(username,password)
    if user:
        login_label.config(text=f"Welcome dear {username} your login was successful",bg='#D8CBBA',fg="#34D136",font=("Calibri",12),pady=20)
        username_label.pack_forget()
        username_entry.pack_forget()
        password_entry.pack_forget()
        password_label.pack_forget()
        login_button.pack_forget()
        if isinstance(user,Customer):
            show_customer_panel(user)
        elif isinstance(user,Admin):
            show_admin_panel(user)
    else:
        login_label.config(text="Invalid username or password",fg="#DC394F",bg="#D8CBBA",font=("Calibri",12))

login_button=tk.Button(root,text="Login",command=handle_login,font=("Segoe UI",10),bg='#A98F76',fg="white")
login_button.pack(padx=3,pady=10)
login_label.pack(pady=2)

signup_label=tk.Label(root,text="Do you want to create an account?",font=("Calibri",12),bg="#D8CBBA",fg="#8F6C58")
signup_label.pack(pady=5)

def signup_window():
    window=tk.Toplevel(root)
    window.title("Sign Up Window")
    window.config(bg="#D8CBBA")
    window.geometry("700x550")
    newusername_label=tk.Label(window,text="Username:",font=("Calibri",12),bg='#A98F76',fg="white")
    newusername_label.pack(pady=5)
    newusername_entry=tk.Entry(window)
    newusername_entry.pack()
    newpassword_label=tk.Label(window,text="Password:",font=("Calibri",12),bg='#A98F76',fg="white")
    newpassword_label.pack(pady=5)
    newpassword_entry=tk.Entry(window)
    newpassword_entry.pack()
    balance_label=tk.Label(window,text="Balance:",font=("Calibri",12),bg='#A98F76',fg="white")
    balance_label.pack(pady=5)
    balance_entry=tk.Entry(window)
    balance_entry.pack()
    result_label=tk.Label(window,text='',font=("Calibri",12),bg="#D8CBBA")
    result_label.pack(pady=5)

    def signup():
        username=newusername_entry.get()
        if username=='':
            result_label.config(text="Username can't be empty",fg="#DC394F")
            return
        password=newpassword_entry.get()
        if password=='':
            result_label.config(text="Password can't be empty",fg="#DC394F")
            return
        try:
            balance=float(balance_entry.get())
            if balance<0:
                result_label.config(text="Balance can't be a negative number",fg="#DC394F")
                return
        except ValueError:
            result_label.config(text="Balance must be a number",fg="#DC394F")
            return
        new_user=store.adding_customer(username,password,balance)
        if new_user:
            store.save_users("users.csv")
            result_label.config(text=f"Welcome {username} you are user now!",fg="#14c157")
            newusername_entry.delete(0,tk.END)
            newpassword_entry.delete(0,tk.END)
            balance_entry.delete(0,tk.END)

        else:
            result_label.config(text="This username already exits pick another one",fg="#DC394F")
    sign_button=tk.Button(window,text="Sign Up",command=signup,font=("Segoe UI",10),bg='#A98F76',fg="white")
    sign_button.pack(pady=3,padx=10)

signup_button=tk.Button(root,text="Sign Up",command=signup_window,font=("Segoe UI",10),bg='#A98F76',fg="white")
signup_button.pack(padx=3,pady=10)

def show_guest_parts():
    window=tk.Toplevel(root)
    window.title("Guest Parts")
    window.config(bg="#D8CBBA")
    window.geometry("700x550")
    tk.Label(window,text="Guest Mode-Browse Products",font=("Calibri",16,"bold"),bg='#A98F76',fg="white").pack(pady=10)
    scrollbar=tk.Scrollbar(window)
    product_listbox=tk.Listbox(window,width=80,height=20,bg="#F1E3D6",fg="#8F6C58",yscrollcommand=scrollbar.set)
    tk.Button(window,text="Show Products",command=lambda:show_products(product_listbox),font=("Segoe UI",10),bg='#A98F76',fg="white").pack(padx=10,pady=3)
    scrollbar.pack(side="right",fill="y")
    product_listbox.pack(side="left",fill="both",expand=True)
    

guests_label=tk.Label(root,text="Do you want to visit as a non-user?",font=("Calibri",12),bg="#D8CBBA",fg="#8F6C58")
guests_label.pack(pady=5)
guests_button=tk.Button(root,text="Visit",command=show_guest_parts,font=("Segoe UI",10),bg='#A98F76',fg="white")
guests_button.pack(padx=3,pady=10)


#customer panel
def show_customer_panel(user:'Customer'):
    panel=tk.Toplevel(root)
    panel.geometry("700x550")
    panel.title('Customer Panel')
    panel.config(bg="#D8CBBA")
    title_frame=tk.Frame(panel,bg='#A98F76')
    title_frame.pack(pady=10)

    button_frame=tk.Frame(panel,bg="#D8CBBA")
    button_frame.pack(pady=10)
    button_frame.columnconfigure(0,weight=1)
    button_frame.columnconfigure(1,weight=1)
    button_frame.columnconfigure(2,weight=1)

    result_frame=tk.Frame(panel,bg='#A98F76')
    result_frame.pack(pady=10)
    tk.Label(title_frame,text=f"Customer Panel-{user.username}",font=("Calibri",16,"bold"),bg='#A98F76',fg="white").pack(pady=10)
    scrollbar=tk.Scrollbar(result_frame)
    product_listbox=tk.Listbox(result_frame,width=80,height=20,bg="#F1E3D6",fg="#8F6C58",yscrollcommand=scrollbar.set,font=("Calibri",13))
    scrollbar.config(command=product_listbox.yview)
    product_listbox.bind("<Double-Button-1>",lambda event:open_product_details(event,product_listbox,user))
    tk.Button(button_frame,text="Show Profile",command=lambda:profile_window(user),font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=0,column=0,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text="Change Password",command=lambda:change_password_window(user),font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=0,column=1,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text="Adding Balance",command=lambda:add_balance_window(user),font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=0,column=2,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text="Show Products",command=lambda:show_products(product_listbox),font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=1,column=0,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text="Search Products",command=lambda:search_product_window(),font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=1,column=1,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text='Checkot',command=lambda:checkout_window(user),font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=1,column=2,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text="Add To Cart",command=lambda:add_to_cart_window(user),font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=2,column=0,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text="View Cart:",command=lambda:view_cart(product_listbox,user),font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=2,column=1,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text="Remove from Cart",command=lambda:remove_from_cart_window(user),font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=2,column=2,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text="Logout",command=lambda:logout(panel),font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=3,column=1,padx=5,pady=5,sticky="ew")
    scrollbar.pack(side="right",fill="y")
    product_listbox.pack(side="left",fill="both",expand=True)

#admin panel
def show_admin_panel(user:Admin):
    panel=tk.Toplevel(root)
    panel.geometry("700x550")
    panel.title("Admin Panel")
    panel.config(bg="#D8CBBA")

    title_frame=tk.Frame(panel,bg='#A98F76')
    title_frame.pack(pady=10)

    button_frame=tk.Frame(panel,bg="#D8CBBA")
    button_frame.pack(pady=10)
    button_frame.columnconfigure(0,weight=1)
    button_frame.columnconfigure(1,weight=1)
    button_frame.columnconfigure(2,weight=1)

    result_frame=tk.Frame(panel)
    result_frame.pack(pady=10)

    tk.Label(title_frame,text=f"Admin Panel {user.username}",font=("Calibri",16,"bold"),bg='#A98F76',fg="#F1E3D6").pack(pady=5)
    scrollbar=tk.Scrollbar(result_frame)
    product_listbox=tk.Listbox(result_frame,width=80,height=15,bg="#F1E3D6",fg="#8F6C58",yscrollcommand=scrollbar.set,font=("Calibri",13))
    scrollbar.config(command=product_listbox.yview)
    product_listbox.bind("<Double-Button-1>",lambda event:open_product_details(event,product_listbox,user))
    tk.Button(button_frame,text="Show Profile",command=lambda:profile_window(user),font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=0,column=0,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text="Change Password",command=lambda:change_password_window(user),font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=0,column=1,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text="Show Products",command=lambda:show_products(product_listbox),font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=0,column=2,padx=10,pady=3,sticky="ew")
    tk.Button(button_frame,text="Search Users",command=search_users_window,font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=0,column=3,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text="Apply Discount",command=apply_discount_window,font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=1,column=0,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text="Add Product",command=add_product_window,font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=1,column=1,padx=10,pady=3,sticky="ew")
    tk.Button(button_frame,text="Remove Product",command=lambda:remove_product_window(user),font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=1,column=2,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text="Edit Product",command=lambda:edit_product_window(user),font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=1,column=3,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text="View Orders",command=lambda:view_orders(product_listbox),font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=2,column=0,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text="Show Users",command=lambda:show_users(product_listbox),font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=2,column=1,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text="View Comments",command=lambda:view_comments(product_listbox),font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=2,column=2,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text="Sale Statistics",command=sale_statistics,font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=2,column=3,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text="Sale Report(Date)",command=sale_report_by_date,font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=3,column=0,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text="Sale Report(ID)",command=sale_report_by_product,font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=3,column=1,padx=5,pady=5,sticky="ew")
    tk.Button(button_frame,text="Logout",command=lambda:logout(panel),font=("Segoe UI",10),bg='#A98F76',fg="white",width=15).grid(row=3,column=2,padx=5,pady=5,sticky="ew")
    scrollbar.pack(side="right",fill="y")
    product_listbox.pack(side="left",fill="both",expand=True)
    
current_view=""
#1.admin/customer
def show_products(listbox):
    global current_view
    current_view="products"
    listbox.delete(0,tk.END)
    for product in store.products:
        listbox.insert(tk.END,
                       f"{product.product_id:<5}|"
                       f"{product.name:<50}"
                       f"${product.price:<10}"
                       f"Stock:{product.stock}"
                       )
        
#2.customer
def view_cart(listbox,user:'Customer'):
    global current_view
    current_view="cart"
    listbox.delete(0,tk.END)
    for product in user.cart:
        listbox.insert(tk.END,
                       f"Product:{product["product"].name:<50}|"
                       f"Quantity:{product["quantity"]:<10}"
                       f"Total:{product["product"].price*product["quantity"]}")

#3.customer
def add_to_cart_window(user:Customer):
    window=tk.Toplevel(root)
    window.geometry("700x550")
    window.title('Add')
    window.config(bg="#D8CBBA")
    pid_label=tk.Label(window,text="Product ID:",font=("Calibri",12),bg='#A98F76',fg="white")
    pid_label.pack(pady=5)
    pid_entry=tk.Entry(window)
    pid_entry.pack()
    quantity_label=tk.Label(window,text="Quantituy:",font=("Calibri",12),bg='#A98F76',fg="white")
    quantity_label.pack(pady=5)
    quantity_entry=tk.Entry(window)
    quantity_entry.pack()
    result_label=tk.Label(window,text='',font=("Calibri",12),bg="#D8CBBA")
    result_label.pack(pady=5)
    def add_to_cart():
        try:
            quantity=int(quantity_entry.get())
            if quantity<=0:
                result_label.config(text="Quantity must be greater than 0",fg="#DC394F")
                return
        except ValueError:
            result_label.config(text="quantity must be a number",fg="#DC394F")
            return
        wanted_product=None
        for product in store.products:
            if product.product_id==pid_entry.get().upper():
                wanted_product=product
        if wanted_product is None:
            result_label.config(text="Invalid Product ID!",fg="#DC394F")
            return
        if quantity>wanted_product.stock:
            result_label.config(text="The quantity is out of range",fg="#DC394F")
            return
        added=user.add_to_cart(wanted_product,quantity)            
        if added:
            result_label.config(text="Product added to your cart successfully",fg="white")
            pid_entry.delete(0,tk.END)
            quantity_entry.delete(0,tk.END)
        else:
            result_label.config(text="this product is already in the cart",fg="#DC394F")
    add_button=tk.Button(window,text="Add",command=add_to_cart,font=("Segoe UI",10),bg='#A98F76',fg="white")
    add_button.pack(pady=10)
 #4.customer
def remove_from_cart_window(user:Customer):
    window=tk.Toplevel(root)
    window.title("Remove")
    window.geometry("700x550")
    window.config(bg="#D8CBBA")
    pid_label=tk.Label(window,text="Product ID:",font=("Calibri",12),bg='#A98F76',fg="white")
    pid_label.pack(pady=5)
    pid_entry=tk.Entry(window)
    pid_entry.pack()
    result_label=tk.Label(window,text='',bg="#D8CBBA",font=("Calibri",12))
    result_label.pack(pady=5)
    def remove_from_cart():
        pid=pid_entry.get()
        removed=user.remove(pid)
        if removed:
            result_label.config(text=f"{pid} removed from your cart successfully")
            pid_entry.delete(0,tk.END)
        else:
            result_label.config(text=f"{pid} wasn't in your cart",fg="#DC394F")
    remove_button=tk.Button(window,text='Remove',command=remove_from_cart,font=("Segoe UI",10),bg='#A98F76',fg="white")
    remove_button.pack(pady=3,padx=10)

#4.customer
def checkout_window(user:Customer):
    window=tk.Toplevel(root)
    window.geometry("700x550")
    window.title('checkout')
    window.config(bg="#D8CBBA")
    checkout_label=tk.Label(window,text="Checkout",font=("Calibri",12),bg='#A98F76',fg="white")
    checkout_label.pack(pady=5)
    result_label=tk.Label(window,text="",font=("Calibri",12),bg="#D8CBBA")
    result_label.pack(pady=3,padx=10)
    def check_out():
        if len(user.cart)==0:
            result_label.config(text='The cart is still empty',fg="#DC394F")
            return
        else:
            checked_out=store.checkout(user)
            if checked_out:
                result_label.config(text=f'checkout was successfull\nYour current budget={user.balance:.2f}')
                store.save_orders("orders.csv")
                store.save_products("products.csv")
                store.save_users("users.csv")
            elif not checked_out:
                result_label.config(text=f'Sorry your balance is not enough!',fg="#DC394F")
    checkeout_button=tk.Button(window,text="Checkout",command=check_out,font=("Segoe UI",10),bg='#A98F76',fg="white")
    checkeout_button.pack(pady=3,padx=10)

#5.customer
def search_product_window():
    window=tk.Toplevel(root)
    window.geometry('700x550')
    window.config(bg="#D8CBBA")
    window.title("search")
    name_label=tk.Label(window,text='Enter the product name:',font=("Calibri",12),bg='#A98F76',fg="white")
    name_label.pack(pady=5)
    name_entry=tk.Entry(window)
    name_entry.pack()
    result_label=tk.Label(window,text='',font=("Calibri",12),bg="#D8CBBA")
    result_label.pack(pady=5)
    scrollbar=tk.Scrollbar(window)
    listbox=tk.Listbox(window,width=80,height=15,bg="#F1E3D6",fg="#8F6C58",yscrollcommand=scrollbar.set,font=("Calibri",13))
    def search():
        name=name_entry.get()
        result=store.search_product(name)
        if len(result)==0:
            result_label.config(text="There's no product here",fg="#DC394F")
            return
        else:
            listbox.delete(0,tk.END)
            for product in result:
                listbox.insert(tk.END,
                               f"{product.product_id:<5}|"
                               f"{product.name:<50}"
                               f"${product.price:<10}"
                               f"Stock:{product.stock}")
    search_button=tk.Button(window,text="Search",command=search,font=("Segoe UI",10),bg='#A98F76',fg="white")
    search_button.pack(pady=3,padx=10)
    scrollbar.pack(side="right",fill="y")
    listbox.pack(side="left",fill="both",expand=True)

#customer
def profile_window(user:User):
    window=tk.Toplevel(root)
    window.geometry("700x550")
    window.title('View Profile')
    window.config(bg="#D8CBBA")
    main_frame=tk.Frame(window,bg="#D8CBBA")
    main_frame.pack(fill="both",expand=True,padx=20,pady=20)
    info_frame=tk.Frame(main_frame,bg="#F1E3D6",padx=20,pady=20,bd=2,relief="groove")
    info_frame.pack(pady=10,fill="x")
    tk.Label(info_frame,text=f"{user.username}'s Profile",font=("Calibri",18,"bold"),bg="#F1E3D6",fg="#8F6C58").pack(pady=5)
    tk.Label(info_frame,text=f"Username:{user.username}",font=("Calibri",12,"bold"),bg="#F1E3D6",fg="#8F6C58").pack(pady=5)
    tk.Label(info_frame,text=f"Balance:{user.balance:.2f}",font=("Calibri",12,"bold"),bg="#F1E3D6",fg="#14c157").pack(pady=5)

    if isinstance(user,Customer):
        cart_frame=tk.Frame(main_frame,bg="#F1E3D6",padx=20,pady=20,bd=2,relief="groove")
        cart_frame.pack(pady=10,fill="x")
        cart_count=len(user.cart)
        tk.Label(cart_frame,text=f"Items in cart:{cart_count}",font=("Calibri",12,"bold"),bg="#F1E3D6",fg="#8F6C58").pack(pady=5)
        tk.Label(cart_frame,text=f"Cart Total:{user.calculate_total()}",font=("Calibri",12,"bold"),bg="#F1E3D6",fg="#8F6C58").pack(pady=5)

def add_balance_window(user:Customer):
    window=tk.Toplevel(root)
    window.geometry("700x550")
    window.title('Add Balance')
    window.config(bg="#D8CBBA")
    add_label=tk.Label(window,text="How much:",font=("Calibri",12),bg='#A98F76',fg="white")
    add_entry=tk.Entry(window)
    add_label.pack()
    add_entry.pack(pady=5)
    result_label=tk.Label(window,text="",font=("Calibri",12),bg="#D8CBBA")
    result_label.pack()
    def add_balance():
        try:
            added=float(add_entry.get())
            if added<=0:
                result_label.config(text="Enter Positive number",fg="#DC394F")
                return
        except ValueError:
            result_label.config(text="Only numbers are acceptable",fg="#DC394F")
            return
        user.balance+=added
        store.save_users("users.csv")
        result_label.config(text=f'Your current balance: {user.balance}',fg="#15a220")
    add_button=tk.Button(window,text="Add",command=add_balance,font=("Segoe UI",10),bg='#A98F76',fg="white")
    add_button.pack(padx=10,pady=3)
#user
#def change_password
#2.admin
def add_product_window():
    window=tk.Toplevel(root)
    window.geometry("700x550")
    window.title('Add')
    window.config(bg="#D8CBBA")
    pid_label=tk.Label(window,text="Product Id:",font=("Calibri",12),bg='#A98F76',fg="white")
    pid_label.pack(pady=5)
    pid_entry=tk.Entry(window)
    pid_entry.pack()
    pname_label=tk.Label(window,text="Name:",font=("Calibri",12),bg='#A98F76',fg="white")
    pname_label.pack(pady=5)
    pname_entry=tk.Entry(window)
    pname_entry.pack()
    price_label=tk.Label(window,text="Price:",font=("Calibri",12),bg='#A98F76',fg="white")
    price_label.pack(pady=5)
    price_entry=tk.Entry(window)
    price_entry.pack()
    stock_label=tk.Label(window,text="Stock:",font=("Calibri",12),bg='#A98F76',fg="white")
    stock_label.pack(pady=5)
    stock_entry=tk.Entry(window)
    stock_entry.pack()
    category_label=tk.Label(window,text="Category:",font=("Calibri",12),bg='#A98F76',fg="white")
    category_label.pack(pady=5)
    category_entry=tk.Entry(window)
    category_entry.pack()
    result_label=tk.Label(window,text="",font=("Calibri",12),bg="#D8CBBA")
    result_label.pack(pady=5)
    def add_product():
        p_id=pid_entry.get()
        name=pname_entry.get()
        if name=="":
            result_label.config(text="Product Nmae Can't Be Empty",fg="#DC394F")
            return
        try:
            price=float(price_entry.get())
            if price<=0:
                result_label. config(text="price must be greater than 0",fg="#DC394F")
                return
        except ValueError:
            result_label.config(text="Price must be a number",fg="#DC394F")
            return
        try:
            stock=int(stock_entry.get())
            if stock<0:
                result_label.config(text="stock must be greater than 0",fg="#DC394F")
                return
        except ValueError:
            result_label.config(text="Stock must be a number",fg="#DC394F")
            return
        category=category_entry.get()
        new_product=Product(p_id,name,price,stock,category)
        added=store.add_product(new_product)
        if added:
            store.save_products("products.csv")
            result_label.config(text="Product added successfully!!",fg="white")
            pid_entry.delete(0,tk.END)
            pname_entry.delete(0,tk.END)
            price_entry.delete(0,tk.END)
            stock_entry.delete(0,tk.END)
            category_entry.delete(0,tk.END)
        else:
            result_label.config(text="This product id already exists",fg="#DC394F")
    add_button=tk.Button(window,text="Add product",command=add_product,font=("Segoe UI",10),bg='#A98F76',fg="white")
    add_button.pack(padx=10,pady=3)

#3.admin
def remove_product_window(user:Admin):
    window=tk.Toplevel(root)
    window.title("Remove")
    window.geometry("700x550")
    window.config(bg="#D8CBBA")
    remove_label=tk.Label(window,text="Enter the Product_id:",font=("Calibri",12),bg='#A98F76',fg="white")
    remove_label.pack(pady=5)
    remove_entry=tk.Entry(window)
    remove_entry.pack()
    result_label=tk.Label(window,text="",font=("Calibri",12),bg="#D8CBBA")
    result_label.pack(pady=5)
    def remove_product():
        p_id=remove_entry.get()
        removed=user.remove_product(store,p_id)
        if removed:
            store.save_products("products.csv")
            result_label.config(text="Product removed successfully!!",fg="white")
            remove_entry.delete(0,tk.END)
        else:
            result_label.config(text=f"There is no product with id:'{p_id}'",fg="#DC394F")
    remove_button=tk.Button(window,text="Remove",command=remove_product,font=("Segoe UI",10),bg='#A98F76',fg="white")
    remove_button.pack(padx=10,pady=3)
#3.admin
def edit_product_window(user:'Admin'):
    window=tk.Toplevel(root)
    window.geometry('700x550')
    window.title("edit panel")
    window.config(bg="#D8CBBA")
    pid_label=tk.Label(window,text="Product ID:",font=("Calibri",12),bg='#A98F76',fg="white")
    pid_label.pack(pady=5)
    pid_entry=tk.Entry(window)
    pid_entry.pack()
    price_label=tk.Label(window,text="Changed Price(orleave it empty",font=("Calibri",12),bg='#A98F76',fg="white")
    price_label.pack(pady=5)
    price_entry=tk.Entry(window)
    price_entry.pack()
    stock_label=tk.Label(window,text="Changed Stock:",font=("Calibri",12),bg='#A98F76',fg="white")
    stock_label.pack(pady=5)
    stock_entry=tk.Entry(window)
    stock_entry.pack()
    result_label=tk.Label(window,text="",font=("Calibri",12),bg="#D8CBBA")
    result_label.pack(pady=5)
    def edit_product():
        pid=pid_entry.get()
        try:
            price=float(price_entry.get()) if price_entry.get() else None
            if price is not None and price<=0:
                result_label.config(text="price must be greater than zero",fg="#DC394F")
                return
        except ValueError:
            result_label.config(text="Price must be a number",fg="#DC394F")
            return
        try:
            stock=int(stock_entry.get()) if stock_entry.get() else None
            if stock is not None and stock<0:
                result_label.config(text="stok must be greater than zero",fg="#DC394F")
                return
        except ValueError:
            result_label.config(text="Stock must be a number",fg="#DC394F")
            return
        edited=user.edit_product(store,pid,price,stock)
        if edited:
            result_label.config(text="The changes applied successfully",fg="white")
            store.save_products("products.csv")
            pid_entry.delete(0,tk.END)
            price_entry.delete(0,tk.END)
            stock_entry.delete(0,tk.END)
        else:
            result_label.config(text="Product Id Not Found",fg="#DC394F")
    edit_button=tk.Button(window,text="edit",command=edit_product,font=("Segoe UI",10),bg='#A98F76',fg="white")
    edit_button.pack(padx=10,pady=3)
        
#4.admin
def view_orders(listbox:'tk.Listbox'):
    global current_view
    current_view="orders"
    listbox.delete(0,tk.END)
    if len(store.orders)==0:
        listbox.insert(tk.END,"No Orders Yet")
    for order in store.orders:
        listbox.insert(tk.END,
                       f"{order["username"]:<20}"
                       f"{order["product_id"]:<10}"
                       f"{order["quantity"]:<10}"
                       f"${order["total_price"]:<10}"
                       f"{order["date"]}")
#admin
def sale_statistics():
    window=tk.Toplevel(root)
    window.geometry('700x550')
    window.title("Sale Statistics")
    window.config(bg="#D8CBBA")
    tk.Label(window,text="Sale Statics:",font=("Calibri",16,"bold"),bg='#A98F76',fg="white").pack(pady=5)
    tk.Label(window,text=f"Total Orders:{len(store.orders)}",font=("Calibri",12),bg='#A98F76',fg="white").pack(pady=5)
    sale_revenue:float=0
    for order in store.orders:
        sale_revenue+=float(order["total_price"])
    tk.Label(window,text=f"Total Revenue:${sale_revenue:.2f}",font=("Calibri",12),bg='#A98F76',fg="white").pack(pady=5)
    customers=[]
    for order in store.orders:
        if order["username"] not in customers:
            customers.append(order["username"])
    tk.Label(window,text=f"Total Customers:{len(customers)}",font=("Calibri",12),bg='#A98F76',fg="white").pack(pady=5)
#admin
def show_users(listbox:'tk.Listbox'):
    global current_view
    current_view="users"
    listbox.delete(0,tk.END)
    for user in store.users:
        listbox.insert(tk.END,
                       f"User: {user.username}|"
                       f"Balance: {user.balance}"
                       )
#admin
def search_users_window():
    window=tk.Toplevel(root)
    window.geometry('700x550')
    window.title("Search users")
    window.config(bg="#D8CBBA")
    name_label=tk.Label(window,text="Username:",font=("Calibri",12),bg='#A98F76',fg="white")
    name_label.pack(pady=5)
    name_entry=tk.Entry(window)
    name_entry.pack(pady=5)
    scrollbar=tk.Scrollbar(window)
    listbox=tk.Listbox(window,width=80,height=20,bg="#F1E3D6",fg="#8F6C58",yscrollcommand=scrollbar.set,font=("Calibri",13))
    scrollbar.config(command=listbox.yview)
    def find_users():
        listbox.delete(0,tk.END)
        username_part=name_entry.get()
        if len(store.users)==0:
            listbox.insert(tk.END,"There's No User")
            return
        found=False
        for user in store.users:
            if username_part.lower() in user.username.lower():
                found=True
                listbox.insert(tk.END,
                               f"Username:{user.username:<20}|"
                               f"Balance:{user.balance:<10}")
        if not found:
            listbox.insert(tk.END,"No Matching Was Found")
    find_button=tk.Button(window,text="Search",command=find_users,font=("Segoe UI",10),bg='#A98F76',fg="white")
    find_button.pack(padx=10,pady=3)
    scrollbar.pack(side="right",fill="y")
    listbox.pack(side="left",fill="both",expand=True)

 #
def change_password_window(user:User):
    window=tk.Toplevel(root)
    window.geometry('700x550')
    window.title("Change Password")
    window.config(bg="#D8CBBA")
    pass_label=tk.Label(window,text="Current Password:",font=("Calibri",12),bg='#A98F76',fg="white")
    pass_label.pack(pady=5)
    pass_entry=tk.Entry(window)
    pass_entry.pack(pady=5)
    new_label=tk.Label(window,text="New Password:",font=("Calibri",12),bg='#A98F76',fg="white")
    new_label.pack(pady=5)
    new_entry=tk.Entry(window)
    new_entry.pack(pady=5)
    result_label=tk.Label(window,text="",font=("Calibri",12,"bold"),bg="#D8CBBA")
    result_label.pack(pady=5)
    def check_changes():
        before=pass_entry.get()
        now=new_entry.get()
        if not before==user.password:
            result_label.config(text="Current Password is Wrong",fg="#DC394F")
            return
        if now==before:
            result_label.config(text="Yoy Didn't Change The Password",fg="#DC394F")
            return
        if now=="":
            result_label.config(text="New Password Can't be Empty",fg="#DC394F")
            return
        else:
            user.password=now
            store.save_users("users.csv")
            result_label.config(text="Password Changed Successfully",fg="#4ddb50")
    change_button=tk.Button(window,text="Change",command=check_changes,font=("Segoe UI",10),bg='#A98F76',fg="white")
    change_button.pack(padx=10,pady=3)
from datetime import datetime
def open_product_details(event,listbox:tk.Listbox,user:Customer):
    global current_view
    if current_view!="products":
        return    
    selected=listbox.curselection()
    if not selected:
            return    
    selected_text=listbox.get(selected[0])
    produdt_id=selected_text.split("|")[0].strip()
    product=None
    for p in store.products:
        if p.product_id==produdt_id:
            product=p
    if product is None:
        return
    window=tk.Toplevel(root)
    window.geometry('700x550')
    window.title(f"{product.category} info")
    window.config(bg="#D8CBBA")
    main_frame=tk.Frame(window,bg="#D8CBBA")
    main_frame.pack(fill="both",expand=True)
    img_path=os.path.join("Images",f"{product.product_id}.jpg")
    image_frame=tk.Frame(main_frame,bg="#F1E3D6",bd=2,relief="groove")
    image_frame.pack(pady=10)
    if os.path.exists(img_path):
        image=Image.open(img_path)
        image=image.resize((150,150))
        photo=ImageTk.PhotoImage(image)
        img_label=tk.Label(image_frame,image=photo,bg="#F1E3D6")
        img_label.image=photo
        img_label.pack(pady=10,padx=10)
    else:
        tk.Label(image_frame,text="No Image Availabel",fg="#8F6C58").pack(pady=10)
    info_frame=tk.Frame(main_frame,bg="#F1E3D6",bd=2,relief="groove")
    info_frame.pack(fill="x",padx=10,pady=10)
    tk.Label(info_frame,text=f"ID:{product.product_id}",font=("Calibri",12,"bold"),fg="#7E5B3A",bg="#D8CBBA").pack(pady=5)
    tk.Label(info_frame,text=f"Name:{product.name}",font=("Calibri",12,"bold"),fg="#7E5B3A",bg="#D8CBBA").pack(pady=5)
    tk.Label(info_frame,text=f"Price:${product.price:.2f}   Stock:{product.stock}",font=("Calibri",12),fg='#7E5B3A',bg="#D8CBBA").pack(pady=5)
    tk.Label(info_frame,text=f"Category:{product.category}",font=("Calibri",12),fg='#7E5B3A',bg="#D8CBBA").pack(pady=5)
    comment_frame=tk.Frame(main_frame,bg="#D8CBBA")
    comment_frame.pack(fill="both",expand=True)
    scrollbar=tk.Scrollbar(comment_frame)
    comments_listbox=tk.Listbox(comment_frame,height=7,bg="#F1E3D6",fg="#8F6C58",yscrollcommand=scrollbar.set)
    scrollbar.config(command=comments_listbox.yview)
    scrollbar.pack(side="right",fill="y")
    comments_listbox.pack(side="left",fill="both",expand=True)


    for comment in store.comments:
        if comment["product_id"]==product.product_id:
            comments_listbox.insert(tk.END,
                                    "Comment:"
                                    f"{comment["username"]:<15}:{comment["comment"]:<50}|{comment['date']}")
    bottom_frame=tk.Frame(main_frame,bg="#D8CBBA")
    bottom_frame.pack(fill="x",pady=10)
    comment_entery=tk.Entry(bottom_frame)
    comment_entery.pack(side="left",fill="x",expand=True,padx=5)
    def submit_comment():
        text=comment_entery.get()
        if text.strip()=="":
            return
        store.add_comment(product.product_id,user.username,text)
        store.save_comments("comments.csv")
        comments_listbox.insert(tk.END,f"Comment:{user.username:<15}:{text:<50}|{datetime.now().strftime("%Y-%m-%d")}")
        comment_entery.delete(0,tk.END)
    submit_button=tk.Button(bottom_frame,text="submit",command=submit_comment,font=("Segoe UI",8),bg='#A98F76',fg="white")
    submit_button.pack(side="right")

def view_comments(listbox:'tk.Listbox'):
    global current_view
    current_view="comments"
    listbox.delete(0,tk.END)
    for comment in store.comments:
        listbox.insert(tk.END,
                       "Comment:"
                       f"{comment["product_id"]:<10}|"
                       f"{comment["username"]:<15}|"
                       f"'{comment["comment"]:<50}'|"
                       f"{comment["date"]}")
        
def apply_discount_window():
    window=tk.Toplevel(root)
    window.geometry('700x550')
    window.title("Applying Discount")
    window.config(bg="#D8CBBA")
    pid_label=tk.Label(window,text="Product ID:",font=("Calibri",12),bg='#A98F76',fg="white")
    pid_label.pack(pady=5)
    pid_entry=tk.Entry(window)
    pid_entry.pack()
    discount_label=tk.Label(window,text="Discount(percent):",font=("Calibri",12),bg='#A98F76',fg="white")
    discount_label.pack(pady=5)
    discount_entry=tk.Entry(window)
    discount_entry.pack()
    result_label=tk.Label(window,text="",font=("Calibri",12),bg="#D8CBBA")
    result_label.pack(pady=5)
    def discount():
        pid=pid_entry.get()
        result=False
        for product in store.products:
            if product.product_id.lower()==pid.lower():
                result=True
                p=product
        if not result:
            result_label.config(text="Product ID Not Found",fg="#DC394F")
            return
        try:
            discount=int(discount_entry.get())
        except ValueError:
            result_label.config(text="Discount Must Be A Number",fg="#DC394F")
            return
        applied=p.apply_discount(discount)
        if applied:
            store.save_products("products.csv")
            result_label.config(text=f"Discount Applied Succcessfully!!\nwith %{discount}:{p.price}",fg="#34D136")
            pid_entry.delete(0,tk.END)
            discount_entry.delete(0,tk.END)
        else:
            result_label.config(text="Discount Number Out Of Range",fg="#DC394F")
    change_button=tk.Button(window,text="Apply",command=discount,font=("Segoe UI",10),bg='#A98F76',fg="white")
    change_button.pack(padx=10,pady=3)

def sale_report_by_date():
    window=tk.Toplevel(root)
    window.geometry('700x550')
    window.title("Sale Reports Based Date")
    window.config(bg="#D8CBBA")
    year_label=tk.Label(window,text="Enter The Year:",font=("Calibri",12),bg='#A98F76',fg="white")
    year_label.pack(pady=5)
    year_entry=tk.Entry(window)
    year_entry.pack()
    month_label=tk.Label(window,text="Enter the Month:",font=("Calibri",12),bg='#A98F76',fg="white")
    month_label.pack(pady=5)
    month_entry=tk.Entry(window)
    month_entry.pack()
    day_label=tk.Label(window,text="Enter Day:",font=("Calibri",12),bg='#A98F76',fg="white")
    day_label.pack(pady=5)
    day_entry=tk.Entry(window)
    day_entry.pack()
    scrollbar=tk.Scrollbar(window)
    listbox=tk.Listbox(window,width=80,height=20,bg="#F1E3D6",fg="#8F6C58",yscrollcommand=scrollbar.set,font=("Calibri",13))
    scrollbar.config(command=listbox.yview)
    def sale_report():
        listbox.delete(0,tk.END)
        if year_entry.get().strip()=="" or month_entry.get().strip()=="" or day_entry.get().strip()=="":
            listbox.insert(tk.END,"Fill All The Fields")
            return
        try:
            year=int(year_entry.get())
            month=int(month_entry.get())
            day=int(day_entry.get())
        except ValueError:
            listbox.insert(tk.END,"You Should Enter Number")
            return
        date=f"{year}-{month:02d}-{day:02d}"
        sale_list=[]
        for order in store.orders:
            if order["date"]==date:
                sale_list.append(order)
        if len(sale_list)==0:
            listbox.insert(tk.END,f"No Sale Recorded in {date}")
            return
        for sale in sale_list:
            listbox.insert(tk.END,
                           f"{sale['username']:<25}|"
                           f"{sale['product_id']:<10}|"
                           f"Quantity:{sale['quantity']:<4}|"
                           f"${sale['total_price']:<10}|"
                           f"{sale["date"]}")
    find_button=tk.Button(window,text="Search",command=sale_report,font=("Segoe UI",10),bg='#A98F76',fg="white")
    find_button.pack(padx=10,pady=3)
    scrollbar.pack(side="right",fill="y")
    listbox.pack(side="left",fill="both",expand=True)

def sale_report_by_product():
    window=tk.Toplevel(root)
    window.geometry('700x550')
    window.title("Sale Reports Based Product")
    window.config(bg="#D8CBBA")
    product_label=tk.Label(window,text="Product ID",font=("Calibri",12),bg='#A98F76',fg="white")
    product_label.pack(pady=5)
    product_entry=tk.Entry(window)
    product_entry.pack()
    scrollbar=tk.Scrollbar(window)
    listbox=tk.Listbox(window,width=80,height=20,bg="#F1E3D6",fg="#8F6C58",yscrollcommand=scrollbar.set,font=("Calibri",13))
    scrollbar.config(command=listbox.yview)
    def sale_report():
        listbox.delete(0,tk.END)
        if product_entry.get().strip()=="":
            listbox.insert(tk.END,"Fill The Field!")
            return
        pid=product_entry.get()
        sales=[]
        for order in store.orders:
            if order["product_id"].lower()==pid.lower():
                sales.append(order)
        if len(sales)==0:
            listbox.insert(tk.END,"No Report Found")
            return
        for sale in sales:
            listbox.insert(tk.END,
                           f"{sale['username']:<25}|"
                           f"{sale['product_id']:<10}|"
                           f"Quantity:{sale['quantity']:<4}|"
                           f"${sale['total_price']:<10}|"
                           f"{sale["date"]}")
    find_button=tk.Button(window,text="Search",command=sale_report,font=("Segoe UI",10),bg='#A98F76',fg="white")
    find_button.pack(padx=10,pady=3)
    scrollbar.pack(side="right",fill="y")
    listbox.pack(side="left",fill="both",expand=True)

def logout(panel):
    panel.destroy()
    username_entry.delete(0,tk.END)
    password_entry.delete(0,tk.END)
    username_label.pack(pady=5)
    username_entry.pack(pady=5)
    password_label.pack(pady=5)
    password_entry.pack(pady=5)
    login_button.pack(pady=10)
    login_label.config(text='')

