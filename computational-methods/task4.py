import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as itg


def rectangle_formula(a, b, n):
    h = (b - a) / n
    xi = a + 0.5 * h
    res = 0
    for _ in range(0, n):
        res += f(xi)
        xi += h
    return res * h


def trapezium_formula(a, b, n):
    h = (b - a) / n
    xi = a + h
    res = 0
    for _ in range(1, n):
        res += f(xi)
        xi += h
    return (h / 2) * (f(a) + f(b)) + res * h


def simps_formula(a, b, n):
    h = (b - a) / n

    xi, sum1 = (a + h, 0)
    for i in range(1, n):
        sum1 += f(xi)
        xi += h

    xi, sum2 = (a + h / 2, 0)
    for i in range(1, n + 1):
        sum2 += f(xi)
        xi += h

    return (h / 6) * (f(a) + f(b) + 2 * sum1 + 4 * sum2)


def gauss_formula(a, b, n):
    if n == 4:
        t = [0.861136, 0.339981, -0.339981, -0.861136]
        C = [0.347855, 0.652145, 0.652145, 0.347855]
    elif n == 5:
        t = [0.90618, 0.538469, 0, -0.538469, -0.90618]
        C = [0.23693, 0.47863, 0.56889, 0.47863, 0.23693]
    else:
        raise Exception("Invalid n value (" + n + ")")

    res = 0
    ab_avg = (b + a) / 2
    ab_delta_div_2 = (b - a) / 2
    for i in range(len(t)):
        xi = ab_avg + ab_delta_div_2 * t[i]
        res += C[i] * f(xi)
    return res * ab_delta_div_2


def f(x):
    return x ** 3


def main():
    a = 0
    b = 2
    n = 20

    print('Expected: ', itg.quad(f, a, b)[0])
    print('Rectangle formula: ', rectangle_formula(a, b, n))
    print('Trapezium formula: ', trapezium_formula(a, b, n))
    print('Simps formula: ', simps_formula(a, b, n))
    print('Gauss formula (n=4) formula: ', gauss_formula(a, b, 4))
    print('Gauss formula (n=5) formula: ', gauss_formula(a, b, 5))

    x = []
    y = []
    for val in np.linspace(a, b, n):
        x.append(val)
        y.append(f(val))

    plt.plot(x, y, linestyle='dashed', color='green')


main()
