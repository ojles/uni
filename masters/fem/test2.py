#!./venv/bin/python3

from fem import FEM

def separate_point(a, b, c, na, nb, nc):
    result = []
    step_a = a / na
    step_b = b / nb
    step_c = c / nc

    for k in range(2 * nc + 1):
        if k % 2 == 0:
            for j in range(2 * nb + 1):
                if j % 2 == 0:
                    for i in range(2 * na + 1):
                        result.append([i * step_a / 2, j * step_b / 2, k * step_c / 2])
                else:
                    for i in range(na + 1):
                        result.append([i * step_a, j * step_b / 2, k * step_c / 2])
        else:
            for j in range(nb + 1):
                for i in range(na + 1):
                    result.append([i * step_a, j * step_b, k * step_c / 2])
    return result

def create_cube(a_start, a_end, b_start, b_end, c_start, c_end):
    a_size = a_end - a_start
    b_size = b_end - b_start
    c_size = c_end - c_start

    # x = [a_start, a_start + a_size / 2, a_end, a_start, a_end, a_start, a_start + a_size / 2, a_end, a_start,
    # a_end,
    #     a_start, a_end, a_start, a_start + a_size / 2, a_end, a_start, a_end, a_start, a_start + a_size / 2,
    #     a_end]
    # y = [b_start, b_start, b_start, b_start + b_size / 2, b_start + b_size / 2, b_end, b_end, b_end, b_start,
    #     b_start, b_end, b_end, b_start, b_start, b_start, b_start + b_size / 2, b_start + b_size / 2, b_end,
    #     b_end,
    #     b_end]
    # z = [c_start, c_start, c_start, c_start, c_start, c_start, c_start, c_start, c_start + c_size / 2,
    #    c_start + c_size / 2, c_start + c_size / 2, c_start + c_size / 2, c_end, c_end, c_end, c_end, c_end, c_end,
    #     c_end, c_end]

    x = [a_start,  # 1
         a_end,  # 2
         a_end,  # 3
         a_start,  # 4
         a_start,  # 5
         a_end,  # 6
         a_end,  # 7
         a_start,  # 8
         a_start + a_size / 2,  # 9
         a_end,  # 10
         a_start + a_size / 2,  # 11
         a_start,  # 12
         a_start,  # 13
         a_end,  # 14
         a_end,  # 15
         a_start,  # 16
         a_start + a_size / 2,  # 17
         a_end,  # 18
         a_start + a_size / 2,  # 19
         a_start  # 20
         ]
    y = [b_start,  # 1
         b_start,  # 2
         b_end,  # 3
         b_end,  # 4
         b_start,  # 5
         b_start,  # 6
         b_end,  # 7
         b_end,  # 8
         b_start,  # 9
         b_start + b_size / 2,  # 10
         b_end,  # 11
         b_start + b_size / 2,  # 12
         b_start,  # 13
         b_start,  # 14
         b_end,  # 15
         b_end,  # 16
         b_start,  # 17
         b_start + b_size / 2,  # 18
         b_end,  # 19
         b_start + b_size / 2  # 20
         ]
    z = [c_start,  # 1
         c_start,  # 2
         c_start,  # 3
         c_start,  # 4
         c_end,  # 5
         c_end,  # 6
         c_end,  # 7
         c_end,  # 8
         c_start,  # 9
         c_start,  # 10
         c_start,  # 11
         c_start,  # 12
         c_start + c_size / 2,  # 13
         c_start + c_size / 2,  # 14
         c_start + c_size / 2,  # 15
         c_start + c_size / 2,  # 16
         c_end,  # 17
         c_end,  # 18
         c_end,  # 19
         c_end  # 20
         ]
    result = []
    for i in range(20):
        result.append([x[i], y[i], z[i]])
    return result

def create_points(a, b, c, na, nb, nc):

    result = []

    step_a = a / na
    step_b = b / nb
    step_c = c / nc
    for k in range(nc):
        for j in range(nb):
            for i in range(na):
                cube = create_cube(i * step_a, (i + 1) * step_a,
                                        j * step_b, (j + 1) * step_b,
                                        k * step_c, (k + 1) * step_c)
                result.append(cube)

    return result

def NT_transform(akt, elem):
    result = []
    for cube in elem:
        nt_cube = []
        for i in cube:
            nt_cube.append(akt.index(i))
        result.append(nt_cube)
    return result

points = create_points(2,2,3,1,1,2)
akt = separate_point(2,2,3,1,1,2)
nt = NT_transform(akt, points)
print(points) 
print()
print(nt) 
print()

fem = FEM(2,2,3,1,1,2)
fem.mesh()
print(fem.NT)
