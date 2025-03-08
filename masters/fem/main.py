#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def set_axes_equal(ax):
    """
    Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    """

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])


ax = 2
ay = 1
az = 2

nx = 2
ny = 1
nz = 2

nel = nx * ny * nz

#
# Generate AKT
#
AKT = []
AKTr = np.zeros((nx * 2 + 1, ny * 2 + 1, nz * 2 + 1)).astype(int)
idx = 1
for iz in range(nz * 2 + 1):
    y_step = 1 + (iz % 2)
    for iy in range(0, ny * 2 + 1, y_step):
        x_step = 1 + ((iy + iz) % 2)
        for ix in range(0, nx * 2 + 1, x_step):
            AKT.append((ix/2, iy/2, iz/2))
            AKTr[ix][iy][iz] = idx
            idx = idx + 1


#
# After AKT is done we can calculate following values:
#    - nqp
#    - ng (??)
nqp = len(AKT)
#ng = 90


#
# Create NT
#
NT = []
for iz in range(nz):
    for iy in range(ny):
        for ix in range(nx):
            # bx -- short for "base x"
            bx, by, bz = (ix * 2, iy * 2, iz * 2)

            locv = [AKTr[bx][by][bz]]                   # 1
            locv.append(AKTr[bx + 2][by][bz])           # 2
            locv.append(AKTr[bx + 2][by + 2][bz])       # 3
            locv.append(AKTr[bx][by + 2][bz])           # 4
            locv.append(AKTr[bx][by][bz + 2])           # 5
            locv.append(AKTr[bx + 2][by][bz + 2])       # 6
            locv.append(AKTr[bx + 2][by + 2][bz + 2])   # 7
            locv.append(AKTr[bx][by + 2][bz + 2])       # 8
            locv.append(AKTr[bx + 1][by][bz])           # 9
            locv.append(AKTr[bx + 2][by + 1][bz])       # 10
            locv.append(AKTr[bx + 1][by + 2][bz])       # 11
            locv.append(AKTr[bx][by + 1][bz])           # 12
            locv.append(AKTr[bx][by][bz + 1])           # 13
            locv.append(AKTr[bx + 2][by][bz + 1])       # 14
            locv.append(AKTr[bx + 2][by + 2][bz + 1])   # 15
            locv.append(AKTr[bx][by + 2][bz + 1])       # 16
            locv.append(AKTr[bx + 1][by][bz + 2])       # 17
            locv.append(AKTr[bx + 2][by + 1][bz + 2])   # 18
            locv.append(AKTr[bx + 1][by + 2][bz + 2])   # 19
            locv.append(AKTr[bx][by + 1][bz + 2])       # 20

            print(locv)
            NT.append(locv)


#
# Plot the mesh
#
x,y,z = zip(*AKT)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c='b', marker='o')
for i, (px, py, pz) in enumerate(AKT):
    ax.text(px, py, pz, str(i + 1), color='red')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Scatter Plot with Indices')
set_axes_equal(ax)
plt.show()
