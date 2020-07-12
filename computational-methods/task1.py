import math


def secant_method(a, b, e):
    if check_a(a, b):
        def calc_next(_x):
            return x - (f(_x) / (f(b) - f(_x))) * (b - _x)
    else:
        def calc_next(_x):
            return a - (f(a) / (f(x) - f(a))) / (_x - a)

    x = 0
    next_x = calc_next(x)
    while abs(next_x - x > e):
        x = next_x
        next_x = calc_next(x)

    return next_x


def newtons_method(a, b, e):
    def calc_next(xx):
        return xx - (f(xx) / df(xx))

    x = a if check_a(a, b) else b
    next_x = calc_next(x)
    while abs(next_x - x) > e:
        x = next_x
        next_x = calc_next(x)

    return next_x


def combined_method(a, b, e):
    x = 0
    xx = 0
    next_x = a
    next_xx = b

    if check_a(a, b):
        def calc_next_x():
            return x - (f(x) / df(x))

        def calc_next_xx():
            return x - (f(x) / (f(xx) - f(x))) * (xx - x)

        def check():
            return abs(next_x - x) > e
    else:
        def calc_next_x():
            return x - (f(x) / (f(xx) - f(x))) * (xx - x)

        def calc_next_xx():
            return xx - (f(xx) / f(x))

        def check():
            return abs(x - xx) > e

    while check():
        x = next_x
        xx = next_xx
        next_x = calc_next_x()
        next_xx = calc_next_xx()

    return next_x


def f(x):
    return x * x * x + 2 * x - 1


def df(x):
    return 3 * x * x + 2


def ddf(x):
    return 6 * x


def check_a(a, b):
    for i in range(a, b + 1):
        if f(b) * ddf(i) <= 0:
            return False
    return True


def newtons_method_for_system(e):
    def _f(_x, _y):
        return math.cos(_x - 1) + _y - 0.5

    def _g(_x, _y):
        return _x - math.cos(_y) - 3

    def dx_f(_x, _y):
        return -math.sin(_x - 1) + _y

    def dy_f(_x, _y):
        return math.cos(_x - 1) + 1

    def dx_g(_x, _y):
        return 1 - math.cos(_y)

    def dy_g(_x, _y):
        return _x + math.sin(_y)

    def det(a, b, c, d):
        return a * c - b * d

    def delta_n(_xn, _yn):
        return det(
            dx_f(_xn, _yn), dy_f(_xn, _yn),
            dx_g(_xn, _yn), dy_g(_xn, _yn)
        )

    def delta_xn(_xn, _yn):
        return -det(
            _f(_xn, _yn), dy_f(_xn, _yn),
            _g(_xn, _yn), dy_g(_xn, _yn)
        )

    def delta_yn(_xn, _yn):
        return det(
            _f(_xn, _xn), dx_f(_xn, _xn),
            _g(_xn, _xn), dx_g(_xn, _xn)
        )

    def calc_next_x(_x, _y):
        return _x + delta_xn(_x, _y) / delta_n(_x, _y)

    def calc_next_y(_x, _y):
        return _y + delta_yn(_x, _y) / delta_n(_x, _y)

    x, y = 1, 1
    x_next, y_next = calc_next_x(x, y), calc_next_y(x, y)
    while abs(x - x_next) > e and abs(y - y_next) > e:
        x, y = x_next, y_next
        x_next, y_next = calc_next_x(x, y), calc_next_y(x, y)

    return x, y


def main():
    print('Secant method: ', secant_method(1, 3, 0.0001))
    print('Newton\'s method: ', newtons_method(1, 3, 0.0001))
    print('Combined method: ', combined_method(1, 3, 0.0001))
    print('Newton\'s method for systems: ', newtons_method_for_system(0.0001))


main()
