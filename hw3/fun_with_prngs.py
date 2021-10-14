#Generates sequences of random numbers
# with various pdf's and then uses matplotlib
# to plot histograms of results

import random
import matplotlib.pyplot as plt

trials=10000
seed=123

#Create PRNG object and set initial seed
prng=random.Random()
prng.seed(seed)

#
#Uniform distribution on [0,1]
#
randnums=[]
for i in range(trials):
    randnums.append(prng.uniform(0.0,1.0))

#Plot the histogram of the data
plt.hist(randnums, 50, density=True, facecolor='green', alpha=0.75)
plt.grid(True)
plt.title("Uniform Distribution")
plt.show()

#
#Gaussian (normal) distribution
#
mu=5
sigma=2
randnums=[]
for i in range(trials):
    randnums.append(prng.normalvariate(mu,sigma))

#Plot the histogram of the data
plt.hist(randnums, 50, density=True, facecolor='green', alpha=0.75)
plt.grid(True)
plt.title("Gaussian Distribution")
plt.show()

#
#Dice-roll generator
#
dice_sets=[(2,6),(1,12),(2,10),(1,20)]
for dice in dice_sets:
    n_sides=dice[1]
    m_rolls=dice[0]
    randnums=[]
    for i in range(trials):
        total=0
        for j in range(m_rolls):
            total+=prng.randint(1,n_sides)
        randnums.append(total)
    
    #Plot the histogram of the data
    plt.hist(randnums, bins=range(m_rolls,m_rolls*n_sides+2), density=True, facecolor='green', alpha=0.75)
    plt.grid(True)
    plt.title(str(dice[0])+'d'+str(dice[1]))
    plt.show()