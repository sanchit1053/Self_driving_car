"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the base Algorithm class that all algorithms should inherit
from. Here are the method details:
    - __init__(self, num_arms, horizon): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, reward): This method is called just after the 
        give_pull method. The method should update the algorithm's internal
        state based on the arm that was pulled and the reward that was received.
        (The value of arm_index is the same as the one returned by give_pull.)

We have implemented the epsilon-greedy algorithm for you. You can use it as a
reference for implementing your own algorithms.
"""

import numpy as np
import math
# Hint: math.log is much faster than np.log for scalars

class Algorithm:
    def __init__(self, num_arms, horizon):
        self.num_arms = num_arms
        self.horizon = horizon
    
    def give_pull(self):
        raise NotImplementedError
    
    def get_reward(self, arm_index, reward):
        raise NotImplementedError

# Example implementation of Epsilon Greedy algorithm
class Eps_Greedy(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # Extra member variables to keep track of the state
        self.eps = 0.1
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
    
    def give_pull(self):
        if np.random.random() < self.eps:
            return np.random.randint(self.num_arms)
        else:
            return np.argmax(self.values)
    
    def get_reward(self, arm_index, reward):
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value


# START EDITING HERE
# You can use this space to define any helper functions that you need

def KL(p, q):
    a = np.zeros(len(p))
    b = np.zeros(len(p))

    term1 = (p * np.log(p / (q + 1e-9) + 1e-9))
    term2 = ((1 - p) * np.log((1 - p) / (1 - q + 1e-9) + 1e-9))
    a[p > 0] =  term1[p > 0]
    b[p < 1] = term2[p<1]

    return a + b



# END EDITING HERE

class UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        self.success = np.zeros(num_arms)
        self.pulls = np.zeros(num_arms)
        self.ucb = np.zeros(num_arms)
        self.t = 0
        # You can add any other variables you need here
        # START EDITING HERE
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        if self.t < self.num_arms:
            return self.t
        
        return np.argmax(self.ucb)

        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.t += 1
        self.pulls[arm_index] += 1
        self.success[arm_index] += reward

        if self.t < self.num_arms:
            return
        
        empMean = self.success / self.pulls
        exploration = np.sqrt(2 * math.log(self.t) / self.pulls)
        self.ucb = empMean + exploration
        # END EDITING HERE

class KL_UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)

        # You can add any other variables you need here
        # START EDITING HERE
        self.success = np.zeros(num_arms)
        self.pulls = np.zeros(num_arms)
        self.klucb = np.zeros(num_arms)
        self.t = 0
        self.c = 3
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        if self.t < self.num_arms:
            return self.t
        return np.argmax(self.klucb)
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.t += 1
        self.pulls[arm_index] += 1
        self.success[arm_index] += reward

        if self.t < self.num_arms:
            return
        
        empMean = self.success / self.pulls
        term = (math.log(self.t) + self.c * math.log ( math.log( self.t))) / self.pulls

        l = empMean.copy()
        r = np.ones(self.num_arms)
        for _ in range(16):
            m = (l + r) / 2
            KLValue = KL(empMean, m)
            l[KLValue < term] = m[KLValue < term]
            r[KLValue >= term] = m[KLValue >= term]

        self.klucb = m
        # END EDITING HERE


class Thompson_Sampling(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.success = np.zeros(num_arms)
        self.failures = np.zeros(num_arms)
        self.samples = np.zeros(num_arms)
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        return np.argmax(self.samples)
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.success[arm_index] += reward
        self.failures[arm_index] += (1 - reward)

        self.samples = [np.random.beta(i+1, j+1) for i,j in zip(self.success, self.failures)]
        #  END EDITING HERE
