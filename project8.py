"""
project 7. the Solow-Swan growth model
"""
# Section 1. Preparation. Import the necessary libraries
import matplotlib.pyplot as plt
import numpy as np
import copy


# Section 2. Define the Growth model as a class

# ==================
# attributes:
# -a: factor productivity
# -s
# -alpha
# -delta
# -n

# -k
# -K
# -y
# -Y
# -i
# -I
# -L
# -d
# -be
# -steady_state


# methods:
# check_model: print the attribute of the instance
# grwoth: take one argument "year", and drive the economic growth
# get parameters: get the model parameters
# get states: get the states variables
# plot_growth: visualize how the income per capita, investment per capita, and
# plot_income_growth
# find_steady_state: solve for the steady state in this model

# arguments:
# ----------------------------------------------------------------------------
# para_dict:
# ----------------------------------------------------------------------------#\
# state_dict



class Growth_Model:
    """
    This class will create an instance of the Solow-Swan growth model

    arguments:
    ------------------
    para_dict: dict
        a dictionary of parameters
    state_dict: dict
        a dictionary of model state

    attributes
    --------------

    methods:
    -------------

    """

    def __init__(self,
                 para_dict={'n': np.array([0.002]),
                            's': np.array([0.15]),
                            'alpha': np.array([1/3]),
                            'delta': np.array([0.05]),
                            'a': np.array([1])},
                 state_dict={
                             'k': np.array([0.1]),
                             'L':([100])},
                 ):

        # read-in the given parameters and variables
        self.para_dict  = para_dict
        self.state_dict = state_dict
        # calculate lower case y
        self.state_dict['y'] = self.para_dict['a'] * (self.state_dict['k'] ** self.para_dict['alpha'])
        # calculate upper case K (i.e., aggregate capital)
        self.state_dict['K'] = self.state_dict['k'] * self.state_dict['L']
        self.state_dict['Y'] = (
        self.para_dict['a']
        * (self.state_dict['K'] ** self.para_dict['alpha'])
        * (self.state_dict['L'] ** (1 - self.para_dict['alpha']))
        )
    
        self.state_dict['d'] = self.para_dict['delta'] * self.state_dict['k']
        self.state_dict['i'] = self.para_dict['s'] * self.state_dict['y']
        self.state_dict['I'] = self.state_dict['i'] * self.state_dict['L']

        self.steady_state = {}

        self.init_param = copy.deepcopy(para_dict)
        self.init_state = copy.deepcopy(state_dict)


    def get_param(self):
        return self.para_dict

    def get_state(self):
        return self.state_dict


    def growth(self, years):
        # reset to initial status
        self.para_dict = self.init_param.copy()
        self.state_dict = self.init_state.copy()

        # step 1. define the time line
        time_lines= np.linspace(0, years, num=years+1, dtype=int)

        # step 2. examine growth
        for t in time_lines:

            # 2.1. load parameters
            n = self.para_dict.get('n')[0]
            s = self.para_dict.get('s')[0]
            alpha = self.para_dict.get('alpha')[0]
            delta = self.para_dict.get('delta')[0]
            a = self.para_dict.get('a')[0]

            # 2.2. load all current states
            y_t = self.state_dict.get('y')
            k_t = self.state_dict.get('k')
            Y_t = self.state_dict.get('Y')
            L_t = self.state_dict.get('L')
            K_t = self.state_dict.get('K')
            i_t = self.state_dict.get('i')
            I_t = self.state_dict.get('I')
            d_t = self.state_dict.get('d')
            
            #current states 
            k_curr = k_t[-1]
            L_curr = L_t[-1]

            # 2.3 calculate new states i.e., the dynamic
            dk = s * (a * (k_curr ** alpha)) - (delta + n) * k_curr
            k_next = k_curr + dk
            L_next = (1 + n) * L_curr
            d_next = delta * k_next
            y_next = a * (k_next ** alpha)
            K_next = k_next * L_next
            Y_next = a * (k_next ** alpha) * (L_next ** (1 - alpha))
            i_next = s * y_next
            I_next = i_next * L_next

            # 2.4. update the state_dict
            self.state_dict['k'] = np.append(k_t, k_next)
            self.state_dict['y'] = np.append(y_t, y_next)
            self.state_dict['Y'] = np.append(Y_t, Y_next)
            self.state_dict['K'] = np.append(K_t, K_next)
            self.state_dict['L'] = np.append(L_t, L_next)
            self.state_dict['i'] = np.append(i_t, i_next)
            self.state_dict['I'] = np.append(I_t, I_next)
            self.state_dict['d'] = np.append(d_t, d_next)

    def find_steady_state(self):
        # step 1. load paramters
        n = self.para_dict.get('n')[0]
        s = self.para_dict.get('s')[0]
        alpha = self.para_dict.get('alpha')[0]
        delta = self.para_dict.get('delta')[0]
        a = self.para_dict.get('a')[0]
        
        # step 2. find the steady state
        k_t = np.linspace(1e-4, 20, 100) # create the k_t domain

        break_even = (n + delta)*k_t # calculate the break_even investment
        # calculate the break_even investment per capita
        be_per_capita = (n + delta) * k_t
        # calculate the investment per capita
        i_t = s * (a * (k_t ** alpha))
        # compare i_t and the break_even invest.
        compare = np.abs(i_t - break_even) 
        # find the "turning point"
        steady = np.argmin(compare)
        y_t = a * (k_t ** alpha)
        c_t = y_t - i_t

        # store the results
        y_star = y_t[steady]
        i_star = i_t[steady]
        c_star = c_t[steady]
        k_star = k_t[steady]

        steady_state = {}
        steady_state["k_star"] = k_star
        steady_state["y_star"] = y_star
        steady_state["c_star"] = c_star
        steady_state["i_star"] = i_star

        self.steady_state = steady_state
        
        return [y_star, i_star, c_star, k_star]

    def plot_income_growth(self, ax=None):
        # plot income growth over time
        if ax is None:
            fig, ax = plt.subplots(figsize=(6, 4))
        Y = self.state_dict.get('Y')
        ax.plot(np.arange(len(Y)), Y, linewidth=2)
        ax.set_title('Aggregate Income Growth over Time')
        ax.set_xlabel('Time (years)')
        ax.set_ylabel('Aggregate Income (Y)')
        ax.grid(True)
        plt.tight_layout()
        plt.show()
        return ax

    def plot_growth(self, ax=None):
        # plot_growth(): visualize the relationship between
        #    income per capita, investment per capita, and capital accumulate.
        # (i.e., income per capita & investment per capita against capital )

        if ax is None:
            fig, ax = plt.subplots(figsize=(6, 4))

        k = self.state_dict.get('k')
        y = self.state_dict.get('y')
        i = self.state_dict.get('i')

        ax.plot(k, y, label='Output per Worker (y = A·k^α)', linewidth=2)
        ax.plot(k, i, label='Investment per Worker (i = s·y)', linewidth=2, linestyle='--')

        # break-even investment line
        n = self.para_dict.get('n')[0]
        delta = self.para_dict.get('delta')[0]
        break_even = (n + delta) * k
        ax.plot(k, break_even, label='Break-even Investment ((n+δ)·k)', color='red', linestyle=':')
        
        ax.set_title('Solow Growth Model: y(k), i(k), and Break-even')
        ax.set_xlabel('Capital per Worker (k)')
        ax.set_ylabel('Output / Investment per Worker')
        ax.legend()
        ax.grid(True)
        plt.tight_layout()
        plt.show()
        return ax


