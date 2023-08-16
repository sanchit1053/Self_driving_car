import argparse
import numpy as np
from pulp import *


class MDP:
    def __init__(self, path):
        with open(path, 'r') as f:

            # get the state, actions 
            self.numStates = int(f.readline().split()[1])
            self.numActions = int(f.readline().split()[1])
           
            # Initialize the reward and the transition matrix
            self.transitions = np.zeros((self.numStates, self.numActions, self.numStates))
            self.rewards = np.zeros((self.numStates, self.numActions, self.numStates))
            
            endStates = [int(e) for e in f.readline().split()[1:]]
            # for end states change the transition and reward to 0
            if endStates != [-1]:
                self.transitions[endStates, :, :] = 0
                self.rewards[endStates, :, :] = 0

            line = f.readline().split()

            # While Transitions
            while line[0] == "transition":
                s = int(line[1])
                a = int(line[2])
                snew = int(line[3])
                r = float(line[4])
                t = float(line[5])

                # store the transition and reward in the corresponding matrix
                self.transitions[s, a, snew] += t
                self.rewards[s, a, snew] = r
                line = f.readline().split()

            # store the type and gamma
            self.type = line[1]
            self.gamma = float(f.readline().split()[1])

    # Util Function to print the values and policy in required manner
    def print(self, values, policy):
        for v, p in zip(values, policy):
            print(f"{v:.6f} {p}")
        

    # Value Iteration
    def vi(self):
        values = np.zeros(self.numStates)
        error = 10000

        # Iterate over Values using the best policy till converge
        while error > 1e-9:
            newvalues = np.max(np.sum(self.transitions * (self.rewards + self.gamma * values.reshape(1,1,self.numStates)), axis = 2), axis = 1)
            error = np.linalg.norm(values - newvalues)
            values = newvalues

        # Get policy
        policy = np.argmax(np.sum(self.transitions * (self.rewards + self.gamma * values.reshape(1,1,self.numStates)), axis = 2), axis = 1)

        self.print(values, policy)

    #HOWARDS POLICY ITERATION
    def hpi(self):

        policy = np.zeros(self.numStates)
        policyChange = True

        # While Policy Keeps changing
        while policyChange:
            values = np.zeros(self.numStates)
            error = 10000

            # Calculate the value for the current policy
            while error > 1e-9:
                computedValues = np.sum(self.transitions * (self.rewards + self.gamma * values.reshape(1,1,self.numStates)), axis = 2)
                newvalues = np.array([computedValues[i, int(policy[i])] for i in range(self.numStates)])
                error = np.linalg.norm(values - newvalues)
                values = newvalues

            # check if value has a better policy
            newpolicy = np.argmax(np.sum(self.transitions * (self.rewards + self.gamma * values.reshape(1,1,self.numStates)), axis = 2), axis = 1)
            
            # if policy same no change
            if np.array_equal(newpolicy, policy):
                policyChange = False
            policy = newpolicy        

        self.print(values, policy)

    # Create a linear program and solve using PuLP
    def lp(self ):
        LP = LpProblem("Bellman", LpMaximize)
        variables = []

        # ADDING THE value variable for each state
        for v in range(self.numStates):
            var = "v" + str(v)
            x = LpVariable(var)
            variables.append(x)
        
        # FOR EAch state, for each action 
        for state in range(self.numStates):
            for act in range(self.numActions):
                temp = 0
                # Summation over destination states
                for state2 in range(self.numStates):
                    temp += self.transitions[state, act, state2] * (self.rewards[state,act,state2] + self.gamma * variables[state2])
                
                # Add the constraint to LP
                LP += variables[state] >= temp

        # Add the objective function 
        LP += -1 * sum(variables)

        #Solve for optimal value
        status = LP.solve(PULP_CBC_CMD(msg=0))
        
        # Get the Values from the LP solver
        values = np.zeros(self.numStates)
        for state in range(self.numStates):
            values[state] = value(variables[state])
        
        # Get the Policy
        policy = np.argmax(np.sum(self.transitions * (self.rewards + self.gamma * values.reshape(1,1,self.numStates)), axis = 2), axis = 1)
        self.print(values,policy)

    # Call the appropriate function 
    def plan(self, algo):
        if algo == "vi":
            self.vi()
        
        elif algo == "hpi":
            self.hpi()
        
        elif algo == "lp":
            self.lp()
            
    def value(self, policyPath):
        policy = []

        # parse the policy file
        with open(policyPath, 'r') as f:
            for line in f.readlines():
                policy.append(int(line))
        
        # Same code as before in hpi iterate over values till converge
        policy = np.array(policy)
        values = np.zeros(self.numStates)
        error = 10000
        while error > 1e-9:
            computedValues = np.sum(self.transitions * (self.rewards + self.gamma * values.reshape(1,1,self.numStates)), axis = 2)
            newvalues = np.array([computedValues[i, int(policy[i])] for i in range(self.numStates)])
            error = np.linalg.norm(values - newvalues)
            values = newvalues
        
        self.print(values, policy)








parser = argparse.ArgumentParser()

if __name__ == "__main__":

    parser.add_argument("--mdp", type = str)
    parser.add_argument("--algorithm", type = str, default = "vi")
    parser.add_argument("--policy", type = str, default="NA")

    args = parser.parse_args()

    mdpPath = args.mdp
    algo = args.algorithm
    policyPath = args.policy
    availableAlgo = ["vi", "hpi", "lp"]

    if algo not in availableAlgo:
        print("algorithm not availabale")
        exit()

    mdpProvided = MDP(mdpPath)

    # IF policy not provided plan a optimal policy
    if policyPath == "NA":
        mdpProvided.plan(algo)
    else: # else find the value for policy given 
        mdpProvided.value(policyPath)







