"""

Scenario :

1. Trucks arrive at a warehouse to offload goods. They request a quay to deliver.
2. Once the quay decided they go to the quay
3. At the quay, they will require a member of the quayside_team to offload the truck. 
4. Quayside_team will offload X pallets in 1 hours.
5. Once offloaded, the truck will leave the quay releasing it to be used by user trucks.
6. Reception_team member will take each 1 pallet, and take boxes one by one to do the reception, X% of boxes will go to quality inspection
7. Once finished with the pallet recepetion_team member will switch to another pallet.
8. Putaway_team will wait for 

"""



import simpy
import numpy as np



def display_time(env_time):
    env_time = float(env_time)
    integer_part, decimal_part = str(env_time).split('.')
    days = str(int(integer_part) // 24)
    hours = str(int(integer_part) % 24)
    minutes = str(int(decimal_part.ljust(10,'0')) // 6000000000).zfill(2)
    return "Day {} {}:{} ".format(days, hours, minutes)

class Truck:
    def __init__(self, id) -> None:
        self.id = np.random.randint(100000, 999999)
        self.name = f"Truck #{id}"
        self.nb_pallets = np.random.randint(1,34)
        self.nb_boxes_per_pallets = np.random.randint(1,12)

    
class Warehouse:
    def __init__(self, env, nb_quay, quayside_team_capacity) -> None:
        self.env = env
        self.quayside = simpy.Store(env, capacity=nb_quay)
        self.quayside_team = simpy.Resource(env, capacity=quayside_team_capacity)


        # Process
        self.truck_arrival_generation = env.process(self.generate_truck_arrival())

    # Function oto be created when a truck arrives at warehouse and request for an empty quay // generic resource request check pump station example in Simpy doc.

    def generate_truck_arrival(self):
        i = 0
        while True:
            truck = Truck(i)
            yield self.env.timeout(np.random.rand())
            print(f'[{display_time(env.now)}] {truck.name} arrived at Warehouse Parking')
            env.process(self.truck_to_quay(truck))
            i += 1

    def truck_to_quay(self, truck):
        with self.quayside.put(1) as request:
                print(f"{truck.name} going to quay")
                yield self.env.timeout(0.4)
                print(f"{truck.name} arrived at quay")
                env.process(self.truck_offloading(truck, request))
                print(f"{truck.name} leaving quay")
                
    
    def truck_offloading(self, truck, request):
        while True:
            with self.quayside_team.request() as request:
                yield request
                for pallet_x in range(0, truck.nb_pallets-1):
                    print(f"[{display_time(env.now)}] {truck.name} - Pallet #{pallet_x+1} [{truck.nb_boxes_per_pallets}] offloaded")
                    #self.quayside.put(truck.nb_boxes_per_pallets)
                    yield self.env.timeout(0.01)
            


env = simpy.Environment()
wrh = Warehouse(env, 1, 2)
env.run(until=24)



# Generate Trucks Arrival
# Truck offloading
# Reception
# Inspection at reception
# Putaway
# --------------------------
# Generate Line Feeding requirements
# Picking
# Packing
# Put to quayside
# Truck loading
# (delivery to final customer)

#
#import simpy, random, statistics
#import numpy as np
#import matplotlib.pyplot as plt
#
#def inbound_run(env, reception_team, inspection_r_team, putaway_team):
#    global cost 
#
#    cost = 0.0
#
#    i = 0
#    while True:
#        # inbound process
#        yield env.timeout(generate_shipment_arrival())
#        print(f"{env.now} -  Shipment n°{i} inbound")
#        env.process(goods_receipt(env, reception_team, i))
#        yield env.timeout(generate_interactivity_time())
#        env.process(inspection_at_reception(env, inspection_r_team, i))
#        yield env.timeout(generate_interactivity_time())
#        env.process(putaway(env, putaway_team, i))
#
#        i += 1
#
#def outbound_run(env, picking_team, packing_team, inspection_s_team, shipping_team):
#    i = 0
#    while True:
#        # inbound process
#        yield env.timeout(generate_delivery_arrival())
#        print(f"{env.now} -  Delivery n°{i} inbound")
#        env.process(picking(env, picking_team, i))
#        yield env.timeout(generate_interactivity_time())
#        env.process(packing(env, packing_team, i))
#        yield env.timeout(generate_interactivity_time())
#        env.process(inspection_at_shipping(env, inspection_s_team, i))
#        yield env.timeout(generate_interactivity_time())
#        env.process(shipping(env, shipping_team, i))
#        i += 1
#    
#def goods_receipt(env, reception_team, name):
#    with reception_team.request() as request:
#        yield request
#        yield env.timeout(generate_reception())
#    print(f"{env.now} -  Shipment {name} received")
#
#def inspection_at_reception(env, inspection_r_team, name):
#    inspection_flag = np.random.randint(1, 10)
#    if inspection_flag >= 8:
#        print(f"{env.now} -  Shipment {name} : inspection required")
#        with inspection_r_team.request() as request:
#            yield request
#            yield env.timeout(generate_insp_recp())
#        print(f"{env.now} -  Shipment {name} inspected")
#    else:
#        pass
#    
#def putaway(env, putaway_team, name):
#    with putaway_team.request() as request:
#        yield request
#        yield env.timeout(generate_putaway())
#    print(f"{env.now} -  Shipment {name} entered in stock")
#
#def picking(env, picking_team, name):
#    with picking_team.request() as request:
#        yield request
#        yield env.timeout(generate_picking())
#    print(f"{env.now} -  Delivery {name} picked")
#
#def packing(env, packing_team, name):
#    with packing_team.request() as request:
#        yield request
#        yield env.timeout(generate_packing())
#    print(f"{env.now} -  Delivery {name} packed")
#
#def inspection_at_shipping(env, inspection_s_team, name):
#    inspection_flag_r = np.random.randint(1, 10)
#    if inspection_flag_r >= 6:
#        print(f"{env.now} -  Delivery {name} : inspection required")
#        with inspection_s_team.request() as request:
#            yield request
#            yield env.timeout(generate_insp_ship())
#        print(f"{env.now} -  Delivery {name} inspected")
#    else:
#        pass
#
#def shipping(env, shipping_team, name):
#    with shipping_team.request() as request:
#        yield request
#        yield env.timeout(generate_shipping())
#    print(f"{env.now} -  Delivery {name} shipped")
#
#def generate_shipment_arrival():
#    return np.random.uniform(1/8)
#
#def generate_delivery_arrival():
#    return np.random.uniform(4/8)
#
#def generate_interactivity_time():
#    return np.random.uniform(1/8, 4/8)
#
#def generate_reception():
#    return 1/8 #np.random.uniform(2, 6)
#
#def generate_insp_recp():
#    return 6/8
#
#def generate_insp_ship():
#    return 6/8
#
#def generate_putaway():
#    return 1/8
#
#def generate_picking():
#    return 1/8
#
#def generate_packing():
#    return 3/8
#
#def generate_shipping():
#    return 8/8
#
#
#def convert_nb_to_time(x):
#    """
#        Generate a function to convert the simulated time to day and hours
#    """
#    day = int(x)
#    hours = x % 1
#    #day = x - hours
#
#    hours = hours*100
#    print(hours)
#    hours = hours/24
#    mins = (hours/24)/60
#    
#    
#    
#
#    #hours = hours*24
#    #mins = hours % 1
#    #hours = hours - mins
#    #mins = mins*100
#    print(hours)
#    print(mins)
#    t_date = f"Day {int(day+1)}, {int(hours)}:{int(mins)}"
#
#    return t_date
#
#def convert_time_to_nb():
#    """
#        Generate a function to convert the time to simulated time
#    """
#    pass
#
#
#x = 1.4434353
#print(x)
#print(convert_nb_to_time(x))
#
#
#env = simpy.Environment()
#reception_team = simpy.Resource(env, capacity=2)
#inspection_r_team = simpy.Resource(env, capacity=1)
#putaway_team = simpy.Resource(env, capacity=1)
#picking_team = simpy.Resource(env, capacity=2)
#packing_team = simpy.Resource(env, capacity=1)
#inspection_s_team = simpy.Resource(env, capacity=1)
#shipping_team = simpy.Resource(env, capacity=1)
##spares = simpy.Container(env, init=20, capacity=20)
#env.process(inbound_run(env, reception_team, inspection_r_team, putaway_team))
#env.process(outbound_run(env, picking_team, packing_team, inspection_s_team, shipping_team))
#
#env.run(until=8*5)
#
#
##class Warehouse():
##    def __init__(self, reception_team_capacity, ):
##        self.env = simpy.Environment()
##        self.reception_team = simpy.Resource
#
#
#
## Warehouse Process
##   Inbound
##       Transport reception
##            Random Event Managed
##       Reception
##            Resource Managed
##       Inspection
##            Resource Managed
##       Putaway
##            Resource Managed
##       Stock Management
##            Resource Managed
#
##   Outbound
##       Delivery Order
##            Random Event Managed
##       Picking
##            Resource Managed
##       Packing
##            Resource Managed
##       Inspection
##            Resource Managed
##       Shipping
##            Resource Managed