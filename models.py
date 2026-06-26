from datetime import datetime
class Product:
    def __init__(self,product_id,name,price,stock,category):
        self.product_id=product_id
        self.name=name
        self.price=float(price)
        self.stock=int(stock)
        self.category=category

    def __str__(self):
        return(f"id:{self.product_id}-name:{self.name}-${self.price}-Stock:{self.stock}")

    def show_info(self):
        return (f"product id:{self.product_id}\n"
        f"name:{self.name}\n"
        f"price:{self.price}\n"
        f"category:{self.category}\n"
        f"stock:{self.stock}")

    def apply_discount(self,percent):
        if 0<=percent<=100:
            self.price-=self.price*percent/100
            return True
        return False
    def is_available(self):
        return self.stock>0
    
class User:
    def __init__(self,username,password,balance):
        self.username=username
        self.password=password
        self.balance=float(balance)
    def __str__(self):
        return f"{self.username}-Balance:{self.balance}"
    def check_password(self,password):
        return self.password==password
    
class Customer(User):
    def __init__(self, username, password, balance):
        super().__init__(username, password, balance)
        self.cart=[]
    def add_to_cart(self,product:Product,quantity:int):
        if quantity<=0 or quantity>product.stock:
            return False
        for item in self.cart:
            if item["product"]==product:
                if item["quantity"]+quantity<=product.stock:
                    item["quantity"]+=quantity
                    return True
                return False
        self.cart.append({
            "product":product,
            "quantity":quantity
            })
        return True            
    def view_cart(self):
        if len(self.cart)>0:
            a="your cart:"
            for product in self.cart:
                a+=f'\nproduct:{product["product"].name} quantity:{product["quantity"]} price:{product["quantity"]*(product["product"].price)}'
            
            return a
        return "your cart is still empty"
        
    def calculate_total(self):
        total=0
        for item in self.cart:
            total+=(item["product"].price)*(item["quantity"])
        return total
    def remove(self,product_id):
        for item in self.cart:
            if item["product"].product_id==product_id:
                self.cart.remove(item)
                return True
        return False
    
class Admin(User):
    def add_product(self,store:"Store",product):
        return store.add_product(product)
    def remove_product(self,store:"Store",product_id):
        return store.remove_product(product_id)
    def edit_product(self,store:"Store",product_id,price=None,stock=None):
        return store.edit_product(product_id,price,stock)
    def view_order(self,store:"Store"):
        return store.view_orders()

import csv
class Store:
    def __init__(self):
        self.products=[]
        self.users=[]
        self.orders=[]
        self.comments=[]
    def show_products(self):
        if len(self.products)>0:
            text="Products:"
            for product in self.products:
                text+=f"\n{product}"
        else:
            text="there is no product"
        return text
    def search_product(self,name:str):
        result=[]
        for product in self.products:
            if name.lower() in product.name.lower():
                result.append(product)
        return result
    def adding_customer(self,username,password,balance):
        for user in self.users:
            if user.username==username:
                return False

        new_user=Customer(username,password,balance)
        self.users.append(new_user)
        return True
    def load_products(self,file_path):
        with open(file_path,"r",encoding="utf-8") as file:
            content=csv.reader(file)
            next(content)#چون ردیف اول سر ستون هاست
            for row in content:
                if len(row)>=5:
                    self.products.append(Product(row[0],row[1],row[2],row[3],row[4]))
        return self.products
    def load_users(self,file_path):
        with open(file_path,"r",encoding="utf8") as file:
            content=csv.reader(file)
            next(content)
            for row in content:
                role=row[3]
                if role.lower()=="admin":
                    self.users.append(Admin(row[0],row[1],float(row[2])))
                elif role.lower()=="customer":
                    self.users.append(Customer(row[0],row[1],float(row[2])))
        return self.users
    def load_orders(self,file_path):
        with open(file_path,"r",encoding="utf8") as f:
            content=csv.reader(f)
            next(content)
            for row in content:
                self.orders.append({"username":row[0],"product_id":row[1],"quantity":row[2],"total_price":row[3],"date":row[4]})
        return self.orders
    def load_comments(self,file_path):
        with open(file_path,"r",encoding="utf8") as f:
            content=csv.reader(f)
            next(content)
            for row in content:
                self.comments.append({
                    "product_id":row[0] ,
                               "username":row[1],
                               "comment":row[2],
                               "date":row[3]
                               })
    def login(self,username,password):
        for user in self.users:
            if user.username==username and user.check_password(password):
                return user
        return False
    def checkout(self,customer:Customer):
        if len(customer.cart)==0:
            return False
        total=customer.calculate_total()
        if customer.balance<total:
            return False
        customer.balance-=total
        for item in customer.cart:
            item["product"].stock-=int(item["quantity"])
            self.orders.append(
                {
                "username":customer.username,
                "product_id":item["product"].product_id,
                "quantity":item["quantity"],
                "total_price":float(item["product"].price*item["quantity"]),
                "date":datetime.now().strftime('%Y-%m-%d')
                }
                    )
        customer.cart.clear()
        return True
    def save_orders(self,file_path):
        header=["username","product_id","quantity","total_price","date"]
        with open(file_path,"w",encoding="utf8",newline="") as file:
            writer=csv.writer(file)
            writer.writerow(header)
            for order in self.orders:
                writer.writerow([order["username"],order["product_id"],order["quantity"],order["total_price"],order["date"]])
    def save_products(self,file_path):
        header=["product_id","name","price","stock","category"]
        with open(file_path,"w",encoding="utf8",newline="") as f:
            writer=csv.writer(f)
            writer.writerow(header)
            for product in self.products:
                writer.writerow([product.product_id,
                                product.name,
                                product.price,
                                product.stock,
                                product.category])
    def save_users(self,file_path):
        header=["username","password","balance","role"]
        with open(file_path,"w",encoding="utf8",newline="") as f:
            writer=csv.writer(f)
            writer.writerow(header)
            for user in self.users:
                role="customer"
                if isinstance(user,Admin):
                    role="admin"
                writer.writerow([user.username,user.password,user.balance,role])
    def save_comments(self,file_path):
        with open(file_path,"w",encoding="utf8",newline="") as file:
            writer=csv.writer(file)
            writer.writerow(["product_id","username","comment","date"])
            for comment in self.comments:
                writer.writerow([
                    comment["product_id"],
                    comment["username"],
                    comment["comment"],
                    comment["date"]
                ])
    def add_comment(self,product_id,username,comment):
        self.comments.append({
            "product_id":product_id,
            "username":username,
            "comment":comment,
            "date": datetime.now().strftime("%Y-%m-%d")})
    def add_product(self,product:Product):
        for p in self.products:
            if p.product_id==product.product_id:
                return False
        self.products.append(product)
        return True
    def remove_product(self,product_id):
        for product in self.products:
            if product.product_id==product_id:
                self.products.remove(product)
                return True
        return False
    def edit_product(self,product_id,new_price=None,new_stock=None):
        for product in self.products:
            if product_id==product.product_id:
                if new_price is not None:
                    product.price=new_price
                if new_stock is not None:
                    product.stock=new_stock
                return True
        return False
    def view_orders(self):
        return self.orders