import argparse

states = {}
actions = {0:0,
           1:1,
           2:2,
           4:3,
           6:4}

reverseActions = {0:0,
           1:1,
           2:2,
           3:4,
           4:6}



def stateDecoder(state):
    # print(state[0:2], state[2:4])
    return state[0], int(state[1:3]), int(state[3:5])


def stateEncoder(player, balls, run):

    if balls == -1 or runs == -1:
        return states["-1"]

    if balls < 10:
        numBalls = "0" + str(balls)
    else:
        numBalls = str(balls)

    if run < 10:
        numRuns = "0" + str(run)
    else:
        numRuns = str(run)
    

    return states[player + numBalls + numRuns]

def printTransitions(player, balls, runs, action, param):
    poss = [-1, 0, 1, 2, 3, 4, 6]
    for i in range(len(param)):
        

        if player == "0":
            if i == 0: # out 
                newBalls = -1
                newRuns = -1
                reward = 0
                newPlayer = "0"
            else:
                newBalls = balls - 1
                newRuns = runs - poss[i]
                
                if poss[i] % 2 == 1:
                    newPlayer = "1"
                else:
                    newPlayer = "0" 


                if newBalls == 0 and newRuns > 0:
                    newBalls = -1
                    newRuns = -1
                    reward = 0
                elif newRuns <= 0:
                    reward = 1
                    newBalls = 99
                    newRuns = 99
                    newPlayer = "0"
                else:
                    reward = 0
            
            if balls == 7 or balls == 13:
                if newPlayer == "0":
                    newPlayer = "1"
                else:
                    newPlayer = "0"
            
            if newBalls == 99:
                newPlayer = "0"

            newState = stateEncoder(newPlayer,newBalls, newRuns)
            
            # testingFile.write(f"transition {player}/{balls}/{runs} {reverseActions[action]} {poss[i]} {newPlayer}/{newBalls}/{newRuns} {reward} {param[i]}\n")
            print(f"transition {stateEncoder(player, balls, runs)} {action} {newState} {reward} {param[i]}")
       
        else:
            # if action > 0 or i > 2:
            #     newState = stateEncoder("0",-1,-1)
            #     reward = 
            #     prob = 0
            #     testingFile.write(f"transition {player}/{balls}/{runs} {reverseActions[action]} {poss[i]} 0/-1/-1 {reward} {prob}\n")
            #     print(f"transition {stateEncoder(player, balls, runs)} {action} {newState} {reward} {prob}")
            if True:
            # else:
                if i == 0:
                    newBalls = -1
                    newRuns = -1
                    reward = 0
                    prob = q
                    newPlayer = "0"
                elif i == 1:
                    newBalls = balls - 1
                    newRuns = runs
                    newPlayer = "1"
                    prob = (1 - q)/2
                    reward = 0
                elif i == 2:
                    newBalls = balls - 1
                    newRuns = runs - 1
                    newPlayer = "0"
                    prob = (1 - q)/2
                    if newRuns <= 0:
                        newBalls = 99
                        newRuns = 99
                        reward = 1
                    else:
                        reward = 0
                else:
                    newBalls = -1
                    newRuns = -1
                    newPlayer = "0"
                    prob = 0
                    reward = 0

                if newBalls == 0 and reward == 0:
                    newBalls = -1
                    newRuns = -1
                    newPlayer = "0"

                if balls == 7 or balls == 13:
                    if newPlayer == "0":
                        newPlayer = "1"
                    else:
                        newPlayer = "0"
                
                if newBalls == 99:
                    newPlayer = "0"
                
                newState = stateEncoder(newPlayer, newBalls, newRuns)
                # testingFile.write(f"transition {player}/{balls}/{runs} {reverseActions[action]} {poss[i]} {newPlayer}/{newBalls}/{newRuns} {reward} {prob}\n")
                print(f"transition {stateEncoder(player, balls, runs)} {action} {newState} {reward} {prob}")


        # print(balls, newBalls, runs, newRuns)


parser = argparse.ArgumentParser()

parser.add_argument("--states", type = str, required=True)
parser.add_argument("--parameters", type=str, required = True)
parser.add_argument("--q", type=float, required=True)
args = parser.parse_args()

statesFile = args.states
parameterFile = args.parameters
q = args.q

testingFile= open("TESTING", 'w')

it = 0
with open(statesFile, 'r') as f:
    for line in f.readlines():
        states["0" + line[:-1]] = it
        it += 1

    f.seek(0)
    for line in f.readlines():
        states["1" + line[:-1]] = it
        it += 1

print(f"numStates {len(states) + 2}")
print(f"numActions 5")
print(f"end {len(states)} {len(states) + 1}")

states["-1"] = it
it += 1
states["09999"] = it

parameters = []
with open(parameterFile, 'r') as f:
    for line in f.readlines()[1:]:  
        parameters.append([float(i) for i in line.split()])
    

for s in states:
    if s == "-1" or s == "09999":
        continue
    for act in range(len(parameters)):
        # print(s,int(parameters[act][0]))
        player, balls, runs = stateDecoder(s)
        printTransitions(player, balls, runs, actions[int(parameters[act][0])], parameters[act][1:])
                
print("mdtype episodic")
print("discount 1")

testingFile.close()

