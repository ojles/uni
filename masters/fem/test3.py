#!./venv/bin/python3

# Verify that two types of for-loops produce the same
# indices

import numpy as np

idx1 = []
for j in range(60):
    for i in range(60):
        if i < 20:
            xyz_cord_i = 0
            i_for_NT = i
        elif 19 < i < 40:
            xyz_cord_i = 1
            i_for_NT = i - 20
        else:
            xyz_cord_i = 2
            i_for_NT = i - 40

        if j < 20:
            xyz_cord_j = 0
            j_for_NT = j
        elif 19 < j < 40:
            xyz_cord_j = 1
            j_for_NT = j - 20
        else:
            xyz_cord_j = 2
            j_for_NT = j - 40

        idx1.append([i, j, xyz_cord_i, xyz_cord_j, i_for_NT, j_for_NT])

idx2 = []
for j in range(60):
    for i in range(60):
        idx2.append([i, j, (i // 20), (j // 20), (i % 20), (j % 20)])

print((np.array(idx1) == np.array(idx2)).all())
