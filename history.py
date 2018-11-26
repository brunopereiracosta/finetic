from gp_edit import *
from MyFuncs import *
from GA import *
from CMAES import *


history = History()

# Decorate the variation operators
toolbox.decorate("mate", history.decorator)
toolbox.decorate("mutate", history.decorator)

run(0.11834723511214429, 0.36282571305589495, 0.002018115516200153*L, 0.12397716233735832, 0.15381049330039887,20,3)

# Create the population and populate the history
population = toolbox.population(n=20)
history.update(population)

# Do the evolution, the decorators will take care of updating the
# history
# [...]

import matplotlib.pyplot as plt
import networkx

graph = networkx.DiGraph(history.genealogy_tree)
graph = graph.reverse()     # Make the grah top-down
colors = [toolbox.evaluate(history.genealogy_history[i])[0] for i in graph]
networkx.draw(graph, node_color=colors)
plt.show()
