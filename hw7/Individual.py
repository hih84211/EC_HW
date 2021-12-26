#
# Individual.py
#
#

import math
import numpy as np

# A simple 1-D Individual class
class Individual:
    """
    Individual
    """
    minSigma = 1e-100
    maxSigma = 1
    learningRate = 1
    minLimit = None
    maxLimit = None
    uniprng = None
    normprng = None
    fitFunc = None

    def __init__(self):
        self.x = self.uniprng.uniform(self.minLimit, self.maxLimit)
        self.fit = self.__class__.fitFunc(self.x)
        self.sigma = self.uniprng.uniform(0.9, 0.1)  # use "normalized" mutRate
        
    def crossover(self, other):
        # perform crossover "in-place"
        alpha = self.uniprng.random()

        tmp = self.x*alpha+other.x*(1-alpha)
        other.x = self.x*(1-alpha)+other.x*alpha
        self.x = tmp
        
        self.fit = None
        other.fit = None
    
    def mutate(self):
        self.sigma = self.sigma*math.exp(self.learningRate*self.normprng.normalvariate(0, 1))
        if self.sigma < self.minSigma:
            self.sigma = self.minSigma
        if self.sigma > self.maxSigma:
            self.sigma = self.maxSigma

        self.x = self.x+(self.maxLimit-self.minLimit)*self.sigma*self.normprng.normalvariate(0, 1)
        self.fit = None
    
    def evaluateFitness(self):
        if self.fit == None:
            self.fit = self.__class__.fitFunc(self.x)
        
    def __str__(self):
        return '%0.8e' % self.x+'\t'+'%0.8e' % self.fit+'\t'+'%0.8e' % self.sigma


# Individual of problem 1
# 由於Lattice也是種Individual，有許多相似之處，於是讓前者繼承後者
class Lattice(Individual):
    latticeLength = None
    selfEnergyVector = None
    interactionEnergyMatrix = None
    numParticleTypes = None

    def __init__(self):
        self.x = [self.uniprng.randint(0, self.numParticleTypes-1) for i in range(self.latticeLength)]
        self.fit = self.__class__.fitFunc(self.x, self.selfEnergyVector, self.interactionEnergyMatrix)
        self.sigma = self.uniprng.uniform(0.9, 0.1)

    def crossover(self, other):
        alpha = int(self.uniprng.random()*self.latticeLength)
        tmp1 = self.x[:alpha]
        tmp2 = other.x[alpha:]
        tmp1.extend(tmp2)
        self.x = tmp1
        self.fit = None
        other.fit = None
        # print('After cross: ', self.x)

    # 非 self-adaptive
    def mutate(self):
        self.sigma = self.sigma*math.exp(self.learningRate*self.normprng.normalvariate(0, 1))
        if self.sigma < self.minSigma:
            self.sigma = self.minSigma
        if self.sigma > self.maxSigma:
            self.sigma = self.maxSigma

        for i in range(self.latticeLength):
            # print('individual: ', self.x)
            # 突變，while迴圈為避免突變回自己
            if self.sigma > self.uniprng.random():
                tmp = self.uniprng.randint(0, self.numParticleTypes-1)
                while tmp == self.x[i]:
                    tmp = self.uniprng.randint(0, self.numParticleTypes-1)
                self.x[i] = tmp
        self.fit = None

    def evaluateFitness(self):
        if self.fit == None:
            self.fit = self.__class__.fitFunc(self.x, self.selfEnergyVector, self.interactionEnergyMatrix)

    def __str__(self):
        return self.x.__str__()+'\t'+'%d' % self.fit+'\t'+'%0.8e' % self.sigma


# Individual of problem 2
# 使用numpy_array可簡單的將1-D individual改寫成N-D individual
class ND_Individual(Individual):
    dimension = 1

    def __init__(self):
        self.x = np.array([self.uniprng.uniform(self.minLimit, self.maxLimit) for i in range(self.dimension)])
        self.fit = self.__class__.fitFunc(self.x)
        self.sigma = self.uniprng.uniform(0.9, 0.1)  # use "normalized" mutRate

    def __str__(self):
        return self.x.__str__()+'\t'+'%0.8e' % self.fit+'\t'+'%0.8e' % self.sigma
