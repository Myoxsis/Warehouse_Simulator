#!/usr/bin/env python
# coding: utf-8

import simpy, random, statistics
import numpy as np
import matplotlib.pyplot as plt

def warehouse_run(env, reception_team, inspection_team, putaway_team):
    global cost 

    cost = 0.0

    i = 0
    while True:
        # inbound process
        yield env.timeout(generate_shipment_arrival())
        print(f"{env.now} -  Shipment n°{i} inbound")
        env.process(goods_receipt(env, reception_team, i))
        env.process(inspection_at_reception(env, inspection_team, i))
        env.process(putaway(env, putaway_team, i))

        i += 1
    
def goods_receipt(env, reception_team, name):
    with reception_team.request() as request:
        yield request
        yield env.timeout(generate_reception())
    print(f"{env.now} -  Shipment {name} received")

def inspection_at_reception(env, inspection_team, name):
    inspection_flag = np.random.randint(1, 10)
    if inspection_flag >= 8:
        print(f"{env.now} -  Shipment {name} : inspection required")
        with inspection_team.request() as request:
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

def generate_shipment_arrival():
    return np.random.uniform(1/8)

def generate_reception():
    return 1 #np.random.uniform(2, 6)

def generate_insp_recp():
    return 1

def generate_putaway():
    return 1


def convert_nb_to_time():
    """
        Generate a function to convert the simulated time to day and hours
    """
    pass

def convert_nb_to_time():
    """
        Generate a function to convert the time to simulated time
    """
    pass


############

#def operate_machine(env, repairers, spares, name):
#    global cost

#    while True:
#        yield env.timeout(generate_time_to_failure())
#        t_broken = env.now
#        print(f"Machine {name} broke {t_broken}")
#        # Launch repair process
#        env.process(repair_machine(env, repairers, spares, name))
#        yield spares.get(1)
#        t_replaced = env.now
#        print(f"Machine {name} Replaced {t_replaced}")

#        cost = 20 * (t_replaced - t_broken)

#def repair_machine(env, repairers, spares, name):
#    with repairers.request() as request:
#        yield request
#        yield env.timeout(generate_repair_time())
#        yield spares.put(1)
#    print(f"Machine {name} repaired {env.now}")

#def generate_time_to_failure():
#    return np.random.uniform(132, 185)

#def generate_repair_time():
#    return np.random.uniform(4, 10) 


env = simpy.Environment()
reception_team = simpy.Resource(env, capacity=2)
inspection_team = simpy.Resource(env, capacity=1)
putaway_team = simpy.Resource(env, capacity=1)
#spares = simpy.Container(env, init=20, capacity=20)
env.process(warehouse_run(env, reception_team, inspection_team, putaway_team))

env.run(until=8)




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
