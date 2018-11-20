##DEVELOPED
from gp_edit import *

#coding=utf-8
import random
import operator
import math

epsilon = 1e-20

#import pandas as pd
#data = pd.read_csv('/Users/bpc/Desktop/Project B.C./R/qantas.csv', sep="\t")
#data.head()
#date = data['Date'].values
#lastprice=data['Last Price'].values

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

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

#ind SHOULD BE POSTITIVE
#part is exactly like shift for negative numbers, but we'll keep it separate because when introducing weights it might be useful to give shift and part different weights
def shift(arr,ind):
	return arr[-(ind+1)]

#ind SHOULD BE POSTITIVE
def part(arr,ind):
	return arr[ind]

def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return left / epsilon

#Note: add line 'pset.addPrimitive(SMA, [array,int,int], float)' to try to add SMA as primitive

#window and ind SHOULD BE POSTITIVE
def SMA(arr,window,ind):
	if window==0: #protect agains division by 0 (choose arr.s just as a choice...)
		window=arr.s

	if ind==0:
		temp = arr[-window:]
	else:
		temp = arr[-window-ind:-ind]
	return sum(temp)/window

class array:
    def __init__(self, v):
        self.v = v
        self.s = len(v)
        
    def __len__(self):
        return self.s
    def __repr__(self): #this is only so that print(array) works
        return self.v.__repr__()

    def protect(self,key): #make it so that key cannot excede [-N,N-1]
        if key>=self.s: #protect agains invalid indices
        	print("WARNING: index over valid size (key={key}; size={size})".format(key=key,size=self.s))
        	return self.s-1
        elif -key>self.s: #protect agains invalid indices
        	print("WARNING: index under valid size (key={key}; size={size})".format(key=key,size=self.s))
        	return -self.s
        return key

    def __getitem__(self, key):
        if isinstance(key, slice): #if key=slice(start,stop,step), protect the start and stop
            return array(self.v[slice(self.protect(key.start),self.protect(key.stop),key.step)])
        return self.v[self.protect(key)]


N=100
vec=[0]*N
for i in range(0,N):
	vec[i]=random.uniform(-1,1)
arr=array(vec)

pset = gp.PrimitiveSetTyped("main", [array], float)
pset.addPrimitive(SMA, [array, int, int], float)
pset.addPrimitive(operator.add, [float, float], float)
pset.addPrimitive(part, [array,int], float)
pset.addPrimitive(shift, [array,int], float)
pset.addEphemeralConstant("randI", lambda: random.randint(0,N-1),int)
pset.addEphemeralConstant("randF", lambda: random.uniform(-1,1),float)
# pset.addPrimitive(operator.sub, [float, float], float)
# pset.addPrimitive(operator.mul, [float, float], float)
# pset.addPrimitive(protectedDiv, [float, float], float)
#pset.addPrimitive(operator.pow, [float, float], float)
# pset.addPrimitive(pow2, [float], float)
#pset.addPrimitive(math.sqrt, [float], float)
# pset.addPrimitive(operator.abs, [float], float)
# pset.addPrimitive(math.cos, [float], float)
# pset.addPrimitive(math.sin, [float], float)
# pset.addPrimitive(math.tan, [float], float)
#pset.addPrimitive(math.atan, [float], float)
#pset.addPrimitive(math.log1p, [float], float)
#pset.addPrimitive(math.exp, [float], float)
# pset.addPrimitive(idem, [A], A)
# pset.addPrimitive(idem, [int], int)
# pset.addPrimitive(SMA, [array,int,int], float)

# pset.renameArguments(ARG0="x")
#pset.renameArguments(ARG1="y")

#pset.addPrimitive(operator.xor, [bool, bool], bool)
#pset.addPrimitive(if_then_else, [bool, float, float], float)
#pset.addTerminal(3.0, float)
# pset.addTerminal(1, float)

#In the last code sample, we first define an if then else function that returns the second argument
#if the first argument is true and the third one otherwise. Then, we define our PrimitiveSetTyped. Again,
#the procedure is named "main". The second argument defines the input types of the program. Here, "x" is a
#bool and "y" is a float. The third argument defines the output type of the program as a float.
#Adding primitives to this primitive now requires to set the input and output types of the primitives and terminal.
#For example, we define our "if_then_else" function first argument as a boolean, the second and third argument
#have to be floats. The function is defined as returning a float. We now understand that the multiplication
#primitive can only have the terminal 3.0, the if_then_else function or the "y" as input, which are the only
#floats defined.

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax,
               pset=pset)

toolbox = base.Toolbox()
toolbox.register("expr", genGrow_edit, pset=pset, min_=1, max_=15)
toolbox.register("individual", tools.initIterate, creator.Individual,toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

#def myfit(ind,arg):
    # Transform the tree expression in a callable function
    #func = toolbox.compile(expr=ind)
    #out = (func(arg)-SMA(arg,4,2))**2
    # out = (func(arg)-arg[4])**2
#return out,

fit=0
def fitness_predictor(individual,arg):
    global fit
    func = toolbox.compile(expr=individual)
    for i in range(N-10):
        print(i)
        if ((func(arg[0:9+i])>0)==(arg[9+i]>arg[9+i-1])):
            fit += 1
        return fit

toolbox.register("evaluate", fitness_predictor,arg=arr)
#
toolbox.register("select", tools.selBest)
toolbox.register("mate", gp.cxOnePointLeafBiased,termpb=0.2)
toolbox.register("expr_mut", genGrow_edit, min_=0, max_=5)
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
pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.3, 50, stats=mstats,
                                   halloffame=hof, verbose=True)

#print(arr,SMA(arr,4,2))
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
