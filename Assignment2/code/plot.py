import matplotlib.pyplot as plt
import numpy as np
optimal = []
random = []

with open("PlotData/optimalPolicy3",'r') as f:
    for l in f.readlines():
        optimal.append(float(l))
        
with open("PlotData/randomPolicy3",'r') as f:
    for l in f.readlines():
        random.append(float(l))

fig, axes = plt.subplots()
axes.set_title("Number of balls")
axes.set_xlabel("Number of Balls Left")
axes.set_ylabel("Probability of Winning")
q = np.arange(15, 0,-1)
name = [str(i) for i in q]
x = np.arange(1,16)
axes.set_xlim(0,16)
axes.set_xticks(x)
axes.plot(x,optimal, label="optimal")
axes.plot(x,random, label ="random")
axes.set_xticklabels(name)
print(name)
axes.legend()
plt.show()
