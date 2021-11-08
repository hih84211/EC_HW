#
# ev3.py: An elitist (mu+mu) generational-with-overlap EA
#
#
# To run: python ev3.py --input ev3_example.cfg
#         python ev3.py --input my_params.cfg
#
# Basic features of ev3:
#   - Supports self-adaptive mutation
#   - Uses binary tournament selection for mating pool
#   - Uses elitist truncation selection for survivors
#

import optparse
import sys
import yaml
import math
from random import Random
import copy
from Population import *
import numpy as np


# EV3 Config class
class EV3_Config:
    """
    EV3 configuration class
    """
    # class variables
    sectionName = 'EV3'
    options = {'populationSize': (int, True),
               'generationCount': (int, True),
               'randomSeed': (int, True),
               'crossoverFraction': (float, True),
               'minLimit': (float, True),
               'maxLimit': (float, True),
               'selfEnergyVector': (list, True),
               'interactionEnergyMatrix': (list, True),
               'latticeLength': (int, True),
               'numParticleTypes': (int, True),
               'dimension': (int, True)}

    # constructor
    def __init__(self, inFileName):
        # read YAML config and get EV3 section
        infile = open(inFileName, 'r')
        ymlcfg = yaml.safe_load(infile)
        infile.close()
        eccfg = ymlcfg.get(self.sectionName, None)
        if eccfg is None: raise Exception('Missing {} section in cfg file'.format(self.sectionName))

        # iterate over options
        for opt in self.options:
            if opt in eccfg:
                optval = eccfg[opt]

                # verify parameter type
                if type(optval) != self.options[opt][0]:
                    raise Exception('Parameter "{}" has wrong type'.format(opt))

                # create attributes on the fly
                setattr(self, opt, optval)
            else:
                if self.options[opt][1]:
                    raise Exception('Missing mandatory parameter "{}"'.format(opt))
                else:
                    setattr(self, opt, None)

    # string representation for class data
    def __str__(self):
        return str(yaml.dump(self.__dict__, default_flow_style=False))


# Simple fitness function example: 1-D Rastrigin function
#
def fitnessFunc(x):
    return -10.0 - (0.04 * x) ** 2 + 10.0 * math.cos(0.04 * math.pi * x)

# Energy evaluate function
def total_engergy(lattice, u, t):
    u = u
    t = t
    size = len(lattice)
    self_eng = 0
    mut_eng = 0
    for i in range(size):
        self_eng += u[lattice[i]]
        if i > 0:
            mut_eng += t[lattice[i-1]][lattice[i]]
        if i < (size - 1):
            mut_eng += t[lattice[i]][lattice[i+1]]
    return self_eng + mut_eng


# Multi-variable function
def multi_dimension_fit_func(x):
    # return -10.0 - (0.04*np.square(x) + 10.0 * np.cos(0.04 * np.pi * x)).sum()
    return 10 * x.size + (np.square(x) - 10 * np.cos(2 * np.pi * x)).sum()


# Print some useful stats to screen
# 可由minmax參數選擇呈現最大值或最小值
def printStats(minmax, pop, gen):
    print('Generation:', gen)
    avgval = 0
    mval = pop[0].fit
    sigma = pop[0].sigma
    if minmax == 0:
        for ind in pop:
            avgval += ind.fit
            if ind.fit < mval:
                mval = ind.fit
                sigma = ind.sigma
            print(ind)
        print('Min fitness', mval)
    elif minmax == 1:
        for ind in pop:
            avgval += ind.fit
            if ind.fit > mval:
                mval = ind.fit
                sigma = ind.sigma
            print(ind)
        print('Max fitness', mval)

    print('Sigma', sigma)
    print('Avg fitness', avgval / len(pop))
    print('')


