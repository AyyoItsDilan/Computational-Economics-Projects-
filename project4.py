#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this project, you will simulate the epidemic with origination-destination matrix
"""

import numpy as np  
import matplotlib.pyplot as plt

#=============================================================================
#Section 1. set the model parameters
#=============================================================================
#1.1 set the random seed to 380 (pseudo randomness)
np.random.seed(380) # DO NOT CHANGE THE SEED

#1.2 create a population vector with five areas, population in areas are:
# areaA: 18000. areaB: 22000, areaC:50100,areaD,21010, areaE:25000
n_j = np.array([18000,22000,50100,21010,25000])

#1.3 use the random integer generation function in numpy to create a 5 x 5
# Origination-Destination flow matrix
# Set the lower limit to 1000, upper limit to 3,000 
od_matrix = np.random.randint(1000, 3000, size=(5,5))


#1.4 same modal share across all regione (1)
alpha_vec = np.full(len(n_j),1) 
#1.5 same transmission rate across all regions
beta_vec = 0.8
#1.6 same recover rate  across all regions
gamma_vec = 0.05
#1.7 normal o-d flow
od_flow = np.round(od_matrix) * 1
#1.8 Have 300 iterations
days = 300



#=============================================================================
#Section 2. define the initial status table
#=============================================================================
# assume in the beginning, no recover or died yet, 
# infected proportion in areas are:
# areaA: 1%; areaB: 0.5%; areaC:0.1%; arerD:0%, areaE:0%

def start_detect(n_j,infect,immune):
    sir = np.zeros(shape=(5,3))
    sir[:,0] = n_j
    init_infect = np.round(sir[:, 0]*infect)
    init_immune = np.round(sir[:, 0]*immune)
    #move infections to group I and recovers to R 
    sir[:,0] = sir[:,0] - init_infect - init_immune 
    sir[:,1] = sir[:,1] + init_infect
    sir[:,2] = sir[:,2] + init_immune
    return sir

sir = start_detect(n_j, np.array([0.01, 0.005,0.001, 0, 0]), 0)


#=============================================================================
#Section 3. Define a function to simulate the epidemic in this big region
#=============================================================================
# function input should include:
# n_j:              population vector
# initial status:   the initial status of the epidemic
# od_flow:          the 5 x 5 o-d matrix
# alpha_vec:        population density in each region
# beta_vec:         transmission rate in each region
# gamma_vec:        daily recover rate in each region
# days: total       iterations

# function return:
# susceptible_pop_norm: changes in the proportion of S group (aggregated)
# infected_pop_norm: changes in the proportion of  I group (aggregated)
# recovered_pop_norm: changes in the proportion of R group (aggregated)

def epidemic_sim(n_j, initial_status,od_flow, 
                 alpha_vec,beta_vec,gamma_vec,days):
    """
    Parameters
    ----------
    n_j : 5 x1 array
        total population in each area.
    initial_status : 5 x 3 array
        initial status
    alpha : 5 x 1 array
        modal share in each area
    beta : 5 x 1 array
        transmission rate in each area
    fatality: 5 x 1 array 
        daily fatality rate in each area
    gamma : 5 x 1 array
        recover rage in each area
    days: int
        total iterations

    Returns
    -------
    infected_pop_norm : List
        DESCRIPTION.
    susceptible_pop_norm : List
        DESCRIPTION.
    recovered_pop_norm : List
        DESCRIPTION.

    """

    #3.1 make copy of the initial sir table
    sir_sim = sir.copy()

    #3.2 create empty list to keep tracking the changes
    susceptible_pop_norm = []
    infected_pop_norm = []
    recovered_pop_norm = []
    dead_pop_norm = []
    
    #3.3. use total_days as the interator
    total_days = np.linspace(1,days,days)
    for day in total_days:
        
        ##3.4 figure out where those infected people go
        
        # normalize the sir table by calculating the percentage of each group
        sir_percent = sir_sim / n_j[:,np.newaxis]
        # assuming the infected people travel to all ares with the same probability:  
        infected_mat = np.repeat(sir_percent[:, 1][:, None], 5, axis=1) 
        # od_infected gives the flow of infected people. i.e., where they go         
        od_infected =  infected_mat * od_flow  

        # "inflow infected" are those who will spread the disease to susceptible    
        inflow_infected =  od_infected.sum(axis=0) # total infected inflow in each area
        inflow_infected =  alpha_vec * inflow_infected # consider population density

        #3.5 calculate new_infect    
        new_infect = (sir_sim[:, 0] / n_j) * inflow_infected * beta_vec
 
        #3.6 set upper limit of the infected group (total susceptible)          
        new_infect =  np.maximum(0.0, np.minimum(new_infect, sir_sim[:, 0]))
    
        #3.7 calculate total number of people recovered        
        new_recovered = gamma_vec * sir_sim[:, 1]

    
        #3.8 remove new infections from susceptible group      
        sir_sim[:,0] =  sir_sim[:, 0] - new_infect

        #3.9 add new infections into infected group, 
        # also remove recovers from the infected group
        sir_sim[:,1] = sir_sim[:, 1] + new_infect - new_recovered


        #3.10 add recovers to the recover group       
        sir_sim[:,2] = sir_sim[:, 2] + new_recovered


        #3.11 set lower limits of the groups (0 people)        
        sir_sim = np.maximum(sir_sim, 0.0)

                 
        #3.12 compute the normalized SIR matrix on aggregate level
        region_sum = sir_sim.sum(axis=0) 
        region_sum_normalized = region_sum / n_j.sum()
        s = region_sum_normalized[0]
        i = region_sum_normalized[1]
        r = region_sum_normalized[2]

        susceptible_pop_norm.append(s)
        infected_pop_norm.append(i)
        recovered_pop_norm.append(r)
        
    return [susceptible_pop_norm, infected_pop_norm,recovered_pop_norm]





#3.13 call the function to simulate the epidemic
outcome = epidemic_sim(n_j, sir,od_flow, alpha_vec,beta_vec,gamma_vec,days)

#=============================================================================
#Section 4. define a function to visualize the simulation result
#=============================================================================
def sir_simulation_plot(outcome,days):
    S_series, I_series, R_series = outcome

    n = min(days, len(S_series), len(I_series), len(R_series))
    t = np.arange(1, n + 1)

    plt.figure(figsize=(10, 8))
    plt.plot(t, S_series[:n], label="S (proportion)")
    plt.plot(t, I_series[:n], label="I (proportion)")
    plt.plot(t, R_series[:n], label="R (proportion)")
    plt.xlabel("Day")
    plt.ylabel("Population proportion")
    plt.title("SIR Simulation (Aggregated)")
    plt.xlim(1, n)
    plt.ylim(0, 1)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

sir_simulation_plot(outcome,days=days)

#=============================================================================
#Section 5. Policy evaluation
#=============================================================================
# Using the simulation model to evaluate the following policy targets
# Visualize the results, organize the plots in a 2x2 figure, each outcome on 
# one subplot.
def policy(od_scale=1.0, beta_scale=1.0):
    od_scaled = od_flow * od_scale
    beta_scaled = beta_vec * beta_scale
    return epidemic_sim(n_j, sir, od_scaled, alpha_vec, beta_scaled, gamma_vec, days)

#Policy 1. do nothing (this should have been done in )
policy1 = policy(od_scale=1, beta_scale = 1.0)
#Policy 2. reduce the o-d flow by 50%, all other arguments stay unchanged
policy2 = policy(od_scale=0.5, beta_scale = 1.0)
#Policy 3. reduce the o-d flow by 80%, all other arguments stay unchanged 
policy3 = policy(od_scale=0.2, beta_scale=1.0)
#Policy 4. reduce the o-d flow by 80%, reduce beta by 50%, all other the same
policy4 = policy(od_scale=0.2, beta_scale=0.5)

fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=True)
fig.suptitle("Policy Evaluation", y=0.98)

def _plot_outcome(ax, outcome, title):
    S_series, I_series, R_series = outcome
    n = min(len(S_series), len(I_series), len(R_series), days)
    t = np.arange(1, n + 1)
    ax.plot(t, S_series[:n], label="S")
    ax.plot(t, I_series[:n], label="I")
    ax.plot(t, R_series[:n], label="R")
    ax.set_title(title, fontsize=11)
    ax.set_ylim(0, 1)
    ax.grid(alpha=0.3)

_plot_outcome(axes[0,0], policy1, "Policy 1: Baseline")
_plot_outcome(axes[0,1], policy2,     "Policy 2: OD −50%")
_plot_outcome(axes[1,0], policy3,     "Policy 3: OD −80%")
_plot_outcome(axes[1,1], policy4, "Policy 4: OD −80%, β −50%")

for ax in axes[1]:
    ax.set_xlabel("Day")
for ax in axes[:,0]:
    ax.set_ylabel("Proportion")

handles, labels = axes[0,0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", ncol=3, frameon=False)
plt.tight_layout(rect=[0, 0.05, 1, 0.97])
plt.show()

