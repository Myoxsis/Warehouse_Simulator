#%%

import simpy 
import numpy as np
import pandas as pd

#%%

class Article(object):
    def __init__(self, name, lot_size, supply_time):
        self.name = name
        self.lot_size = lot_size
        self.supply_time = supply_time



class Warehouse(object):
    def __init__(self, env, name, reception_team_capacity, inspection_r_team_capacity, putaway_team_capacity, picking_team_capacity, packing_team_capacity, inspection_s_team_capacity, shipping_team_capacity):
        self.env = env
        self.name = name

        
        
        # Link team capacity to user input in UI
        self.inbound_team = simpy.Resource(env, capacity=inbound_team_capacity)
        self.outbound_team = simpy.Resource(env, capacity=outbound_team_capacity)
        self.stock_team = simpy.Resource(env, capacity=stock_team_capacity)

        # Starting Processes.
        self.inb_process = env.process(self.inbound_run(env, self.inbound_team))
        self.out_process = env.process(self.outbound_run(env, self.outbound_team))
        self.stock_process = env.process(self.stock_run(env, self.stock_team))
        
    def display_time(self, env):
        date_ = datetime.datetime.strptime('01/01/2022', "%d/%m/%Y") + datetime.timedelta(days=int(env.now / 8)) + datetime.timedelta(hours=env.now %8)
        return f"Date : {date_}"

    def collect_metrics(self, env):
        while True:
            self.df_logs.loc[len(self.df_logs)] = [datetime.datetime.strptime('01/01/2022', "%d/%m/%Y") + datetime.timedelta(days=int(env.now / 8)) + datetime.timedelta(hours=env.now %8), self.kpi_shipment_received, self.kpi_delivery_received, self.kpi_delivery_inspected_rcp, self.kpi_delivery_putaway, self.kpi_delivery_picked, self.kpi_delivery_packed, self.kpi_delivery_inspected_shp, self.kpi_delivery_shipped]
            yield env.timeout(.25)

    def log_delivery_metrics(self, env, name, event_name):
        self.df_dl_lg.loc[len(self.df_dl_lg)] = [datetime.datetime.strptime('01/01/2022', "%d/%m/%Y") + datetime.timedelta(days=int(env.now / 8)) + datetime.timedelta(hours=env.now %8), name, event_name ]

    def inbound_run(self, env, reception_team, inspection_r_team, putaway_team):
        shp_i = 0
        dl_in_count=0
        while True:
            # inbound process
            yield env.timeout(self.generate_shipment_arrival())
            #st.write(f"{self.display_time(env)} -  Shipment n°{shp_i} inbound")
            random_nb_delivery = np.random.randint(10, 50)
            self.kpi_shipment_received +=1
            for rd_dl in range(1,random_nb_delivery):
                env.process(self.goods_receipt(env, reception_team, f"I{shp_i}-{rd_dl}"))
                yield env.timeout(self.INTERACTIVITY_TIME)
                inspection_flag = np.random.randint(1, 5)
                if inspection_flag >= 3:
                    inspection_proc = env.process(self.inspection_at_reception(env, inspection_r_team, f"I{shp_i}-{rd_dl}"))
                    yield inspection_proc & env.timeout(self.INTERACTIVITY_TIME)
                else:
                    continue
                putaway_proc = env.process(self.putaway(env, putaway_team, f"I{shp_i}-{rd_dl}"))
                yield putaway_proc & env.timeout(self.INTERACTIVITY_TIME)
                dl_in_count+=1
            shp_i += 1
            
        
    def outbound_run(self, env, picking_team, packing_team, inspection_s_team, shipping_team):
        i = 0
        while True:
            # inbound process
            yield env.timeout(self.generate_delivery_arrival())
            #st.write(f"{self.display_time(env)} -  Delivery n°{i} inbound")
            env.process(self.picking(env, picking_team, f"O000-{i}"))
            yield env.timeout(self.INTERACTIVITY_TIME)
            env.process(self.packing(env, packing_team, f"O000-{i}"))
            yield env.timeout(self.INTERACTIVITY_TIME)
            inspection_flag = np.random.randint(1, 5)
            if inspection_flag >= 3:
                env.process(self.inspection_at_shipping(env, inspection_s_team, f"O000-{i}"))
                yield env.timeout(self.INTERACTIVITY_TIME)
            else:
                continue
            env.process(self.shipping(env, shipping_team, f"O000-{i}"))
            i += 1
        
    def goods_receipt(self, env, reception_team, name):
        with reception_team.request() as request:
            self.log_delivery_metrics(env, name, "goods_receipt_in")
            yield request
            yield env.timeout(self.RECEPTION_TIME)
            self.kpi_delivery_received +=1
            self.log_delivery_metrics(env, name, "goods_receipt_out")
        #st.write(f"{self.display_time(env)} -  Shipment {name} received")        

    def inspection_at_reception(self, env, inspection_r_team, name):
        #st.write(f"{self.display_time(env)} -  Shipment {name} : inspection required")
        with inspection_r_team.request() as request:
            self.log_delivery_metrics(env, name, "inspection_recp_in")
            yield request
            yield env.timeout(self.INSPECTION_RECP_TIME)
            self.kpi_delivery_inspected_rcp += 1
            self.log_delivery_metrics(env, name, "inspection_recp_out")
        
    def putaway(self, env, putaway_team, name):
        with putaway_team.request() as request:
            self.log_delivery_metrics(env, name, "putaway_in")
            yield request
            yield env.timeout(self.PUTAWAY_TIME)
            self.kpi_delivery_putaway +=1
            self.log_delivery_metrics(env, name, "putaway_out")
        #st.write(f"{self.display_time(env)} -  Shipment {name} entered in stock")

    def picking(self, env, picking_team, name):
        with picking_team.request() as request:
            self.log_delivery_metrics(env, name, "picking_in")
            yield request
            yield env.timeout(self.PICKING_TIME)
            self.kpi_delivery_picked += 1
            self.log_delivery_metrics(env, name, "picking_out")
        #st.write(f"{self.display_time(env)} -  Delivery {name} picked")

    def packing(self, env, packing_team, name):
        with packing_team.request() as request:
            self.log_delivery_metrics(env, name, "packing_in")
            yield request
            yield env.timeout(self.PACKING_TIME)
            self.kpi_delivery_packed += 1
            self.log_delivery_metrics(env, name, "packing_out")
        #st.write(f"{self.display_time(env)} -  Delivery {name} packed")

    def inspection_at_shipping(self, env, inspection_s_team, name):
        #st.write(f"{self.display_time(env)} -  Delivery {name} : inspection required")
        with inspection_s_team.request() as request:
            self.log_delivery_metrics(env, name, "inspection_shp_in")
            yield request
            yield env.timeout(self.INSPECTION_SHP_TIME)
            self.kpi_delivery_inspected_shp += 1
            self.log_delivery_metrics(env, name, "inspection_shp_out")
        #st.write(f"{self.display_time(env)} -  Delivery {name} inspected")

    def shipping(self, env, shipping_team, name):
        with shipping_team.request() as request:
            self.log_delivery_metrics(env, name, "shipping_in")
            yield request
            yield env.timeout(self.SHIPPING_TIME)
            self.kpi_delivery_shipped += 1
            self.log_delivery_metrics(env, name, "shipping_out")
        #st.write(f"{self.display_time(env)} -  Delivery {name} shipped")

    def generate_shipment_arrival(self):
        return np.random.uniform(.5/8)

    def generate_delivery_arrival(self):
        return np.random.uniform(.01/8)    

