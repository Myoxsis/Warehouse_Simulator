import simpy
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Define parameters
SIMULATION_TIME = 1000
NUM_PRODUCT = 20
PRODUCTION_RATE = 1
SHIPPING_TIME = 2
CUSTOMER_ORDER_RATE = 0.5
ORDER_RECEPTION = 1
STORE_TIME = 0.75

def format_time(sim_time):
    start_time = datetime(2024, 1, 1)
    sim_time_delta = timedelta(hours=sim_time)
    return start_time + sim_time_delta


class Material:
    def __init__(self, price, delivery_time) -> None:
        self.price = price
        self.delivery_time = delivery_time

class ManufacturingCompany:
    def __init__(self, env, num_products) -> None:
        self.env = env
        self.production_machine = simpy.Resource(env, capacity=1)
        self.warehouse = simpy.Container(env, init=num_products)
        self.material_cost = 0 # Initialize material costs
        self.material_prices = []
        self.parts_received = []
        self.receiving_process = env.process(self.receive_goods())
        self.inspection_process = env.process(self.inspect_goods())

    def produce(self):
        while True:
            with self.production_machine.request() as request:
                yield request
                yield self.env.timeout(PRODUCTION_RATE)
                yield self.warehouse.put(1)

    def ship_product(self):
        while True:
            yield self.env.timeout(SHIPPING_TIME)
            yield self.warehouse.get(1)
            print(f"Order shipped at {format_time(env.now)}")

    def receive_goods(self):
        while True:
            material_price = random.uniform(1, 10)
            self.material_prices.append((self.env.now, material_price))
            self.material_cost += material_price
            yield self.warehouse.put(1)
            self.parts_received.append((self.env.now, self.warehouse.level))
            yield self.env.timeout(ORDER_RECEPTION) # Time it takes to receive goods
            yield self.env.process(self.inspect_goods())
            print(f"Received goods at time {format_time(env.now)} Material Price : $ {material_price}")

    def inspect_goods(self):
            yield self.env.timeout(random.uniform(0.5, 1.1))
            print(f"Goods inspected and passed at time {format_time(env.now)}")

    def store_goods(self):
        while True:
            yield self.env.timeout(STORE_TIME) # Time it takes to receive goods
            yield self.warehouse.put(1)
            print(f"Store goods at time {format_time(env.now)}")

    def buy_material(self, material):
        yield self.env.timeout(material.delivery_time)
        self.material_prices.append((self.env.now, material.price))
        self.material_cost == material.price
        print(f"Bought Material at {format_time(env.now)} for {material.price}")

class Customer:
    def __init__(self, env, company) -> None:
        self.env = env
        self.company = company

    def order_product(self):
        while True:
            yield env.timeout(random.expovariate(CUSTOMER_ORDER_RATE))
            if self.company.warehouse.level >=1:
                yield self.company.warehouse.get(1)
                print(f"Customer received a product at time {format_time(env.now)}")
            else:
                print(f"No product available for customer at time {format_time(env.now)}")

def plot_material_and_prices(material_prices, parts_received):
    fig, axes = plt.subplots(3, 1, figsize=(10, 10))

    
    times, prices = zip(*material_prices)
    axes[0].plot(times, prices, color='b')
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('Material Price')
    axes[0].set_title('Evolution of Material Price')

    times, parts = zip(*parts_received)
    axes[1].plot(times, parts, color='r')
    axes[1].set_xlabel('Time')
    axes[1].set_ylabel('Number of parts received')
    axes[1].set_title('Evolution of Part Received')

    #calculate cumulative value of mateaerial cost
    cumulative_material_cost = [0]
    for time, price in material_prices:
        cumulative_material_cost.append(cumulative_material_cost[-1] + price)
    axes[2].plot([time for time, _ in material_prices], cumulative_material_cost[1:], color='g')
    axes[2].set_xlabel('Time')
    axes[2].set_ylabel('Cumulated costs')
    axes[2].set_title('Evolution of cumulated costs')


    plt.tight_layout()
    plt.show()

# Setup and start simulation
env = simpy.Environment()
company = ManufacturingCompany(env, NUM_PRODUCT)
env.process(company.produce())
env.process(company.ship_product())

customer = Customer(env, company)
env.process(customer.order_product())

material1 = Material(price=5, delivery_time=2)
material2 = Material(price=17, delivery_time=4)
material3 = Material(price=52, delivery_time=6)
material4 = Material(price=0.5, delivery_time=1)
env.process(company.buy_material(material1))
env.process(company.buy_material(material2))
env.process(company.buy_material(material3))
env.process(company.buy_material(material4))

env.run(until=SIMULATION_TIME)

print(f"Total Material cost : ${company.material_cost}")

plot_material_and_prices(company.material_prices, company.parts_received)