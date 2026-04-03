#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project 7. optimization and consumer theory

In this project, you will be practicing on root finding and optimization problems
In addition, you will apply the computational method to solve the utility
maximization problem in economics.
"""
import numpy as np

import matplotlib.pyplot as plt
from scipy.optimize import root
from scipy.optimize import minimize

#=============================================================================
# Section 1. Root finding and optimization
#=============================================================================
# 1.1. define the function y = ln(x) + (x-6)^3 - 4x + 30
# you can find the printed equation on Canvas
def f(x):
    return np.log(x) + (x-6)**3 - 4*x + 30


# 1.2. plot the function on the domain [1, 12]
x = np.linspace(1, 12, 100)
y = f(x)

def plot_function(x, y, title="Function"):
    fig = plt.figure()
    ax = fig.add_subplot(1 ,1, 1)
    ax.plot(x, y, color='blue')
    ax.set_title(title)
    ax.hlines(0, -2, 2, linestyle='--', color='r')  # highlight the horizontal line y = 0
    plt.show()
    
plot_function(x,y, title="np.log(x) + (x-6)**3 - 4*x + 30")
    


# 1.3. derive and define the first-order derivative of the function
def fp(x):
    return 1/x + 3*(x-6)**2 - 4

# 1.4. plot it on the domain [1, 12]
z = fp(x)

plot_function(x, z, title="1/x + 3*(x-6)**2 - 4")


# 1.5. Define the Newton-Raphson algorithm (as a function)
def newton_raphson(f,fp, initial_guess, tolerance=1e-9 , max_iteration=100):
    """
    This function will apply the Newton-Raphson method to find the root of a given function
    Parameters:
    ------------
    f : function
       The original function we wanted to find roots
    fp : function
        The first order derivative of the original function
    initial_guess: list
        A list of starting points.
    tolerance : float, optional
        defines how close to zero needs to be
    max_iteration : int
        defines maximum iterations if not converge
    Return:
    roots : list
        a list of roots found
    """
    roots = [ ]
    for x0 in initial_guess:
        x = x0
        fx = f(x)
        fpx = fp(x)
        iteration = 0
        # continue the iteration until stopping conditions are met
        while (abs(f(x)) > tolerance) and (iteration < max_iteration):
            x = x - fx/fpx
            fx = f(x)
            fpx = fp(x)
            iteration += 1
    
        if abs(f(x)) < tolerance:
            roots.append(np.round(x,3))

    return roots


# 1.6.Use the Newton-Raphson algorithm you defined to find the root of the function
# store the result in a list named as res_1

res_1 = newton_raphson(f, fp, initial_guess = [12, 10, 8])



# 1.7. use the Newton-Raphson method to find the
# maximum value on the domain [4, 8], name the returned variable as res_2
def fpp(x):
    return -1/x**2 + 6*(x - 6)

max_val = -np.inf
min_val = np.inf

temp1 = newton_raphson(fp, fpp, initial_guess = [4,5,6,7,8])
temp1 = [x for x in temp1 if 4 <= x <= 8]

for x in temp1:
    if fpp(x) < 0: 
        max_val = max(max_val, f(x))
    elif fpp(x) > 0: 
        min_val = min(min_val, f(x))
        
max_val = max(max_val, f(4), f(8))
min_val = min(min_val, f(4), f(8))
        

res_2 = max_val

# 1.8. use the Newton-Raphson method to find the
# minimum value on the domain [4, 8], name the returned variable as res_3
res_3 = min_val

# 1.9. use the scipy.optimize library to
# (a). find the root of f(x), store the result in variable res_4
res_4 = root(f, 4)
print(res_4)


# (b). find miniumn value of f(x) on the domain [4, 8],
# name the returned var as res_5
res_5 = minimize(f,4)

# (3). find maximum value of f(x) on the domain [4, 8],
# name the returned var as res_6
def neg_f(x):
    return -f(x)
res_6 = minimize(neg_f, 4)



#=============================================================================
# Section 2. Utiliyt Theory and the Application of Optimization
#=============================================================================

# Consider a utility function over bundles of A (apple) and B (banana)
#  U(B, A) =( B^alpha) * (A^(1-alpha))
# hint: you can find the printed equation on Canvas: project 7.

# 2.1. Define the given utility function
def utility(A, B, alpha):
    return B**alpha*A**(1-alpha)


# 2.2. Set the parameter alpha = 1/3,
# Assume the consumer always consume 1.5 units of B.
# plot the relationship between A (x-axis) and total utility (y-axis)
# set the range of A between 1 and 10
A = np.linspace(1, 10, 100)
B = 1.5
alpha = 1/3
U = utility(A,B,alpha)



def plot_utility(A, u_level):
    plt.figure()
    plt.plot(A, u_level, color='red')
    plt.title("Utility vs Apples")
    plt.xlabel("Quantity of Apples")
    plt.ylabel("Utility")
    plt.grid(True)
    plt.show()
    
plot_utility(A, U)


# 2.3.  plot the 3-dimensional utility function
# 3-d view of utility
A = np.linspace(1, 10, 100)
B = np.linspace(1, 10, 100)
A, B =  np.meshgrid(A, B)
u_level = utility(A, B, 1/3)


def plot_utility_3d(A, B, u_level):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(A, B, u_level, cmap='viridis', edgecolor='none')
    ax.set_xlabel("Apples (A)")
    ax.set_ylabel("Bananas (B)")
    ax.set_zlabel("Utility Level (U)")
    plt.show()

plot_utility_3d(A, B, u_level)



# 2.4.plot the utility curve on a "flatten view"
A = np.linspace(1, 10, 100)
B = np.linspace(1, 10 ,100)
A, B =  np.meshgrid(A, B)
u_level = utility(A, B, 1/3)

def plot_utility_flat(A, B, u_level):
    plt.figure()
    CS = plt.contour(A, B, u_level, levels=20, cmap='viridis')
    plt.clabel(CS, inline=True, fontsize=8)
    plt.title("Flattened Utility Map (Indifference Curves)")
    plt.xlabel("Apples (A)")
    plt.ylabel("Bananas (B)")
    plt.grid(True)
    plt.show()

plot_utility_flat(A, B, u_level)


# 2.5. from the given utitlity function, derive A as a function of B, alpha, and U
# plot the indifferences curves for u=1 ,3,5,7,9 on the same figure.
# Put B on the x-axis, and A on the y-axis
def A_indifference(B, ubar, alpha=1/3):
    return (ubar / (B**alpha))**(1 / (1 - alpha))


def plot_indifference_curves(ax, alpha=1/3):
    B = np.linspace(0.5, 10, 400) 
    U_levels = [1, 3, 5, 7, 9]
    for ubar in U_levels:
        A = A_indifference(B, ubar, alpha)
        ax.plot(B, A, label=f'U = {ubar}')
    ax.set_xlabel("Bananas (B)")
    ax.set_ylabel("Apples (A)")
    ax.set_title("Indifference Curves")
    ax.legend()
    plt.show()


fig, ax = plt.subplots()
plot_indifference_curves(ax)


# 2.6.suppose pa = 2, pb = 1, Income W = 20,
# Add the budget constraint to the  previous figure
def A_bc(B, W, pa, pb):
    return (W - pb * B) / pa


def plot_budget_constraint(ax, W, pa, pb):
    B = np.linspace(0, W/pb, 200)
    A = A_bc(B, W, pa, pb)
    ax.plot(B, A, color='black', linewidth=2, label="Budget Constraint")
    ax.set_xlim(0, W/pb)
    ax.set_ylim(0, W/pa)
    ax.legend()
    plt.show()
    
bc = A_bc(1.5, 20, 2, 1)
fig, ax = plt.subplots()
plot_budget_constraint(ax, 20, 2, 1)

# 2.7. find the optimized consumption bundle and maximized utility
def objective(B, W=20, pa=2, pb=1):
    A = (W - pb * B) / pa
    U = utility(A, B, alpha)
    return -U 

res_8 = minimize(objective, 5)
optimal_B = res_8.x[0]
optimal_A = (20 - 1 * optimal_B) / 2
optimal_U = utility(optimal_A, optimal_B, 1/3)