import math

import matplotlib.pyplot as plt
import numpy as np


class LeastSquares:
    def __init__(self, a, b, n, m, func):
        if a >= b:
            raise Exception("Invalid a,b values (a is more than b)")

        self.n = n
        self.m = m
        self.__calculate_a(a, b, func)

    @staticmethod
    def __phi(x, i):
        return math.pow(x, i)

    def __phi_k_phi_j(self, k, j, x):
        res = 0
        for i in range(self.n + 1):
            res += self.__phi(x[i], k) * self.__phi(x[i], j)
        return res

    def __f_phi_j(self, func, j, x):
        res = 0
        for i in range(self.n + 1):
            res += func(x[i]) * self.__phi(x[i], j)
        return res

    def __calculate_a(self, a, b, func):
        x = np.linspace(a, b, self.n + 1)
        matrix = [[0.0 for _ in range(self.m + 1)] for _ in range(self.m + 1)]
        for j in range(self.m + 1):
            for k in range(self.m + 1):
                matrix[j][k] = self.__phi_k_phi_j(k, j, x)

        res = []
        for j in range(self.m + 1):
            res.append(self.__f_phi_j(func, j, x))

        self.a = np.linalg.solve(matrix, res)

    def calc(self, x):
        res = 0
        for i in range(self.m + 1):
            res += self.a[i] * self.__phi(x, i)
        return res


def f(x):
    return x ** 2


def main():
    a, b, n, m = (-2, 2, 4, 1)
    N = n * 10

    ls = LeastSquares(a, b, n, m, f)

    x = [i for i in np.linspace(a, b, N)]

    y = [f(i) for i in x]
    plt.plot(x, y, linestyle='dashed', color='green')

    y = [ls.calc(i) for i in x]
    plt.plot(x, y)

    plt.show()


main()
