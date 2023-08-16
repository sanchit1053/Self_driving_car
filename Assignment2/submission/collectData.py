
import subprocess
import numpy as np


# Part 1
# for q in np.linspace(0,1,num = 100):

#     cmd = "python", "encoder.py", "--states" , "states", "--parameters", "data/cricket/sample-p1.txt", "--q", str(q)
#     f = open("temp", "w")
#     subprocess.call(cmd, stdout=f)
#     f.close()

#     # cmd = "python", "planner.py", "--mdp", "temp", "--policy", "pol"
#     cmd = "python", "planner.py", "--mdp", "temp"
#     output = subprocess.check_output(cmd)
#     print(output.split()[0])


# Part 2
# for runs in range(20, 0, -1):
#     # print(runs)
#     f = open("states", "w")
#     cmd = "python", "cricket_states.py", "--balls", "10", "--runs", str(runs)
#     subprocess.call(cmd, stdout=f)
#     f.close()

#     f = open("temp", "w")
#     cmd = "python", "encoder.py", "--states" , "states", "--parameters", "data/cricket/sample-p1.txt", "--q", "0.25"
#     subprocess.call(cmd, stdout=f)
#     f.close()

#     # cmd = "python", "planner.py", "--mdp", "temp", "--policy", "pol"
#     cmd = "python", "planner.py", "--mdp", "temp"
#     output = subprocess.check_output(cmd)
#     print(output.split()[0])


# Part 3
for balls in range(15, 0, -1):
    # print(runs)
    f = open("states", "w")
    cmd = "python", "cricket_states.py", "--balls", str(balls), "--runs", "10"
    subprocess.call(cmd, stdout=f)
    f.close()

    f = open("temp", "w")
    cmd = "python", "encoder.py", "--states" , "states", "--parameters", "data/cricket/sample-p1.txt", "--q", "0.25"
    subprocess.call(cmd, stdout=f)
    f.close()

    # cmd = "python", "planner.py", "--mdp", "temp", "--policy", "pol"
    cmd = "python", "planner.py", "--mdp", "temp"
    output = subprocess.check_output(cmd)
    print(output.split()[0])
