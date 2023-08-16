import argparse

states = {}
actions = {0:0,
           1:1,
           2:2,
           4:3,
           6:4}


# given a string stateDecoder will return tuple of player, balls nad runs left
def stateDecoder(state):
    return state[0], int(state[1:3]), int(state[3:5])


# given the player, balls and runs it will return the state code 
def stateEncoder(player, balls, run):

    # OUT STATE
    if balls == -1 or runs == -1:
        return states["-1"]

    # convert always to 2 digits
    if balls < 10:
        numBalls = "0" + str(balls)
    else:
        numBalls = str(balls)

    if run < 10:
        numRuns = "0" + str(run)
    else:
        numRuns = str(run)
    
    # Return the mapping from the states Dictionary
    return states[player + numBalls + numRuns]

def printTransitions(player, balls, runs, action, param):
    # Possible Outcomes
    poss = [-1, 0, 1, 2, 3, 4, 6]
    
    # FOR EACH POSS    
    for i in range(len(param)):

        ## BETTER PLAYER
        if player == "0":
            if i == 0: # Player is out
                newBalls = -1
                newRuns = -1
                reward = 0
                newPlayer = "0"
            else:

                #update the balls and runs
                newBalls = balls - 1
                newRuns = runs - poss[i]
                
                # Update the player
                if poss[i] % 2 == 1:
                    newPlayer = "1"
                else:
                    newPlayer = "0" 


                
                if newBalls == 0 and newRuns > 0: # IF balls finished and not reached the score
                    newBalls = -1
                    newRuns = -1
                    reward = 0
                elif newRuns <= 0: # IF target mathched Then winning state
                    reward = 1
                    newBalls = 99
                    newRuns = 99
                    newPlayer = "0"
                else:
                    reward = 0
            
            # STRIKE CHANGE ON OVER COMPLETION
            if balls == 7 or balls == 13:
                if newPlayer == "0":
                    newPlayer = "1"
                else:
                    newPlayer = "0"
            
            # IF WINNING JUST CHANGE THE PLAYER TO 0, JUST TO REDUCE ONE STATE
            if newBalls == 99:
                newPlayer = "0"


            newState = stateEncoder(newPlayer,newBalls, newRuns)
            
            # transition oldstate action newstate reward prob
            print(f"transition {stateEncoder(player, balls, runs)} {action} {newState} {reward} {param[i]}")
       
        else: # TAILENDER PLAYER

            if i == 0: # OUT
                newBalls = -1
                newRuns = -1
                reward = 0
                prob = q
                newPlayer = "0"

            elif i == 1: # ZERO RUNS
                newBalls = balls - 1
                newRuns = runs
                newPlayer = "1"
                prob = (1 - q)/2
                reward = 0

            elif i == 2: # ONE RUNS
                newBalls = balls - 1
                newRuns = runs - 1
                newPlayer = "0"
                prob = (1 - q)/2
                if newRuns <= 0: # WON THE GAME
                    newBalls = 99
                    newRuns = 99
                    reward = 1
                else:
                    reward = 0
            else: # ALL OTHER HAVE ZERO PROBABILITY
                newBalls = -1
                newRuns = -1
                newPlayer = "0"
                prob = 0
                reward = 0

            if newBalls == 0 and reward == 0: # IF BALLS ARE FINISHED THEN LOST
                newBalls = -1
                newRuns = -1
                newPlayer = "0"

            if balls == 7 or balls == 13: # OVER COMPLETE
                if newPlayer == "0":
                    newPlayer = "1"
                else:
                    newPlayer = "0"
            
            if newBalls == 99: # AGAIN IF WON CHANGE NEW PLAYER TO 0
                newPlayer = "0"
            
            newState = stateEncoder(newPlayer, newBalls, newRuns)

            print(f"transition {stateEncoder(player, balls, runs)} {action} {newState} {reward} {prob}")



parser = argparse.ArgumentParser()

parser.add_argument("--states", type = str, required=True)
parser.add_argument("--parameters", type=str, required = True)
parser.add_argument("--q", type=float, required=True)
args = parser.parse_args()

statesFile = args.states
parameterFile = args.parameters
q = args.q

it = 0

# Add a state for both the 0 and 1 player
with open(statesFile, 'r') as f:
    for line in f.readlines():
        states["0" + line[:-1]] = it
        it += 1

    f.seek(0)
    for line in f.readlines():
        states["1" + line[:-1]] = it
        it += 1


# Print the basic numStates, numActions and end states
print(f"numStates {len(states) + 2}")
print(f"numActions 5")
print(f"end {len(states)} {len(states) + 1}")

# Add the losing and winning state
states["-1"] = it
it += 1
states["09999"] = it

# STORE THE PARAMETERS
parameters = []
with open(parameterFile, 'r') as f:
    for line in f.readlines()[1:]:  
        parameters.append([float(i) for i in line.split()])
    

# FOR EACH STATE ADD THE TRANSITIONS TO ALL THE OTHER STATES
for s in states:
    if s == "-1" or s == "09999":
        continue
    for act in range(len(parameters)):
        # print(s,int(parameters[act][0]))
        player, balls, runs = stateDecoder(s)
        printTransitions(player, balls, runs, actions[int(parameters[act][0])], parameters[act][1:])

# WE CAN KEEP THE DISCOUNT 1 as we do not care to win in less number of balls   
print("mdtype episodic")
print("discount 1")