#%%


import simpy
import numpy as np
import matplotlib.pyplot as plt

def supply_run(env, order_cutoff, order_target):
    global inventory, balance, num_ordered

    inventory = order_target
    balance = 0.0
    num_ordered = 0

    while True:
        interarrival = np.random.exponential(1./5)
        yield env.timeout(interarrival)
        balance = inventory * 2 * interarrival
        demand = np.random.randint(1, 5)
        if demand < inventory:
            balance += 100*demand
            inventory -= demand
            print(f"{env.now} sold {demand}")
        else:
            balance += 100*inventory
            inventory = 0
            print(f"{env.now} sold {inventory} (out of stock)")


        if inventory < order_cutoff and num_ordered == 0:
            env.process(handle_order(env, order_target))

def handle_order(env, order_target):
    global inventory, balance, num_ordered

    num_ordered = order_target - inventory
    print(f"{env.now} placed order for {num_ordered}") 
    balance -= 50 * num_ordered
    yield env.timeout(2.0)
    inventory += num_ordered
    num_ordered = 0
    print(f"{env.now} received order,  {inventory} in inventory") 

df = pd.DataFrame({
    "obs_time" : [],
    "inventory_level" : []
})


def observe(env):
    global inventory
    while True:
        df.loc[len(df)] = [env.now, inventory]
        yield env.timeout(0.1)

