#DEVELOPED
from gp_edit import *
from MyFuncs import *
from GA import *

from deap import benchmarks
from deap import cma

def myfunc(vec):
    a=0.
    for i in range(0,len(vec)):
        a = a + (vec[i]-(i+1))**2
    return a

# Problem size
N=3

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("evaluate", myfunc)

def main():
    # The cma module uses the numpy random number generator
    numpy.random.seed(128)
    
    # The CMA-ES algorithm takes a population of one individual as argument
    # The centroid is set to a vector of 5.0 see http://www.lri.fr/~hansen/cmaes_inmatlab.html
    # for more details about the rastrigin and other tests for CMA-ES
    strategy = cma.Strategy(centroid=[0.82]*N, sigma=3.14, lambda_=0.69*N)
    toolbox.register("generate", strategy.generate, creator.Individual)
    toolbox.register("update", strategy.update)
    
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    #logger = tools.EvolutionLogger(stats.functions.keys())
    
    # The CMA-ES algorithm converge with good probability with those settings
    algorithms.eaGenerateUpdate(toolbox, ngen=250, stats=stats, halloffame=hof)
    
    # print "Best individual is %s, %s" % (hof[0], hof[0].fitness.values)
    return hof[0].fitness.values[0]

if __name__ == "__main__":
    main()
