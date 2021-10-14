from random import Random
from matplotlib import pyplot as plt
import numpy as np

class my_class:
    d1 = 1000
    d2 = 200
    def __init__(self):
        self.print_val()

    def print_val(self):
        print('d1: ', self.d1)
        print('d2: ', self.d2)

    def get_vla(self):
        return self.d1, self.d2

    def set_val(self, d1, d2):
        self.d1 = d1
        self.d2 = d2


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def super_SiBaLa(dice, side, trial):
    if trial < 1:
        print("You'll have to roll the dice at least once.")
        return None
    if side < 3:
        print("Invalid dice.")
        return None
    if dice < 1:
        print("You'll need at least one die.")
        return None
    prng = Random()
    prng.seed(797)
    total = np.full(trial, 0)
    for i in range(dice):
        tmp = np.array([prng.randint(1, side) for i in range(trial)])
        print(tmp)
        total += tmp
    return total


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    prng = Random()
    prng.seed(797)
    '''uni_list = list(prng.uniform(.0, 1.) for i in range(10000))
    normal_list = list(prng.gauss(mu=5., sigma=2.) for i in range(10000))
    # print(random_list)
    n, bins, patches = plt.hist(uni_list, bins=50, density=True, facecolor='g')
    plt.axis([0, 1, 0, 2])
    plt.title('Uniform distribution')
    plt.show()

    n, bins, patches = plt.hist(normal_list, bins=50, density=True, facecolor='g')
    plt.title('Normal distribution')
    plt.show()'''
    print(super_SiBaLa(2, 6, 50))
#[5 4 2 1 4 5 4 5 1 6 3 3 6 4 1 5 3 3 5 1 5 1 2 2 1 3 4 3 1 4 4 2 2 3 5 5 3 1 3 6 6 3 3 5 5 5 3 3 1 3]



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
