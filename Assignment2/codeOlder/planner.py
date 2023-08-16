import argparse
import numpy as np
from pulp import *


class state:
    def __init__(self):
        self.terminal = False


class MDP:
    def __init__(self, path):
        with open(path, 'r') as f:
            self.numStates = int(f.readline().split()[1])
            self.numActions = int(f.readline().split()[1])
            self.transitions = np.zeros((self.numStates, self.numActions, self.numStates))
            self.rewards = np.zeros((self.numStates, self.numActions, self.numStates))
            endStates = [int(e) for e in f.readline().split()[1:]]
            if endStates != [-1]:
                self.transitions[endStates, :, :] = 0
                self.rewards[endStates, :, :] = 0

            line = ""
            line = f.readline().split()
            while line[0] == "transition":
                s = int(line[1])
                a = int(line[2])
                snew = int(line[3])
                r = float(line[4])
                t = float(line[5])
                self.transitions[s, a, snew] += t
                self.rewards[s, a, snew] = r
                line = f.readline().split()

            self.type = line[1]
            self.gamma = float(f.readline().split()[1])

    def print(self, values, policy):
        # with open
        for v, p in zip(values, policy):
            print(f"{v} {p}")
        

    def vi(self):
        values = np.zeros(self.numStates)
        error = 10000
        while error > 1e-9:
            # print(values)
            # print(np.sum(self.transitions * (self.rewards + self.gamma * values.reshape(1,1,self.numStates)), axis = 2))
            # temp = input()
            newvalues = np.max(np.sum(self.transitions * (self.rewards + self.gamma * values.reshape(1,1,self.numStates)), axis = 2), axis = 1)
            error = np.linalg.norm(values - newvalues)
            values = newvalues

        policy = np.argmax(np.sum(self.transitions * (self.rewards + self.gamma * values.reshape(1,1,self.numStates)), axis = 2), axis = 1)

        self.print(values, policy)

    def hpi(self):
        values = np.zeros(self.numStates)
        policy = np.zeros(self.numStates)
        policyChange = True
        while policyChange:
            error = 10000
            while error > 1e-9:
                computedValues = np.sum(self.transitions * (self.rewards + self.gamma * values.reshape(1,1,self.numStates)), axis = 2)
                newvalues = np.array([computedValues[i, int(policy[i])] for i in range(self.numStates)])
                error = np.linalg.norm(values - newvalues)
                values = newvalues

            newpolicy = np.argmax(np.sum(self.transitions * (self.rewards + self.gamma * values.reshape(1,1,self.numStates)), axis = 2), axis = 1)
            
            if np.array_equal(newpolicy, policy):
                policyChange = False
            policy = newpolicy        

        self.print(values, policy)
        pass

    def lp(self ):
        LP = LpProblem("Bellman", LpMaximize)
        variables = []
        for v in range(self.numStates):
            var = "v" + str(v)
            x = LpVariable(var)
            variables.append(x)
        
        for state in range(self.numStates):
            for act in range(self.numActions):
                temp = 0
                for state2 in range(self.numStates):
                    temp += self.transitions[state, act, state2] * (self.rewards[state,act,state2] + self.gamma * variables[state2])
                # LP += variables[state] >= sum(self.transitions[state, act, :] * (self.rewards[state, act, :] + self.gamma * variables))
                LP += variables[state] >= temp
        LP += -1 * sum(variables)

        status = LP.solve(PULP_CBC_CMD(msg=0))
        
        values = np.zeros(self.numStates)
        for state in range(self.numStates):
            # print(value(variables[state]))
            values[state] = value(variables[state])
        
        policy = np.argmax(np.sum(self.transitions * (self.rewards + self.gamma * values.reshape(1,1,self.numStates)), axis = 2), axis = 1)
        self.print(values,policy)

    def plan(self, algo):
        if algo == "vi":
            self.vi()
        
        elif algo == "hpi":
            self.hpi()
        
        elif algo == "lp":
            self.lp()
            
    def value(self, policyPath):
        policy = []
        with open(policyPath, 'r') as f:
            for line in f.readlines():
                policy.append(int(line))
        # print(policy)
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
    availableAlgo = ["vi", "hpi", "lp"]

    if algo not in availableAlgo:
        print("algorithm not availabale")
        exit()

    policyPath = args.policy
    mdpProvided = MDP(mdpPath)
    if policyPath == "NA":
        mdpProvided.plan(algo)
    else:
        mdpProvided.value(policyPath)