# Section 3. Specify model parameters and examine economic grwoth
# set parameters (exgoneousely given):
parameters = {'n': np.array([0.002]),                 # population growth rate
              's': np.array([0.15]),                  # saving rate
              'alpha': np.array([1/3]),               # share of capital
              'delta': np.array([0.05]),              # depreciation rate
              'a': np.array([1])                      # technology
              }

states = {              # factor productivity
          'k': np.array([1]),
          'L': np.array([100])}


# instantiate a growth model
model = Growth_Model(para_dict=parameters, state_dict=states)


# simulate the growth
model.growth(100)

# 3.2  visualize the growth by

#   (a). plotting income per worker (y), investment per worker (i),
#   and break-even investment against capital per worker (k).
model.plot_income_growth()

#    (b) plotting aggregate income (Y) against time.
model.plot_growth()


# 3.3  find the steady state of the model
ss = model.find_steady_state()
print(f'Steady States for y, i, c, and k are {ss}')


# Section 4. Use the growth model class to perform "what-if" analysis.
# see canvas for detailed requirements
#4-1. Holding all other factors the same as 3-1, what would happen to the steady state consumption (c*) if the saving rate is 33%?
model2 = Growth_Model(para_dict=parameters, state_dict=states)
model2.para_dict['s'] = np.array([0.33])
ss_33 = model2.find_steady_state()
print("s = 33% → y*, i*, c* =", ss_33)

#4-2. Holding all other factors the same as 3-1, what would happen to the steady state consumption (c*) if the saving rate is 50%?
model3 = Growth_Model(para_dict=parameters, state_dict=states)
model3.para_dict['s'] = np.array([0.50])
ss_50 = model3.find_steady_state()
print("s = 50% → y*, i*, c* =", ss_50)