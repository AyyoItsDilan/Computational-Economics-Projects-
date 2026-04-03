
"""
Project 5. In this project, you will apply Object Oriented Programming to
simulate the market demand/supply model.

"""
import numpy as np
import matplotlib.pyplot as plt
import math

np.random.seed(380)
#=============================================================================
# Section 1. Define classes
#=============================================================================
# 1.1. define a class Econ_agent
# attributes: id_number, budget
# methods: introduce_me(self):
# print out agent's id number and budget in sentences.


class Econ_agent:

    def __init__(self, id_number, budget):
        self.id_number = id_number
        self.budget = budget

    def introduce_me(self):
        print(f'This agents has ID Number:{self.id_number} and budget:{self.budget}')


# 1.2 define  "Consumer" as a child class of Econ_agent;
# 1.2.1 the Consumer class inherits all attributes and methods from Econ_agent;
# 1.2.2 additional attributes:
    # (1) 'preference', indicates how much the consumer like the product
    # 0 means does not like at all, 1 means wiling to spend whole budget on it

    # (2). wtp (i.e.,willingness to pay).
    # the wtp is the product of budget and preference

# 1.2.3 additional methods:
    # buying(self,price)
    # the buying method defines the consumer's purchasing decision
    # it takes two parameter, the first one is self, the second one is 'price'
    # when wtp is smaller than price, the consumer won't buy;
    # when wtp is greater or equal to price, the consumer will buy the product.
    # depending on budget, each customer may purchase no more than 5 units.
    # the buying method returns if the consumer decide to buy.


class Consumer(Econ_agent):

    def __init__(self, id_number, budget, preference):
        super().__init__(id_number, budget)
        self.preference = preference
        self.wtp = self.budget * self.preference

    def buying(self, price):
        buy = 0
        if self.wtp >= price:
            buy = self.budget/price
            return min(int(buy), 5)
        else:
            return 0



# 1.3 define "Producer" as a child class of Econ_agent;
# 1.3.1 the Producer class inherits all attributes and methods from Econ_agent;
# 1.3.2 additional attributes:
    # 1. 'opp_cost', indicate the opp_cost of producing and selling one unit
    # assume opp_cost is a constant for each producer.
# 1.3.3. additional methods:
    # selling(self,price)
    # the selling method defines the producer's decision
    # it takes two parameter, the first one is self, the second one is 'price'
    #when opp_cost is greater than price, the producer won't produce
    # when opp_cost or equal to price, the consumer will produce
    # the quantity supplied depends on the ratio between the producer's budget
    # and the the opp_cost. i.e., quantity supplied = budget/opp_cost
    # the method returns total amount a producer made.


class Producer(Econ_agent):
    
    def __init__(self, id_number, budget, opp_cost):
        super().__init__(id_number, budget)
        self.opp_cost = opp_cost
        
    def selling(self, price):
        if self.opp_cost > price:
            return 0
        quantity_supplied = int(self.budget / self.opp_cost)
        return quantity_supplied
            


#=============================================================================
# Section2. generate objects
#=============================================================================
# 2.1 generate a list of 200 consumer
# each has a unique id number
# budget is determined by a random draw from a normal distribution
#   set the normal distribution mean = 500, s.d. = 100
# preference is determined by a random draw from a uniform distribution [0,1]
consumers = []
for i in range(200):
    budget = np.random.normal(loc=500, scale=100)
    preference = np.random.uniform(0, 1)
    consumers.append(Consumer(id_number=i, budget=budget, preference=preference))
    

#2.2 generate a list of 50 producers
# each has a unique id number
# budget is determined by a random draw from a UNIFORM distribution [1000,8000]
# opp_cost is determined by  a drandom draw from uniform distribution [100,200]
producers = []
for i in range(50):
    budget = np.random.uniform(1000,8000)
    opp_cost = np.random.uniform(100,200)
    producers.append(Producer(id_number=i, budget=budget, opp_cost = opp_cost))
#=============================================================================
# Section 3. Simulate the market mechanism, and find the equilibrium
#=============================================================================

# Specifically, find the market equilibrium price and quantity (i.e., you
# may not be able to find a point where  Q = S exactly. Let's consider the
# market is in equilibrium as long as the difference between D and S is smaller
# than 5 units)

# Hint: you will need to think the process through before coding.
def total_demand(consumers, price):
    return sum(c.buying(price) for c in consumers)

def total_supply(producers, price):
    return sum(p.selling(price) for p in producers)

price = 100

td = total_demand(consumers, price)
ts = total_supply(producers, price)
    
