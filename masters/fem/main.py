#!./venv/bin/python3

import sys
import numpy as np
import pyvista as pv
from pyvistaqt import QtInteractor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLineEdit, QLabel, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from vtk import VTK_QUADRATIC_HEXAHEDRON

from fem import FEM


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FEM")
        self.resize(1200, 800)

        main_layout = QHBoxLayout()

        # 3D viewer
        self.plotter = QtInteractor(self)
        self.plotter.set_background("white")
        # Init FEM with default values
        self.fem = FEM(2,2,3,1,1,2)
        self.fem.mesh()
        self.display_mesh()

        # Side panel
        self.side_panel = self.create_side_panel()

        main_layout.addWidget(self.plotter, 3)
        main_layout.addWidget(self.side_panel, 1)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_side_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()

        # Cube size inputs
        layout.addWidget(QLabel("Розмір (ax,ay,az)"))
        self.ax_input = QLineEdit()
        self.ax_input.setText(str(self.fem.ax))
        self.ax_input.setPlaceholderText("ax")
        self.ax_input.setValidator(QIntValidator(1, 100))
        self.ay_input = QLineEdit()
        self.ay_input.setText(str(self.fem.ay))
        self.ay_input.setPlaceholderText("ay")
        self.ay_input.setValidator(QIntValidator(1, 100))
        self.az_input = QLineEdit()
        self.az_input.setText(str(self.fem.az))
        self.az_input.setPlaceholderText("az")
        self.az_input.setValidator(QIntValidator(1, 100))
        cubesize_hbox = QHBoxLayout()
        cubesize_hbox.addWidget(self.ax_input, 1)
        cubesize_hbox.addWidget(self.ay_input, 1)
        cubesize_hbox.addWidget(self.az_input, 1)
        layout.addLayout(cubesize_hbox)

        layout.addWidget(QLabel("Сітка (nx,ny,nz)"))
        self.nx_input = QLineEdit()
        self.nx_input.setText(str(self.fem.nx))
        self.nx_input.setPlaceholderText("nx")
        self.nx_input.setValidator(QIntValidator(1, 50))
        self.ny_input = QLineEdit()
        self.ny_input.setText(str(self.fem.ny))
        self.ny_input.setPlaceholderText("ny")
        self.ny_input.setValidator(QIntValidator(1, 50))
        self.nz_input = QLineEdit()
        self.nz_input.setText(str(self.fem.nz))
        self.nz_input.setPlaceholderText("nz")
        self.nz_input.setValidator(QIntValidator(1, 50))
        cubemesh_hbox = QHBoxLayout()
        cubemesh_hbox.addWidget(self.nx_input, 1)
        cubemesh_hbox.addWidget(self.ny_input, 1)
        cubemesh_hbox.addWidget(self.nz_input, 1)
        layout.addLayout(cubemesh_hbox)

        update_btn = QPushButton("Оновити сітку")
        update_btn.clicked.connect(self.remesh)
        layout.addWidget(update_btn)

        layout.addStretch()
        panel.setLayout(layout)
        return panel

    def display_mesh(self):
        self.plotter.clear()

        points = self.fem.AKT.copy()

        for p_idx, p in enumerate(self.fem.u):
            points[p_idx // 3][p_idx % 3] += p

        point_cloud = pv.PolyData(points)
        self.plotter.add_mesh(point_cloud, color='black', point_size=10, render_points_as_spheres=True)

        self.plotter.add_axes()

    def remesh(self):
        self.fem = FEM(
                int(self.ax_input.text()),
                int(self.ay_input.text()),
                int(self.az_input.text()),
                int(self.nx_input.text()),
                int(self.ny_input.text()),
                int(self.nz_input.text()))
        self.fem.mesh()
        camera_position = self.plotter.camera_position
        self.display_mesh()
        self.plotter.camera_position = camera_position


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())




#=====================================================================================

"""
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
"""

