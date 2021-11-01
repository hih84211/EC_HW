#
# Binary tournament selection experiment
#
import random
from random import Random
import random
import matplotlib.pyplot as plt
import numpy as np

# A few useful constants
#
pop_size = 20
generations = 10
fit_range = 40

# Init the random number generator
#
prng = Random()
prng.seed(123)


# Let's suppose we have an imaginary problem that generates
# integer fitness values on some fixed range.  We'll start by randomly
# initializing a population of fitness values
#
pop = [prng.randrange(0, fit_range) for i in range(pop_size)]


# Helper function to plot histogram of population fitness values
#
def plt_hist(pop, generation=0, bin_limit=fit_range):
    plt.hist(pop, bins=range(0, bin_limit + 1))
    plt.grid(True)
    plt.title('Generation: ' + str(generation))
    plt.show()


# Binary tournament operator:
#  - Input: population of size N (pop_size)
#  - Output: new population of size N (pop_size), the result of applying selection
#
#  - Tournament pairs should be randomly selected
#  - All individuals from input population should participate in exactly 2 tournaments
#
def binary_tournament(pop_in, prng):
    newPop = []

    # 先將pop_in洗牌，再切割成兩兩一組，得到n輪對戰組合
    #
    random.shuffle(pop_in)
    tour1 = [pop_in[i:i + 2] for i in range(0, len(pop_in), 2)]
    random.shuffle(pop_in)
    tour2 = [pop_in[i:i + 2] for i in range(0, len(pop_in), 2)]

    for i in range(len(tour1)):
        # 把各個對戰組合排序後，pop出第一個就是最大的
        tour1[i].sort()
        tour2[i].sort()
        newPop.append(tour1[i].pop())
        newPop.append(tour2[i].pop())

    return newPop


# Let's iteratively apply our binary selection operator
# to the initial population and plot the resulting fitness histograms.
# This is somewhat like having a selection-only EA without any stochastic variation operators
#
for i in range(generations):
    print(pop)
    plt_hist(pop, i)

    pop = binary_tournament(pop, prng)
'''
rng = Random()
lst = [(rng.randint(0, 1023), rng.randint(0, 511)) for i in range(10)]
lst2 = [rng.randint(0, 100) for i in range(10)]
lst2.sort(reverse=True)
print(lst2)
print([lst2[i:i + 2] for i in range(0, len(lst2), 2)])
random.shuffle(lst2)
print([lst2[i:i + 2] for i in range(0, len(lst2), 2)])
'''