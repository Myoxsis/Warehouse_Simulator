#%%

import simpy 
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

#%%

class Article():
    """ Article Master Data """
    def __init__(self, name, unit_cost, supply_lead_time, reorder_point, order_size):
        self.name = name
        self.unit_cost = unit_cost
        self.supply_lead_time = supply_lead_time
        self.reorder_point = reorder_point
        self.order_size = order_size
        self.allocated_warehouse = []

    def allocate_to_warehouse(self, warehouse):
        warehouse.article_list.append(self)
        self.allocated_warehouse.append(warehouse)

    def display_stocks(self):
        """ Display stocks of the allocated warehouse """
        lvl_lst = []
        for wrh in self.allocated_warehouse:
            wrh_name = wrh.name
            stock_lvl = wrh.inv_list[self.name].history[-1][-1]
            lvl_lst.append((str(wrh_name), stock_lvl))
        return lvl_lst
        

    
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
        """ Update holding and shortage cost at each inventory
         movement """
        if self.level <= 0 :
            self.shortage_cost += (abs(self.level) * self.SHORTAGE_COST_C * (env.now - self.last_change))
        else:
            self.holding_cost += (self.level * self.HOLDING_COST_C * (env.now - self.last_change))
        
    def generate_demand(self, env):
        """ Generate demand at random intervals (based on normal distribution) and update
         inventory level """
        while True:
            interarrivalTime = math.ceil(np.random.normal(3, 1))
            demandQty = math.ceil(np.random.normal(5, 4))
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
        """ Start the inventory processes for all the article allocated to
         the warehouse. """
        self.inv_list = {art.name: InventorySystem(env, self, art, 6) for art in self.article_list}

    def ABC_analysis(self):
        pass



# Runtime

env = simpy.Environment()

art1 = Article('Article A', 100, 5, 10, 5)
art2 = Article('Article B', 87, 14, 15, 5)

wh = Warehouse(env, 0.1, 'Wrh1')
wh1 = Warehouse(env, 0.1, 'Wrh2')

art1.allocate_to_warehouse(wh)
art2.allocate_to_warehouse(wh)

art1.allocate_to_warehouse(wh1)

wh.run(env)
wh1.run(env)

env.run(until=10)

#%%

for art in wh.article_list:
    print(art.name)

wh.inv_list

#%%

for art_nm in wh.inv_list.keys():
    print(wh.inv_list[art_nm].history[-1][-1])

#%%

art1.allocated_warehouse

#%%

art1.display_stocks()