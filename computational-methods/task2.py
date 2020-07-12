import math

import matplotlib.pyplot as plt


class Interpolation:
    def __init__(self, a, b, n, func):
        if a >= b:
            raise Exception("Invalid a,b values (a is more than b)")

        self.n = n + 1
        h = (b - a) / n

        self.x = [0 for i in range(self.n)]
        self.m = [[0 for i in range(self.n)] for j in range(self.n)]
        for i in range(self.n):
            x = a + i * h
            self.x[i] = x
            self.m[i][0] = func(x)


class NewtonBackward(Interpolation):
    def __init__(self, a, b, n, func):
        Interpolation.__init__(self, a, b, n, func)

        # calculate delta matrix
        for i in range(1, self.n):
            for j in range(self.n - 1, i - 1, -1):
                self.m[j][i] = self.m[j][i - 1] - self.m[j - 1][i - 1]

    @staticmethod
    def __calc_q(q, n):
        res = q
        for i in range(1, n):
            res *= (q + i)
        return res

    def __delta_y(self, n):
        return self.m[self.n - 1][n]

    def calc(self, x):
        res = self.m[self.n - 1][0]
        q = (x - self.x[self.n - 1]) / (self.x[1] - self.x[0])
        for i in range(1, self.n):
            res += (self.__calc_q(q, i) * self.__delta_y(i)) / math.factorial(i)
        return res


class GaussForward(Interpolation):
    def __init__(self, a, b, n, func):
        Interpolation.__init__(self, a, b, n, func)
        if self.n % 2 == 0:
            raise Exception("The number of steps should be an odd number")

        # calculate delta matrix
        for i in range(1, self.n):
            for j in range(self.n - i):
                self.m[j][i] = self.m[j + 1][i - 1] - self.m[j][i - 1]

    @staticmethod
    def __calc_q(q, n):
        res = q
        d = 1
        for i in range(1, n):
            if i % 2 == 1:
                res *= q - d
            else:
                res *= (q + d)
                d += 1
        return res

    def __delta_y(self, n):
        return self.m[self.n // 2 - (n // 2)][n]

    def calc(self, x):
        res = self.m[self.n // 2][0]
        q = (x - self.x[self.n // 2]) / (self.x[1] - self.x[0])
        for i in range(1, self.n):
            res += (self.__calc_q(q, i) * self.__delta_y(i)) / math.factorial(i)
        return res


def f(x):
    return (x / 2 + 1) * math.sin(x)


def main():
    nb = NewtonBackward(1, 3, 2, f)
    gf = GaussForward(1, 3, 2, f)

    print("Real value: ", f(2.3))
    print("Newton backward algorithm: ", nb.calc(2.3))
    print("Gauss forward algorithm: ", gf.calc(2.3))

    x = []
    y = []
    for i in range(10, 31, 1):
        x.append(i / 10)
        y.append(f(i / 10))

    plt.plot(x, y, linestyle='dashed', color='green')

    for i in range(10, 31, 1):
        x[i - 10] = (i / 10)
        y[i - 10] = (nb.calc(i / 10))

    plt.plot(x, y)
    plt.show()


main()
