#
# Individual.py
#
#

import math

#A simple 1-D Individual class
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
        self.sigma = self.uniprng.uniform(0.9, 0.1)  # use "normalized" sigma
        
    def crossover(self, other):
        # perform crossover "in-place"
        alpha = self.uniprng.random()

        tmp = self.x*alpha+other.x*(1-alpha)
        other.x = self.x*(1-alpha)+other.x*alpha
        self.x = tmp
        
        self.fit = None
        other.fit = None
    
    def mutate(self):
        self.sigma=self.sigma*math.exp(self.learningRate*self.normprng.normalvariate(0,1))
        if self.sigma < self.minSigma: self.sigma=self.minSigma
        if self.sigma > self.maxSigma: self.sigma=self.maxSigma

        self.x=self.x+(self.maxLimit-self.minLimit)*self.sigma*self.normprng.normalvariate(0,1)
        self.fit=None
    
    def evaluateFitness(self):
        if self.fit == None: self.fit=self.__class__.fitFunc(self.x)
        
    def __str__(self):
        return '%0.8e'%self.x+'\t'+'%0.8e'%self.fit+'\t'+'%0.8e'%self.sigma


class Lattice(Individual):
    def __init__(self, particles=None):
        super().__init__()
        self.x = particles

    def crossover(self, other):
        alpha = int(self.uniprng.random()*len(other))
        tmp1 = self.x[:alpha]
        tmp2 = other.x[alpha:]
        self.x = tmp1.extend(tmp2)

    # 非 self-adaptive
    def mutate(self):
        self.sigma = self.sigma * math.exp(self.learningRate * self.normprng.normalvariate(0, 1))
        if self.sigma < self.minSigma:
            self.sigma = self.minSigma
        if self.sigma > self.maxSigma:
            self.sigma = self.maxSigma

        for i in self.x:
            # 要避免突變回自己
            if self.sigma > self.uniprng.random():
                i = self.uniprng.randint(0, 2)