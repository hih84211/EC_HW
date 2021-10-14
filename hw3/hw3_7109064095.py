from random import Random
import numpy as np
import matplotlib.pyplot as plt


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
    p = Random()
    # prng.seed(797)
    total = np.full(trial, 0)
    for i in range(dice):
        tmp = np.array([p.randint(1, side) for i in range(trial)])
        # print(tmp)
        total += tmp
    return total


if __name__=='__main__':
    prng = Random()
    # prng.seed(797)
    uni_list = list(prng.uniform(.0, 1.) for i in range(10000))
    normal_list = list(prng.gauss(mu=5., sigma=2.) for i in range(10000))
    # print(random_list)
    plt.hist(uni_list, bins=50, density=True, facecolor='g')
    plt.axis([0, 1, 0, 2])
    plt.title('Uniform distribution')
    plt.show()
    
    plt.hist(normal_list, bins=50, density=True, facecolor='g')
    plt.title('Normal distribution')
    plt.show()

    # 2d6 1d12 2d10 1d20

    dd6 = super_SiBaLa(dice=2, side=6, trial=10000)
    d12 = super_SiBaLa(1, 12, 10000)
    dd10 = super_SiBaLa(2, 10, 10000)
    d20 = super_SiBaLa(1, 20, 10000)

    if dd6 is not None:
        plt.hist(dd6, bins=50, density=True, facecolor='g')
        plt.title('2D6')
        plt.show()

    if d12 is not None:
        plt.hist(d12, bins=50, density=True, facecolor='g')
        plt.title('1D12')
        plt.show()

    if dd6 is not None:
        plt.hist(dd6, bins=50, density=True, facecolor='g')
        plt.title('2D10')
        plt.show()

    if d20 is not None:
        plt.hist(d20, bins=50, density=True, facecolor='g')
        plt.title('1D20')
        plt.show()