np.random.seed(0)

env = simpy.Environment()
env.process(warehouse_run(env, 15, 80))
env.process(observe(env))
env.run(until=25.0)

plt.figure()
plt.step(df['obs_time'], df['inventory_level'], where='post')
plt.fill_between(df['obs_time'], df['inventory_level'], max(df['inventory_level']),  where=(df['inventory_level']==0), color='red', alpha=0.2)
plt.fill_between(df['obs_time'], df['inventory_level'], min(df['inventory_level']),  where=(df['inventory_level']!=0), color='green', alpha=0.2)
plt.xlabel('Simulation time (days')
plt.ylabel('Inventory Level')



#%%



class Inventory(object):
    def __init__(self, env, name, inventory, order_cutoff, order_target):
        self.env = env
        self.name = name
        self.inventory = inventory
        self.demand = np.random.randint(3, 8)
        self.balance = 0.0
        self.num_ordered = 0
        self.order_cutoff = order_cutoff
        self.order_target = order_target

        self.logs = pd.DataFrame({
            "obs_time" : [],
            "inventory_level" : [],
            "balance_level" : []
        })

        self.out_process = env.process(self.supply_run(env))
        self.monitoring = env.process(self.collect_metrics(env))

    def supply_run(self, env):
        while True:
            interarrival = np.random.exponential(1./5)
            yield env.timeout(interarrival)
            self.balance += self.inventory * 2 * interarrival
            
            if self.demand < self.inventory:
                self.balance += 100 * self.demand
                self.inventory -= self.demand
                #print(f"{env.now} sold {self.demand}")
            else:
                self.balance += 100 * self.inventory
                self.inventory = 0
                #print(f"{env.now} sold {self.inventory} (out of stock)")

            if self.inventory < self.order_cutoff and self.num_ordered == 0:
                env.process(self.handle_order(env))

    def handle_order(self, env):
        self.num_ordered = self.order_target - self.inventory
        #print(f"{env.now} placed order for {self.num_ordered}") 
        self.balance -= 50 * self.num_ordered
        yield env.timeout(2.0)
        self.inventory += self.num_ordered
        self.num_ordered = 0
        #print(f"{env.now} received order,  {self.inventory} in inventory") 


    def collect_metrics(self, env):
        while True:
            self.logs.loc[len(self.logs)] = [env.now, self.inventory, self.balance]
            yield env.timeout(0.1)

    def display_inventory_chart(self):
        plt.figure()
        plt.step(self.logs['obs_time'], self.logs['inventory_level'], where='post')
        plt.fill_between(self.logs['obs_time'], self.logs['inventory_level'], max(self.logs['inventory_level']),  where=(self.logs['inventory_level']==0), color='red', alpha=0.2)
        plt.fill_between(self.logs['obs_time'], self.logs['inventory_level'], min(self.logs['inventory_level']),  where=(self.logs['inventory_level']!=0), color='green', alpha=0.2)
        plt.xlabel('Simulation time (days')
        plt.ylabel('Inventory Level')
        plt.show()
    



hrd_runtime_input = 8
dys_runtime_input = 5

env = simpy.Environment()
wh = Inventory(env, "Wrh 1", 40, 15, 40)
wh1 = Inventory(env, "Wrh 1", 40, 10, 50)
wh2 = Inventory(env, "Wrh 1", 40, 10, 40)
env.run(until=10) #hrd_runtime_input*dys_runtime_input


wh.display_inventory_chart()
wh1.display_inventory_chart()
wh2.display_inventory_chart()

#print(wh.logs)


#%%

class Article():
    def __init__(self, name, unit_cost, supply_lead_time, reorder_point, order_size):
        self.name = name
        self.unit_cost = unit_cost
        self.supply_lead_time = supply_lead_time
        self.reorder_point = reorder_point
        self.order_size = order_size

    def allocate_to_warehouse(self, warehouse):




