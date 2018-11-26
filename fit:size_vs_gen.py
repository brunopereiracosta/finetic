from gp_edit import *
from MyFuncs import *
from GA import *
from CMAES import *

popu = pop_GA*2
logbook = run(cxpb=0.11834723511214429, mutpb=0.36282571305589495, n=int(round(0.002018115516200153*L)), tour=int(round(0.12397716233735832*popu)), termpb=0.15381049330039887,popu=popu,ngen=500)

gen = logbook.select("gen")
fit_mins = logbook.chapters["fitness"].select("max")
size_avgs = logbook.chapters["size"].select("avg")

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots()
line1 = ax1.plot(gen, fit_mins, "b-", label="Minimum Fitness")
ax1.set_xlabel("Generation")
ax1.set_ylabel("Fitness", color="b")
for tl in ax1.get_yticklabels():
    tl.set_color("b")

ax2 = ax1.twinx()
line2 = ax2.plot(gen, size_avgs, "r-", label="Average Size")
ax2.set_ylabel("Size", color="r")
for tl in ax2.get_yticklabels():
    tl.set_color("r")

lns = line1 + line2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc="center right")

plt.show()
