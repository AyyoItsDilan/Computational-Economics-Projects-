"""

In this project, you will use Agent-based modeling to simulate 
people's cooperation decision and the consequence of social interactions. 
In particular. We will replicate the in-class experiment we did in class 

Very Briefly:

• In this experiment, we will play a “matching fund game”.
 Each of you start with X points as initial endowment.

• You can contribute any amount from 0 to X to a “fund pool”. 
I will double the total contributions to this fund.

• I will then divide the doubled amount equally among all the players 
regardless of their contribution.

"""


import numpy as np
import matplotlib.pyplot as plt

class Player:
    """Base class for all players in the public goods game"""
    
    def __init__(self, endowment):
        """
        TODO: Initialize a player with given endowment
        - Set the endowment attribute
        - Create an empty list to store contribution history
        """
        self.endowment = endowment
        self.contribution_history = []
        
        
    def self_introduction(self):
        """
        TODO: Print player information
        - Print the player's class name (type of player)
        - Print their endowment
        - Print a dividing line of dashes
        """
        print(f"Player type: {self.__class__.__name__}")
        print(f"Endowment: {self.endowment}")
    
    def contribute(self, last_round_avg=None):
        """
        TODO: Default contribution behavior - random contribution
        - Return a random contribution between 0 and endowment
        - Store the contribution in the history list
        Hint: Use np.random.uniform(0, self.endowment)
        """
        contribution = np.random.uniform(0, self.endowment)
        self.contribution_history.append(contribution)
        return contribution


class FreeRider(Player):
    """
    TODO: Create a FreeRider class that inherits from Player
    Free riders should contribute very little (between 0 and 10% of their endowment)
    """
    def contribute(self, last_round_avg=None):
        contribution = 0
        self.contribution_history.append(contribution)
        return contribution

class StrongCooperator(Player):
    """
    TODO: Create a StrongCooperator class that inherits from Player
    Strong cooperators should contribute a lot (between 90% and 100% of their endowment)
    """
    def contribute(self, last_round_avg=None):
        contribution = np.random.uniform(self.endowment*0.90, self.endowment)
        self.contribution_history.append(contribution)
        return contribution

class ConditionalCooperator(Player):
    """
    TODO: Create a ConditionalCooperator class that inherits from Player
    - In the first round (last_round_avg is None), contribute randomly like the parent class
    - In subsequent rounds, contribute 80% of the last round's average
    - Remember to store contributions in history
    """
    def contribute(self, last_round_avg=None):
        if last_round_avg is None:
            # First round — random like the parent
            contribution = np.random.uniform(0, self.endowment)
            self.contribution_history.append(contribution)
        else:
            # Later rounds — 80% of last round’s avg, capped at endowment
            contribution = 0.8 * last_round_avg
            contribution = min(contribution, self.endowment)
            self.contribution_history.append(contribution)
            
        return contribution

def run_game(players, n_rounds):
    """
    TODO: Implement the public goods game simulation
    For each round:
        1. Get last round's average (None in first round)
        2. Collect contributions from all players
        3. Calculate and store the average contribution
    Return the list of average contributions per round
    """
    average_contributions = []
    
    last_round_avg=None
    
    for n in range(n_rounds):
      
       contributions = [p.contribute(last_round_avg) for p in players]
       # Compute round average
       round_avg = np.mean(contributions)
       average_contributions.append(round_avg)

       # Update for next round
       last_round_avg = round_avg
    return average_contributions

def create_scenario(n_conditional, n_free_riders=0, n_strong=0, endowment=100):
    """
    TODO: Create a list of players for a scenario
    1. Create n_conditional ConditionalCooperator players
    2. Create n_free_riders FreeRider players
    3. Create n_strong StrongCooperator players
    Return the list of all players
    """
    players = []
    # Create Conditional Cooperators
    for i in range(n_conditional):
        players.append(ConditionalCooperator(endowment))

    # Create Free Riders
    for i in range(n_free_riders):
        players.append(FreeRider(endowment))

    # Create Strong Cooperators
    for i in range(n_strong):
        players.append(StrongCooperator(endowment))

    return players

def calculate_earnings(players, total_pool):
    """
    TODO: Calculate average earnings by player type
    For each player:
        1. Calculate their total contribution
        2. Calculate their share of the pool
        3. Calculate their earnings:
           earnings = (endowment * n_rounds) - total_contribution + share
    Return a dictionary of average earnings by player type
    """
    earnings = {}
    n_rounds = len(players[0].contribution_history)
    total_contributed = sum(sum(p.contribution_history) for p in players)
    
    for p in players:
        total_contribution = sum(p.contribution_history)
        share = (total_contribution / total_contributed) * total_pool
        earning = (p.endowment * n_rounds) - total_contribution + share
        ptype = p.__class__.__name__ 
        
        # store earnings by player type
        if ptype not in earnings:
           earnings[ptype] = []
        earnings[ptype].append(earning)

    for ptype in earnings:
        earnings[ptype] = np.mean(earnings[ptype])
        
    return earnings

# Main simulation code - DO NOT MODIFY
if __name__ == "__main__":
    np.random.seed(380)  # Set seed for reproducibility
    
    # Game parameters
    n_rounds = 20
    endowment = 100
    multiplier = 2  # Pool multiplier
    
    # Create and run three scenarios
    scenarios = {
        "All Conditional": create_scenario(30),
        "With Free Riders": create_scenario(25, n_free_riders=5),
        "With Strong Cooperators": create_scenario(25, n_strong=5)
    }
    
    # Run simulations and store results
    results = {}
    for name, players in scenarios.items():
        results[name] = run_game(players, n_rounds)
    
    # Plot results
    plt.figure(figsize=(10, 6))
    for name, contributions in results.items():
        plt.plot(contributions, label=name)
    
    plt.xlabel('Round')
    plt.ylabel('Average Contribution')
    plt.title('Average Contributions Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()
    