class Warehouse():
    def __init__(self, env, name, holding_rate, articles):
        self.env = env
        self.name = name
        self.holding_rate = holding_rate
        self.article_list = articles

    def runInventory(self, env):
        for art in self.article_list:
            print()


        for art in self.article_list:
            InventorySystem(art, 40, )

class InventorySystem():
    def __init__(self, env, article, start_inventory, reorder_point, order_size, inventory_level):
        self.env = env
        self.name = article.name
        self.start_inventory = start_inventory
        self.reorder_point = reorder_point
        self.order_size = order_size
        self.inventory_level = inventory_level
        self.ordering_cost = article.unit_cost
        self.history = [(0., inventory_level)]

        print(self.name)

        

env = simpy.Environment()

# Define Articles
art1 = Article('Ecrou', 10, 5, 10, 4)

# Define Warehouse

wh = Warehouse(env, "Wrh", 0.2, [art1])


env.run(until=10)


#%%

class Article():
    def __init__(self, name, unit_cost, supply_lead_time, reorder_point, order_size):
        self.name = name
        self.unit_cost = unit_cost
        self.supply_lead_time = supply_lead_time
        self.reorder_point = reorder_point
        self.order_size = order_size

    def allocate_to_warehouse(self, warehouse):
        warehouse.article_list.append(self)

    
class InventorySystem():
    def __init__(self, env, warehouse, article, start_level):
        self.env = env
        # Settings 
        self.NAME_C = article.name
        self.ORDER_SIZE_C = article.order_size
        self.REORDER_POINT_C = article.reorder_point
        self.ORDERING_COST_C = article.unit_cost * 0.2
        self.HOLDING_COST_C = article.unit_cost * warehouse.holding_rate
        self.SHORTAGE_COST_C = article.unit_cost * 0.5

        # Metrics variables
        self.level = start_level
        self.last_change = 0.
        self.shortage_cost = 0.
        self.holding_cost = 0.
        self.ordering_cost = 0.
        self.history = [(0., self.level)]

        # Other variables
        self.supply_lead_time = article.supply_lead_time

        #Declare Processes
        env.process(self.review_inventory(env))
        env.process(self.generate_demand(env))

    def review_inventory(self, env):
        while True:
            if self.level <= self.REORDER_POINT_C:
                ordered_quantity = (self.ORDER_SIZE_C + self.REORDER_POINT_C - self.level)
                env.process(self.manage_orders(env, ordered_quantity))
            yield env.timeout(1.)

    def manage_orders(self, env, ordered_quantity):
        self.ordering_cost += self.ORDERING_COST_C * ordered_quantity # try to add fix vs variable cost
        lead_time = np.random.normal(self.supply_lead_time, 1)
        yield env.timeout(lead_time)
        self.update_cost(env)
        self.level += ordered_quantity
        self.last_change = env.now
        self.history.append((env.now, self.level))

    def update_cost(self, env):
        if self.level <= 0 :
            self.shortage_cost += (abs(self.level) * self.SHORTAGE_COST_C * (env.now - self.last_change))
        else:
            self.holding_cost += (self.level * self.HOLDING_COST_C * (env.now - self.last_change))
        
    def generate_demand(self, env):
        while True:
            interarrivalTime = np.random.normal(3, 1)
            demandQty = np.random.normal(5, 4)
            yield env.timeout(interarrivalTime)
            self.update_cost(env)
            self.level -= demandQty
            self.last_change = env.now
            self.history.append((env.now, self.level))

class Warehouse():
    def __init__(self, env, holding_rate, name):
        self.env = env
        self.name = name
        self.holding_rate = holding_rate
        self.article_list = []

    def run(self, env):
        """
            Start the inventory processes for all the article allocated to the warehouse.

        """
        self.inv_list = {art.name: InventorySystem(env, self, art, 6) for art in self.article_list}

    def ABC_analysis(self):
        pass





env = simpy.Environment()

art1 = Article('Article A', 100, 5, 10, 5)
art2 = Article('Article B', 87, 14, 15, 5)

wh = Warehouse(env, 0.1, 'Wrh1')


art1.allocate_to_warehouse(wh)
art2.allocate_to_warehouse(wh)

wh.run(env)

env.run(until=10)

#%%

for art in wh.article_list:
    print(art.name)

wh.inv_list

#%%

wh.inv_list['Article A'].history

#%%

