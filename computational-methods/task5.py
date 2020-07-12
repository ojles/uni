import math

import matplotlib.pyplot as plt
import numpy as np


def f(x, y):
    return x + math.cos(y / 2.2)


def fun_an(x):
    return 2 * math.exp(x) - x - 1


def eiler(f, a, b, y0, n):
    h = (b - a) / n
    x = [k for k in range(n + 1)]
    y = [k for k in range(n + 1)]
    x[0] = a
    y[0] = y0
    for i in range(n):
        x[i + 1] = x[i] + h
        ypr = y[i] + h / 2 * f(x[i], y[i])
        y[i + 1] = y[i] + h * f(x[i] + h / 2, ypr)

    return x, y


def kut(f, a, b, y0, n):
    h = (b - a) / n
    x = [k for k in range(n + 1)]
    y = [k for k in range(n + 1)]
    x[0] = a
    y[0] = y0
    for i in range(n):
        x[i + 1] = x[i] + h
        k1 = h * f(x[i], y[i])
        k2 = h * f(x[i] + h / 2, y[i] + k1 / 2)
        k3 = h * f(x[i] + h / 2, y[i] + k2 / 2)
        k4 = h * f(x[i] + h, y[i] + k3)
        y[i + 1] = y[i] + 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return x, y


def met_adam_bosh(fun, a, b, y0, n):
    h = (b - a) / n
    x = [x for x in range(n + 1)]
    y = [x for x in range(n + 1)]
    f = [x for x in range(n + 1)]
    x[0] = a
    y[0] = y0
    f[0] = fun(x[0], y[0])
    for i in range(3):
        x[i + 1] = x[i] + h
        k1 = h * f[i]
        k2 = h * fun(x[i] + h / 2, y[i] + k1 / 2)
        k3 = h * fun(x[i] + h / 2, y[i] + k2 / 2)
        k4 = h * fun(x[i] + h, y[i] + k3)
        y[i + 1] = y[i] + 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        f[i + 1] = fun(x[i + 1], y[i + 1])
    for i in range(3, n):
        x[i + 1] = x[i] + h
        y[i + 1] = y[i] + h / 24 * (55 * f[i] - 59 * f[i - 1] +
                                    37 * f[i - 2] - 9 * f[i - 3])
        f[i + 1] = fun(x[i + 1], y[i + 1])
    return x, y


def met_adam_multon(fun, a, b, y0, n):
    h = (b - a) / n
    x = [x for x in range(n + 1)]
    y = [x for x in range(n + 1)]
    f = [x for x in range(n + 1)]
    x[0] = a
    y[0] = y0
    f[0] = fun(x[0], y[0])
    for i in range(3):
        x[i + 1] = x[i] + h
        k1 = h * f[i]
        k2 = h * fun(x[i] + h / 2, y[i] + k1 / 2)
        k3 = h * fun(x[i] + h / 2, y[i] + k2 / 2)
        k4 = h * fun(x[i] + h, y[i] + k3)
        y[i + 1] = y[i] + 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        f[i + 1] = fun(x[i + 1], y[i + 1])
    for i in range(3, n):
        x[i + 1] = x[i] + h
        ypred = y[i] + h / 24 * (55 * f[i] - 59 * f[i - 1] +
                                 37 * f[i - 2] - 9 * f[i - 3])
        fpred = fun(x[i + 1], ypred)
        y[i + 1] = y[i] + h / 24 * (9 * fpred + 19 * f[i] - 5 * f[i - 1] + f[i - 2])
        f[i + 1] = fun(x[i + 1], y[i + 1])
    return x, y


def main():
    a = 1.8
    b = 2.8
    y0 = 2.6
    n = 30
    x1, y1 = eiler(f, a, b, y0, n)
    print(x1)
    print(y1)

    x2, y2 = kut(f, a, b, y0, n)
    print(x2)
    print(y2)

    x3, y3 = met_adam_multon(f, a, b, y0, n)
    print(x3)
    print(y3)

    x4, y4 = met_adam_bosh(f, a, b, y0, n)
    print(x4)
    print(y4)
    x0 = np.linspace(x1[0], x1[n])
    y0 = list()
    for i in x0:
        y0.append(fun_an(i))
    plt.plot(x1, y1, color="blue", lw=0.5)
    plt.plot(x2, y2, color="red", lw=0.5)
    plt.plot(x3, y3, color="black", lw=0.5)
    plt.plot(x4, y4, color="yellow", lw=0.5)

    plt.show()


main()
