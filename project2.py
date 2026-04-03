"""
Weekly project 2. The Gale-Shapley algorithm
"""

# Section 1. Preparation
# 1-1. import all the necessary python modules
import json
import copy


# 1-2. import the datasets
with open('project2_data.json') as f:
    preference = json.load(f)


# Section 2 Extract information from the dataset, 
# 2-1. create a dictionary 'guyprefer' contains mens' preferences
guyprefers = preference['men_preference']
    
# 2-2. create a dictionary 'galprefer' contains women's preferences
galprefers = preference['women_preference']
    
# 2-3. create a list contains guys who are currently not engaged, 
# sort alphabetically
free_guy = sorted(list(guyprefers.keys()))

# 2-4. generate an empty dictionary 'engage_book' to store result
engage_book = {}

# 2-5. make copies of guyprefers and gal refers
guypreference = copy.copy(guyprefers)
galpreference = copy.copy(galprefers)

# Section 3. Impletement the Gale-Shapley algorithm 
# Follow the algorithm flowchart, it should be very helpful
while free_guy:
    
# pop the first guy in the free_guy list, let him take the move
    a_brave_guy = free_guy.pop(0)
    
# get his preference list
    mylist = guypreference[a_brave_guy]
    
    # Decision 2: has this guy been rejected by ALL the ladies?
    if not mylist:
       # let him die alone 
       continue
   
    # Let's propose to my favorate lady!
    my_girl = mylist[0]
    
    # YOU WILL NEED TO DO THE REST, GOOD LUCK AND HAVE FUN!.
    # Decision 3: is this lady engaged with another guy?
    if my_girl not in engage_book:
        #No
        engage_book[my_girl] = a_brave_guy
        #Yes
    else:
        current_fiance = engage_book[my_girl]
        
        # Decision 4: does she like the current proposer better than her fiancé?
        prefers_new = (
            galpreference[my_girl].index(a_brave_guy)
            < galpreference[my_girl].index(current_fiance)
        )

        if prefers_new:
            free_guy.append(current_fiance)
            engage_book[my_girl] = a_brave_guy
        else:
            guypreference[a_brave_guy].pop(0)
            free_guy.append(a_brave_guy)

print(engage_book)
