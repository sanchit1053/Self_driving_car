import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--value-policy", type=str, required=True)
parser.add_argument("--states", type=str, required=True)

args = parser.parse_args()
valueFile = args.value_policy
statesFile = args.states

states = {}

actions = {0:0,
           1:1,
           2:2,
           3:4,
           4:6}

it = 0
with open(statesFile, 'r') as f:
    for line in f.readlines():
        states[it] = line[:-1]
        it += 1

it = 0
with open(valueFile, 'r') as f:
    for line in f.readlines()[:len(states)]:
        print(f"{states[it]} {actions[int(line.split()[1])]} {line.split()[0]}")
        it += 1