while abs(td - ts) > 5 and 100 <= price <= 200:
    if td > ts:
     
        if price == 200:
        
            break
        price = min(200, price + 1)
    else:
       
        if price == 100:
          
            break
        price = max(100, price - 1)

    new_td = total_demand(consumers, price)
    new_ts = total_supply(producers, price)

    if new_td == td and new_ts == ts:
        break

    td, ts = new_td, new_ts

print(f"Equilibrium price = {price}, Demand={td}, Supply={ts}, |D-S|={abs(td - ts)}")

#=============================================================================
# Section4. Define the demand curve and supply curve
#=============================================================================
# 4.1. Define the demand curve when price ranging from 100 to 200
def demand():
    prices = list(range(100, 201))
    quantities = [total_demand(consumers, p) for p in prices]
    return prices, quantities

# 4.2. Define the supply curve when price ranging from 100 to 200
def supply():
    prices = list(range(100, 201))
    quantities = [total_supply(producers, p) for p in prices]  
    return prices, quantities


# 4.3 visualize the demand and supply, see if it makes sense.
pD, qD = demand()
pS, qS = supply()

gaps = [abs(d - s) for d, s in zip(qD, qS)]
idx_star = gaps.index(min(gaps))
p_star = pD[idx_star]

plt.figure(figsize=(8,5))
plt.plot(pD, qD, label="Demand")
plt.plot(pS, qS, label="Supply")
plt.axvline(p_star, linestyle="--", label=f"≈ p* {p_star} (|D−S|={gaps[idx_star]})")
plt.xlabel("Price"); plt.ylabel("Quantity")
plt.title("Market Demand & Supply (Price 100–200)")
plt.legend(); plt.tight_layout(); plt.show()

#=============================================================================
# Section 5. Changes in supply
#=============================================================================
# imagine there is a technology improvement, reduce the average opp_cost by 5%
# run a simulation to find the new market equilibrium
# visualize the change graphically
# Save the original equilibrium from Section 3
p_eq_old = price
D_old = td
S_old = ts

# Helper to find equilibrium for any (consumers, producers) set
def find_equilibrium(consumers, producers, p0=100):
    price = p0
    td = total_demand(consumers, price)
    ts = total_supply(producers, price)

    while abs(td - ts) > 5 and 100 <= price <= 200:
        if td > ts:
            if price == 200:  # stuck at upper bound
                break
            price = min(200, price + 1)
        else:
            if price == 100:  # stuck at lower bound
                break
            price = max(100, price - 1)

        new_td = total_demand(consumers, price)
        new_ts = total_supply(producers, price)

        # plateau guard
        if new_td == td and new_ts == ts:
            break

        td, ts = new_td, new_ts

    return price, td, ts

# --- Apply technology improvement: reduce opp_cost by 5% (i.e., *0.95) ---
producers_tech = [
    Producer(id_number=p.id_number, budget=p.budget, opp_cost=p.opp_cost * 0.95)
    for p in producers
]

# New equilibrium
p_eq_new, D_new, S_new = find_equilibrium(consumers, producers_tech, p0=p_eq_old)

print(f"[Old]  p*={p_eq_old}, D={D_old}, S={S_old}, |D-S|={abs(D_old - S_old)}")
print(f"[New]  p*={p_eq_new}, D={D_new}, S={S_new}, |D-S|={abs(D_new - S_new)}")

# --- Curves before/after (supply shifts right) ---
# Demand curve unchanged
pD, qD = demand()

# Old supply curve
prices = list(range(100, 201))
qS_old = [total_supply(producers, p) for p in prices]

# New supply curve (after tech improvement)
qS_new = [total_supply(producers_tech, p) for p in prices]

# Plot
plt.figure(figsize=(9,6))
plt.plot(pD, qD, label="Demand", linewidth=2)
plt.plot(prices, qS_old, label="Supply (old)", linewidth=2)
plt.plot(prices, qS_new, label="Supply (new, tech ↓ opp_cost 5%)", linewidth=2)
plt.axvline(p_eq_old, linestyle="--", label=f"old p* ≈ {p_eq_old}")
plt.axvline(p_eq_new, linestyle="--", label=f"new p* ≈ {p_eq_new}")
plt.xlabel("Price")
plt.ylabel("Quantity")
plt.title("Supply Shift from Technology Improvement (−5% opp_cost)")
plt.legend()
plt.tight_layout()
plt.show()


#=============================================================================
# Section 6 (optional). Estimate the demand and supply function
# Estimate the demand function and supply function you simulated in Section 4,
# and then use the two function to figure out the market equilibrium,
# see if the calculated equilibrium coincide with the simulation result.
#=============================================================================
