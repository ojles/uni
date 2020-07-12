import math

import matplotlib.pyplot as plt
import numpy as np


def solve(a, b, alpha, beta, A, B, n):
    h = (b - a) / n
    x = [(a + i * h) for i in range(n + 1)]

    C = [[0 for x in range(n + 1)] for _ in range(n + 1)]
    d = [i for i in range(n + 1)]

    C[0][0] = alpha[0] * h - alpha[1]
    C[0][1] = alpha[1]
    C[n][n - 1] = -beta[1]
    C[n][n] = beta[0] * h + beta[1]

    for i in range(1, n):
        C[i][i - 1] = 1 - h * p(x[i]) / 2
        C[i][i] = (h ** 2) * q(x[i]) - 2
        C[i][i + 1] = 1 + h * p(x[i]) / 2

    d[0] = A * h
    d[n] = B * h
    for i in range(1, n):
        d[i] = f(x[i]) * (h ** 2)

    y = np.linalg.solve(C, d)
    return x, y


def p(x):
    return 1


def q(x):
    return 1


def f(x):
    return math.cos(x)


def main():
    a, b = (0, 2 * math.pi)
    alpha, beta = ([1, 0], [1, 0])
    A, B = (0, 0)
    n = 40

    x, y = solve(a, b, alpha, beta, A, B, n)

    # for i in range(n + 1):
    #     print(x[i], "   ", y[i])

    x_real = np.linspace(a, b, n)
    y_real = [(0.5 * (np.log(x_real[i])) ** 2) for i in range(n)]

    # plt.plot(x_real, y_real, "y")
    plt.plot(x, y, "bo")

    plt.show()


main()
