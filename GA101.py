#coding=utf-8
import random
import operator
import math



import pandas as pd
data = pd.read_csv('/Users/bpc/Desktop/Project B.C./R/qantas.csv', sep="\t")
data.head()
date = data['Date'].values
lastprice=data['Last Price'].values

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

###Strongly Typed GP
#In strongly typed GP, every primitive and terminal is assigned a specific type. The output type of a
#primitive must match the input type of another one for them to be connected. For example, if a primitive
#returns a boolean, it is guaranteed that this value will not be multiplied with a float if the multiplication
#operator operates only on floats.

def pow2(input):
    return pow(input,2)

def if_then_else(input, output1, output2):
    return output1 if input else output2

def maximum(input):
    return max(input[0:random.randint(0, len(input))])

def minimum(input):
    return min(input[0:random.randint(0, len(input))])

def get_price(input):
    return input[random.randint(0, len(input))]

def window(input):
    return random.randint(0, len(input))

def shift(input):
    return random.randint(0, len(input))

def part(input):
    return random.randint(0, len(input))

def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1





pset = gp.PrimitiveSetTyped("main", [float], float)
pset.addPrimitive(operator.add, [float, float], float)
pset.addPrimitive(operator.sub, [float, float], float)
pset.addPrimitive(operator.mul, [float, float], float)
pset.addPrimitive(protectedDiv, [float, float], float)
#pset.addPrimitive(operator.pow, [float, float], float)
pset.addPrimitive(pow2, [float], float)
#pset.addPrimitive(math.sqrt, [float], float)
pset.addPrimitive(operator.abs, [float], float)
pset.addPrimitive(math.cos, [float], float)
pset.addPrimitive(math.sin, [float], float)
pset.addPrimitive(math.tan, [float], float)
#pset.addPrimitive(math.atan, [float], float)
#pset.addPrimitive(math.log1p, [float], float)
#pset.addPrimitive(math.exp, [float], float)

pset.addEphemeralConstant("rand101", lambda: random.randint(-1,1),int)

pset.renameArguments(ARG0="x")
#pset.renameArguments(ARG1="y")

#pset.addPrimitive(operator.xor, [bool, bool], bool)
#pset.addPrimitive(if_then_else, [bool, float, float], float)
#pset.addTerminal(3.0, float)
#pset.addTerminal(1, bool)

#In the last code sample, we first define an if then else function that returns the second argument
#if the first argument is true and the third one otherwise. Then, we define our PrimitiveSetTyped. Again,
#the procedure is named "main". The second argument defines the input types of the program. Here, "x" is a
#bool and "y" is a float. The third argument defines the output type of the program as a float.
#Adding primitives to this primitive now requires to set the input and output types of the primitives and terminal.
#For example, we define our "if_then_else" function first argument as a boolean, the second and third argument
#have to be floats. The function is defined as returning a float. We now understand that the multiplication
#primitive can only have the terminal 3.0, the if_then_else function or the "y" as input, which are the only
#floats defined.

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin,
               pset=pset)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genGrow, pset=pset, min_=1, max_=15)
toolbox.register("individual", tools.initIterate, creator.Individual,toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)
#
def evalSymbReg(individual, points):
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    # Evaluate the mean squared error between the expression
    # and the real function : x**4 + x**3 + x**2 + x
    sqerrors = ((func(x) - x**4 - x**3 - x**2 - x)**2 for x in points)
    return math.fsum(sqerrors) / len(points),
toolbox.register("evaluate", evalSymbReg, points=[x/10. for x in range(-10,10)])
#
toolbox.register("select", tools.selBest)
toolbox.register("mate", gp.cxOnePointLeafBiased,termpb=0.2)
toolbox.register("expr_mut", gp.genGrow, min_=0, max_=5)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
stats_size = tools.Statistics(len)
mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
mstats.register("avg", numpy.mean)
mstats.register("std", numpy.std)
mstats.register("min", numpy.min)
mstats.register("max", numpy.max)

pop = toolbox.population(n=500)
hof = tools.HallOfFame(1)
pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.3, 200, stats=mstats,
                                   halloffame=hof, verbose=True)

print(hof[0])


##
#expr = toolbox.individual()
#nodes, edges, labels = gp.graph(expr)
#tree = gp.PrimitiveTree(expr)
#str(tree)

#function = gp.compile(tree, pset)
#function(10,20)

#import matplotlib.pyplot as plt
#import networkx as nx


#g = nx.Graph()
#g.add_nodes_from(nodes)
#g.add_edges_from(edges)
#pos = nx.circular_layout(g)

#nx.draw_networkx_nodes(g, pos)
#nx.draw_networkx_edges(g, pos)
#nx.draw_networkx_labels(g, pos, labels)
#plt.show()
