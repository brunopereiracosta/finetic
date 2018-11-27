from gp_edit import *
from MyFuncs import *
from GA_3 import *
# from CMAES import *



popu = 20
history = run(cxpb=0.11834723511214429, mutpb=0.36282571305589495, n=int(round(0.002018115516200153*L)), tour=int(round(0.12397716233735832*popu)), termpb=0.15381049330039887,popu=popu,ngen=3)

import matplotlib.pyplot as plt
import networkx

graph = networkx.DiGraph(history.genealogy_tree)
graph = graph.reverse()     # Make the grah top-down
colors = [toolbox.evaluate(history.genealogy_history[i])[0] for i in graph]
networkx.draw(graph, node_color=colors)
plt.show()
