#!/usr/bin/env python
# coding: utf-8

import simpy, random, statistics
import numpy as np
import matplotlib.pyplot as plt

def inbound_run(env, reception_team, inspection_r_team, putaway_team):
    global cost 

    cost = 0.0

    i = 0
    while True:
        # inbound process
        yield env.timeout(generate_shipment_arrival())
        print(f"{env.now} -  Shipment n°{i} inbound")
        env.process(goods_receipt(env, reception_team, i))
        yield env.timeout(generate_interactivity_time())
        env.process(inspection_at_reception(env, inspection_r_team, i))
        yield env.timeout(generate_interactivity_time())
        env.process(putaway(env, putaway_team, i))

        i += 1

def outbound_run(env, picking_team, packing_team, inspection_s_team, shipping_team):
    i = 0
    while True:
        # inbound process
        yield env.timeout(generate_delivery_arrival())
        print(f"{env.now} -  Delivery n°{i} inbound")
        env.process(picking(env, picking_team, i))
        yield env.timeout(generate_interactivity_time())
        env.process(packing(env, packing_team, i))
        yield env.timeout(generate_interactivity_time())
        env.process(inspection_at_shipping(env, inspection_s_team, i))
        yield env.timeout(generate_interactivity_time())
        env.process(shipping(env, shipping_team, i))
        i += 1
    
def goods_receipt(env, reception_team, name):
    with reception_team.request() as request:
        yield request
        yield env.timeout(generate_reception())
    print(f"{env.now} -  Shipment {name} received")

def inspection_at_reception(env, inspection_r_team, name):
    inspection_flag = np.random.randint(1, 10)
    if inspection_flag >= 8:
        print(f"{env.now} -  Shipment {name} : inspection required")
        with inspection_r_team.request() as request:
            yield request
            yield env.timeout(generate_insp_recp())
        print(f"{env.now} -  Shipment {name} inspected")
    else:
        pass
    
def putaway(env, putaway_team, name):
    with putaway_team.request() as request:
        yield request
        yield env.timeout(generate_putaway())
    print(f"{env.now} -  Shipment {name} entered in stock")

def picking(env, picking_team, name):
    with picking_team.request() as request:
        yield request
        yield env.timeout(generate_picking())
    print(f"{env.now} -  Delivery {name} picked")

def packing(env, packing_team, name):
    with packing_team.request() as request:
        yield request
        yield env.timeout(generate_packing())
    print(f"{env.now} -  Delivery {name} packed")

def inspection_at_shipping(env, inspection_s_team, name):
    inspection_flag_r = np.random.randint(1, 10)
    if inspection_flag_r >= 6:
        print(f"{env.now} -  Delivery {name} : inspection required")
        with inspection_s_team.request() as request:
            yield request
            yield env.timeout(generate_insp_ship())
        print(f"{env.now} -  Delivery {name} inspected")
    else:
        pass

def shipping(env, shipping_team, name):
    with shipping_team.request() as request:
        yield request
        yield env.timeout(generate_shipping())
    print(f"{env.now} -  Delivery {name} shipped")

def generate_shipment_arrival():
    return np.random.uniform(1/8)

def generate_delivery_arrival():
    return np.random.uniform(4/8)

def generate_interactivity_time():
    return np.random.uniform(1/8, 4/8)

def generate_reception():
    return 1/8 #np.random.uniform(2, 6)

def generate_insp_recp():
    return 6/8

def generate_insp_ship():
    return 6/8

def generate_putaway():
    return 1/8

def generate_picking():
    return 1/8

def generate_packing():
    return 3/8

def generate_shipping():
    return 8/8


def convert_nb_to_time(x):
    """
        Generate a function to convert the simulated time to day and hours
    """
    day = int(x)
    hours = x % 1
    #day = x - hours

    hours = hours*100
    print(hours)
    hours = hours/24
    mins = (hours/24)/60
    
    
    

    #hours = hours*24
    #mins = hours % 1
    #hours = hours - mins
    #mins = mins*100
    print(hours)
    print(mins)
    t_date = f"Day {int(day+1)}, {int(hours)}:{int(mins)}"

    return t_date

def convert_time_to_nb():
    """
        Generate a function to convert the time to simulated time
    """
    pass


x = 1.4434353
print(x)
print(convert_nb_to_time(x))


env = simpy.Environment()
reception_team = simpy.Resource(env, capacity=2)
inspection_r_team = simpy.Resource(env, capacity=1)
putaway_team = simpy.Resource(env, capacity=1)
picking_team = simpy.Resource(env, capacity=2)
packing_team = simpy.Resource(env, capacity=1)
inspection_s_team = simpy.Resource(env, capacity=1)
shipping_team = simpy.Resource(env, capacity=1)
#spares = simpy.Container(env, init=20, capacity=20)
env.process(inbound_run(env, reception_team, inspection_r_team, putaway_team))
env.process(outbound_run(env, picking_team, packing_team, inspection_s_team, shipping_team))

env.run(until=8*5)


#class Warehouse():
#    def __init__(self, reception_team_capacity, ):
#        self.env = simpy.Environment()
#        self.reception_team = simpy.Resource



# Warehouse Process
#   Inbound
#       Transport reception
#            Random Event Managed
#       Reception
#            Resource Managed
#       Inspection
#            Resource Managed
#       Putaway
#            Resource Managed
#       Stock Management
#            Resource Managed

#   Outbound
#       Delivery Order
#            Random Event Managed
#       Picking
#            Resource Managed
#       Packing
#            Resource Managed
#       Inspection
#            Resource Managed
#       Shipping
#            Resource Managed
