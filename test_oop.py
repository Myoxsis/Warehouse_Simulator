class Product:
    def __init__(self, name, price, description, stock):
        self.name = name
        self.price = price
        self.description = description
        self.stock = stock

    def update_stock(self, quantity):
        self.stock += quantity

    def total_value(self):
        return self.stock * self.price
    
class Order:
    def __init__(self, customer, product, quantity):
        self.customer = customer
        self.product = product
        self.quantity = quantity

    def total_cost(self):
        return self.quantity * self.product.price
    
class Customer:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.orders = []

    def place_order(self, product, quantity):
        if product.stock >= quantity:
            order = Order(self, product, quantity)
            product.update_stock(-quantity)
            self.orders.append(order)
        else:
            print("Error: Not enough stock")
    
    def view_orders(self):
        for order in self.orders:
            print(order)

class Store:
  def __init__(self):
    self.products = []
    self.orders = []
    self.customers = []
    
  def add_product(self, product):
      self.products.append(product)
  
  def delete_product(self, product):
      self.products.remove(product)
  
  def add_customer(self, customer):
    self.customers.append(customer)

  def delete_customer(self, customer):
      self.customers.remove(customer)
  
  def add_order(self, order):
      self.orders.append(order)
  
  def delete_order(self, order):
      self.orders.remove(order)
  
  def find_product(self, name):
      for product in self.products:
          if product.name == name:
              return product
      return None
  
  def find_customer(self, name):
      for customer in self.customers:
          if customer.name == name:
              return customer
      return None
  
  def display_customer_list(self):
      for customer in self.customers:
          print(customer.name)
  
  def sales_report(self):
      total_sales = 0
      for order in self.orders:
          total_sales += order.total_cost()
      return total_sales
  
  def restock_report(self):
      low_stock = []
      for product in self.products:
          if product.stock < 10:
              low_stock.append(product)
      return low_stock
  
# Test the classes
store = Store()

product1 = Product("Keyboard", 49.99, "Wireless keyboard", 100)
product2 = Product("Mouse", 29.99, "Wireless mouse", 50)
store.add_product(product1)
store.add_product(product2)

customer1 = Customer("John Smith", "john@example.com")
customer2 = Customer("Jane Doe", "jane@example.com")
store.add_customer(customer1)
store.add_customer(customer2)

customer1.place_order(product1, 1)
customer2.place_order(product2, 2)

print("Total sales:", store.sales_report())
print("Low stock:", store.restock_report())

customer1.view_orders()