# EV3 for problem1:
def ev3_problem1(cfg):
    # start random number generators
    uniprng = Random()
    uniprng.seed(cfg.randomSeed)
    normprng = Random()
    normprng.seed(cfg.randomSeed + 101)

    # set static params on classes
    # (probably not the most elegant approach, but let's keep things simple...)
    Lattice.selfEnergyVector = cfg.selfEnergyVector
    Lattice.interactionEnergyMatrix = cfg.interactionEnergyMatrix
    Lattice.latticeLength = cfg.latticeLength
    Lattice.numParticleTypes = cfg.numParticleTypes
    Lattice.fitFunc = total_engergy
    Lattice.uniprng = uniprng
    Lattice.normprng = normprng
    Population.uniprng = uniprng
    Population.crossoverFraction = cfg.crossoverFraction

    # create initial Population (random initialization)
    # 額外加入problem_num 以及minmax兩參數：
    # problem_num用以選擇執行作業中的problem 1或2
    # minmax用以決定所求得極值為最大值或最小值
    population = Population(populationSize=cfg.populationSize, problem_num=1, minmax=0)

    # print initial pop stats
    printStats(minmax=0, pop=population, gen=0)

    # evolution main loop
    for i in range(cfg.generationCount):
        # create initial offspring population by copying parent pop
        offspring = copy.deepcopy(population)

        # select mating pool
        offspring.conductTournament()

        # perform crossover
        offspring.crossover()

        # random mutation
        offspring.mutate()

        # update fitness values
        #print(offspring.population)
        offspring.evaluateFitness()

        # survivor selection: elitist truncation using parents+offspring
        population.combinePops(offspring)
        population.truncateSelect(cfg.populationSize)

        # print population stats
        printStats(minmax=0, pop=population, gen=i + 1)


# EV3 for problem2:
def ev3_problem2(cfg):
    # start random number generators
    uniprng = Random()
    uniprng.seed(cfg.randomSeed)
    normprng = Random()
    normprng.seed(cfg.randomSeed + 101)

    # set static params on classes
    # (probably not the most elegant approach, but let's keep things simple...)
    ND_Individual.dimension = cfg.dimension
    ND_Individual.minLimit = cfg.minLimit
    ND_Individual.maxLimit = cfg.maxLimit
    ND_Individual.fitFunc = multi_dimension_fit_func
    ND_Individual.uniprng = uniprng
    ND_Individual.normprng = normprng
    Population.uniprng = uniprng
    Population.crossoverFraction = cfg.crossoverFraction

    minmax = 0

    # create initial Population (random initialization)
    population = Population(populationSize=cfg.populationSize, problem_num=2, minmax=minmax)

    # print initial pop stats
    printStats(minmax=minmax, pop=population, gen=0)

    # evolution main loop
    for i in range(cfg.generationCount):
        # create initial offspring population by copying parent pop
        offspring = copy.deepcopy(population)

        # select mating pool
        offspring.conductTournament()

        # perform crossover
        offspring.crossover()

        # random mutation
        offspring.mutate()

        # update fitness values
        #print(offspring.population)
        offspring.evaluateFitness()

        # survivor selection: elitist truncation using parents+offspring
        population.combinePops(offspring)
        population.truncateSelect(cfg.populationSize)

        # print population stats
        printStats(minmax=minmax, pop=population, gen=i + 1)


#
# Main entry point
#
#
def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        #
        # get command-line options
        #
        parser = optparse.OptionParser()
        parser.add_option("-i", "--input", action="store", dest="inputFileName", help="input filename", default=None)
        parser.add_option("-q", "--quiet", action="store_true", dest="quietMode", help="quiet mode", default=False)
        parser.add_option("-d", "--debug", action="store_true", dest="debugMode", help="debug mode", default=False)
        (options, args) = parser.parse_args(argv)

        # validate options
        if options.inputFileName is None:
            raise Exception("Must specify input file name using -i or --input option.")

        # Get EV3 config params
        cfg = EV3_Config(options.inputFileName)


        # print config params
        print(cfg)

        '''
            Problem 1 & Problem 2 分別由 ev3_problem1(cfg) 和 ev3_problem2(cfg)執行
        '''
        ev3_problem1(cfg)

        if not options.quietMode:
            print('Combinatorial energy minimization Completed!')

        ev3_problem2(cfg)

        if not options.quietMode:
            print('Multi-variate real-number upgrade Completed!')

    except Exception as info:
        if 'options' in vars() and options.debugMode:
            from traceback import print_exc
            print_exc()
        else:
            print(info)


if __name__ == '__main__':
    # Problem 1 & 2已包在main()中，並共用同一個.cfg檔案
    main(['-i', 'ev3_example.cfg', '-d'])

