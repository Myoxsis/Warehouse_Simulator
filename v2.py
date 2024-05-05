import simpy
import random

# Define parameters
SIMULATION_TIME = 1000
CUSTOMER_ORDER_RATE = 0.5
BOM = {'material1': 5, 'material2': 7}  # Bill of Materials with material names and quantities
DELIVERY_TIME_MEAN = 2
INSPECTION_TIME_MEAN = 1
PRODUCTION_TIME_MEAN = 3

class Manufacturer:
    def __init__(self, env, bom):
        self.env = env
        self.bom = bom
        self.warehouse = simpy.Container(env, init=0)
        self.production_line = simpy.Resource(env, capacity=1)
        self.orders_to_supplier = []
        self.material_received = {material: 0 for material in self.bom}
        self.final_goods = simpy.Container(env, init=0)
        self.supplier_process = env.process(self.receive_orders_from_supplier())

    def start_supply_process(self):
        self.env.process(self.check_bom_and_generate_orders())

    def check_bom_and_generate_orders(self):
        while True:
            required_materials = self.get_required_materials()
            for material, quantity in required_materials.items():
                if self.material_received[material] < quantity:
                    self.generate_order_to_supplier(material, quantity - self.material_received[material])
            yield self.env.timeout(1)  # Check BOM periodically

    def generate_order_to_supplier(self, material, quantity):
        order = {'material': material, 'quantity': quantity}
        self.orders_to_supplier.append(order)
        print(f"Generated order to supplier for {quantity} units of {material} at {self.env.now}")

    def receive_orders_from_supplier(self):
        while True:
            if self.orders_to_supplier:
                order = self.orders_to_supplier.pop(0)
                yield self.env.timeout(random.expovariate(1/DELIVERY_TIME_MEAN))  # Wait for delivery time
                self.receive_material(order['material'], order['quantity'])
                print(f"Received {order['quantity']} units of {order['material']} from supplier at {self.env.now}")
            else:
                yield self.env.timeout(1)  # Check for new orders periodically

    def receive_material(self, material, quantity):
        self.material_received[material] += quantity
        self.warehouse.put(quantity)

    def inspect_material(self):
        yield self.env.timeout(random.expovariate(1/INSPECTION_TIME_MEAN))  # Simulate inspection time
        print(f"Material inspection completed at {self.env.now}")

    def store_material(self, quantity):
        yield self.warehouse.get(quantity)

    def deliver_to_production_line(self):
        while True:
            required_materials = self.get_required_materials()
            if all(self.material_received[material] >= quantity for material, quantity in required_materials.items()):
                yield self.production_line.request()
                for material, quantity in required_materials.items():
                    yield self.store_material(quantity)
                    self.material_received[material] -= quantity
                print(f"All required materials received. Delivered to production line at {self.env.now}")
                yield self.env.timeout(random.expovariate(1/PRODUCTION_TIME_MEAN))  # Simulate production time
                self.final_goods.put(1)
                self.production_line.release()

    def get_required_materials(self):
        return self.bom

class Supplier:
    def __init__(self, env):
        self.env = env

class Customer:
    def __init__(self, env, manufacturer):
        self.env = env
        self.manufacturer = manufacturer

    def order_material(self):
        while True:
            yield self.env.timeout(random.expovariate(CUSTOMER_ORDER_RATE))
            self.manufacturer.start_supply_process()
            print(f"Customer ordered materials at {self.env.now}")

# Setup and start the simulation
env = simpy.Environment()
manufacturer = Manufacturer(env, BOM)
customer = Customer(env, manufacturer)
env.process(customer.order_material())
env.run(until=SIMULATION_TIME)