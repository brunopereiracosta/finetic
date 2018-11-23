#DEVELOPED
from GA import *

from deap import benchmarks
from deap import cma


####################################################################
# Problem parametes
D           = 5     #dimensions

pop_GA      = 20    #population size in GA
pop_CMAES   = 5    #population size in CMA-ES

ngen_GA     = 50     #number of generations in GA
ngen_CMAES  = 3     #number of generations in CMA-ES

reps_GA     = 1     #repetitions of GA
reps_CMAES  = 1    #repetitions of CMA-ES

sigma       = 0.25   #sigma for CMA-ES

cxpb_def    = 0.5
mutpb_def   = 0.5
#n_def       = 5000./L
n_def       = 0.5
#tour_def    = 3./pop_GA
tour_def    = 0.5
termpb_def  = 0.5
####################################################################

vec_def     = [cxpb_def,mutpb_def,n_def,tour_def,termpb_def]

#moved it to here because it must be defined after 'vec_def'
def average_fitness(vec,pop,ngen,reps):
    new = vec_def[:]
    if len(vec)>5:
        raise "FIZESTE PORCARIA"
    for i in range(0,len(vec)):
        new[i]=vec[i]

    if (new[0]<0 or new[0]>1 or new[1]<0 or new[1]>1 or new[2]<0 or new[2]>1 or new[3]<0 or new[3]>1 or new[4]<0 or new[4]>1):
        # print("OUT OF DOMAIN, maybe sigma is too big")
        return 10**10,
    return sum([run(cxpb=new[0],mutpb=new[1],n=int(round(new[2]*(L-1)+1)),tour=int(round(new[3]*(pop-1)+1)),termpb=new[4],pop=pop,ngen=ngen) for i in range(0,reps)])/reps,



creator.create("FitnessMin1", base.Fitness, weights=(-1.0,))
creator.create("Individual1", list, fitness=creator.FitnessMin1)

toolbox1 = base.Toolbox()
toolbox1.register("evaluate", average_fitness, pop=pop_GA, ngen=ngen_GA, reps=reps_GA)

count = 1
def mycmaes():
    global count
    print("CMA-ES REPETITION",count)
    count+=1

    # The cma module uses the numpy random number generator
    numpy.random.seed()
    
    # The CMA-ES algorithm takes a population of one individual as argument
    # The centroid is set to a vector of 5.0 see http://www.lri.fr/~hansen/cmaes_inmatlab.html
    # for more details about the rastrigin and other tests for CMA-ES
    strategy = cma.Strategy(centroid=vec_def[0:D], sigma=sigma, lambda_=pop_CMAES)
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
    start = time.time()
    algorithms.eaGenerateUpdate(toolbox1, ngen=ngen_CMAES, stats=stats, halloffame=hof)
    end = time.time()
    elapsed = end - start
    print(elapsed)
    # print "Best individual is %s, %s" % (hof[0], hof[0].fitness.values)
    # print(hof[0])
    # return hof[0].fitness.values[0]
    print(hof[0].fitness.values[0])
    return hof[0]

def main():
    start1 = time.time()
    arr = numpy.array([mycmaes() for i in range(0,reps_CMAES)]).transpose()
    end1 = time.time()
    elapsed1 = end1 - start1
    print(elapsed1)
    #re-adjust 'n' and 'tour'
    vec_def[2]*=L
    vec_def[3]*=pop_GA
    arr[2]*=L
    arr[3]*=pop_GA

    print("START",vec_def)
    print("FINAL",arr)
    print("MEAN",[numpy.mean(arr[i]) for i in range(0,len(arr))])
    print("STD",[numpy.std(arr[i]) for i in range(0,len(arr))])

if __name__ == "__main__":
    main()
