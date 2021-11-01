#
# Binary tournament selection experiment
#

from random import Random
import matplotlib.pyplot as plt

#A few useful constants
#
pop_size=20
generations=10
fit_range=40

#Init the random number generator
#
prng=Random()
prng.seed(123)


#Let's suppose we have an imaginary problem that generates
#integer fitness values on some fixed range.  We'll start by randomly
#initializing a population of fitness values
#
pop=[prng.randrange(0,fit_range) for i in range(pop_size)]


#Helper function to plot histogram of population fitness values
#
def plt_hist(pop, generation=0, bin_limit=fit_range):
    plt.hist(pop, bins=range(0,bin_limit+1))
    plt.grid(True)
    plt.title('Generation: ' + str(generation))
    plt.show()
    

#Binary tournament operator:
#  - Input: population of size N (pop_size)
#  - Output: new population of size N (pop_size), the result of applying selection
#
#  - Tournament pairs should be randomly selected
#  - All individuals from input population should participate in exactly 2 tournaments
#    
def binary_tournament(pop_in, prng):
    newPop=[]
    
    #
    #It's your job to implement this binary tournament function!
    #
    
    # return newPop    
    return newPop    


#Let's iteratively apply our binary selection operator
# to the initial population and plot the resulting fitness histograms.
# This is somewhat like having a selection-only EA without any stochastic variation operators
#
for i in range(generations):
    print(pop)
    plt_hist(pop,i)
    
    pop=binary_tournament(pop, prng)

  
