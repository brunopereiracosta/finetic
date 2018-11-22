#DEVELOPED
from GA import *

from deap import benchmarks
from deap import cma

def myfunc(vec):
    a=0.
    for i in range(0,len(vec)):
        a = a + (vec[i]-(i+1))**2.
    return a,



# Problem size
N=1

creator.create("FitnessMin1", base.Fitness, weights=(-1.0,))
creator.create("Individual1", list, fitness=creator.FitnessMin1)

toolbox1 = base.Toolbox()
toolbox1.register("evaluate", average_fitness)

def mycmaes():
    # The cma module uses the numpy random number generator
    numpy.random.seed()
    
    # The CMA-ES algorithm takes a population of one individual as argument
    # The centroid is set to a vector of 5.0 see http://www.lri.fr/~hansen/cmaes_inmatlab.html
    # for more details about the rastrigin and other tests for CMA-ES
    strategy = cma.Strategy(centroid=[0.5]*N, sigma=0.1, lambda_=10*N)
    toolbox1.register("generate", strategy.generate, creator.Individual1)
    toolbox1.register("update", strategy.update)
    
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg1", numpy.mean)
    stats.register("std1", numpy.std)
    stats.register("min1", numpy.min)
    stats.register("max1", numpy.max)
    #logger = tools.EvolutionLogger(stats.functions.keys())
    
    # The CMA-ES algorithm converge with good probability with those settings
    algorithms.eaGenerateUpdate(toolbox1, ngen=2, stats=stats, halloffame=hof)
    
    # print "Best individual is %s, %s" % (hof[0], hof[0].fitness.values)
    # print(hof[0])
    # return hof[0].fitness.values[0]
    print(hof[0].fitness.values[0])
    return hof[0]

def main():
    repeat = 2
    arr = numpy.array([mycmaes() for i in range(0,repeat)])
    print(arr)
    print(numpy.mean(arr))
    print(numpy.std(arr))

if __name__ == "__main__":
    main()
