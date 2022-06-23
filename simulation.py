#!/usr/bin/env python
# coding: utf-8

import simpy, random, statistics
import matplotlib.pyplot as plt

customers_handled_cashier_l = [[], []]
customers_handled_usher_l = [[], []]

customers_handled_cashier = 0
customers_handled_usher = 0

class Warehouse(object):
    def __init__(self, env, nb_cashiers, nb_servers, nb_ushers):
        self.env = env
        self.cashier = simpy.Resource(env, nb_cashiers)
        self.server = simpy.Resource(env, nb_servers)
        self.usher = simpy.Resource(env, nb_ushers)
        
    def purchase_ticket(self, moviegoer):
        yield self.env.timeout(random.randint(1, 3))
        
    def check_ticket(self, moviegoer):
        yield self.env.timeout(random.randint(1, 6))
        
def moviegoer(env, name, theater):
    global customers_handled_cashier, customers_handled_usher
    print(f"Custmer {name} arrived at {env.now:.2f}")
    with theater.cashier.request() as request:
        yield request
        print(f"Customer {name} with Cashier")
        yield env.process(theater.purchase_ticket(name))
        customers_handled_cashier +=1
        customers_handled_cashier_l[0].append(customers_handled_cashier)
        customers_handled_cashier_l[1].append(env.now)
    with theater.usher.request() as request :
        yield request
        print(f"Customer {name} with Usher")
        yield env.process(theater.check_ticket(name))
        customers_handled_usher +=1
        customers_handled_usher_l[0].append(customers_handled_usher)
        customers_handled_usher_l[1].append(env.now)
    
def setup(env, nb_cashiers, nb_servers, nb_ushers):
    theater = Warehouse(env, nb_cashiers, nb_servers, nb_ushers)
    
    for i in range(1, 6):
        env.process(moviegoer(env, i, theater))
    while True:
        yield env.timeout(random.randint(1, 3))
        i += 1
        env.process(moviegoer(env, i, theater))
    
print('// Starting Simulation')
env = simpy.Environment()
env.process(setup(env, 2, 1, 1))
env.run(until=60)
print('// Ending Simulation')

plt.plot(customers_handled_cashier_l[0], customers_handled_cashier_l[1], label='Cashier')
plt.plot(customers_handled_usher_l[0], customers_handled_usher_l[1], label='Usher')
plt.legend()
plt.show()




# Warehouse
#   Processes
#       Reception
#       Put in Stock
#       Pick from stok
#       Handling Units
#       Loading
#       Transportation starts