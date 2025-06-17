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

vtk_quadratic_hexahedron = 25

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
        self.fem = FEM(1,1,1,1,1,1)
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

        layout.addWidget(QLabel("Константи (E, nu)"))
        self.e_input = QLineEdit()
        self.e_input.setText(str(self.fem.E))
        self.e_input.setPlaceholderText("E")
        self.nu_input = QLineEdit()
        self.nu_input.setText(str(self.fem.nu))
        self.nu_input.setPlaceholderText("nu")
        constants_hbox = QHBoxLayout()
        constants_hbox.addWidget(self.e_input, 1)
        constants_hbox.addWidget(self.nu_input, 1)
        layout.addLayout(constants_hbox)

        layout.addWidget(QLabel("Навантаження"))
        self.p_input = QLineEdit()
        self.p_input.setText(str(self.fem.P))
        self.p_input.setPlaceholderText("P")
        layout.addWidget(self.p_input)

        update_btn = QPushButton("Обчислити")
        update_btn.clicked.connect(self.remesh)
        layout.addWidget(update_btn)

        layout.addStretch()
        panel.setLayout(layout)
        return panel

    def display_mesh(self):
        self.plotter.clear()

        points = self.fem.AKT.copy()

        # Apply shift
        for p_idx, p in enumerate(self.fem.u):
            points[p_idx // 3][p_idx % 3] += p

        # Re-shape NT
        nt = []
        for el in self.fem.NT:
            nt.append([20,
                       el[3],  el[2],  el[1],  el[0],
                       el[7],  el[6],  el[5],  el[4],
                       el[10], el[9],  el[8],  el[11],
                       el[18], el[17], el[16], el[19],
                       el[15], el[14], el[13], el[12]])

        num_cells = len(self.fem.finite_elements)
        cells_flat = np.array(nt).flatten()


        # Локальні індекси вершин для ребер серендипового гексаедра
        serendip_edge_triplets = [
            (0,  8, 1), (1,  9, 2), (2, 10, 3), (3, 11, 0),  # низ
            (4, 12, 5), (5, 13, 6), (6, 14, 7), (7, 15, 4),  # верх
            (0, 16, 4), (1, 17, 5), (2, 18, 6), (3, 19, 7),  # боки
        ]

        for element in nt:
            for i, j, k in serendip_edge_triplets:
                p0 = self.fem.AKT[element[i+1]]
                pm = self.fem.AKT[element[j+1]]
                p1 = self.fem.AKT[element[k+1]]
                self.plotter.add_lines(np.array([p0, pm]), color="black", width=1)
                self.plotter.add_lines(np.array([pm, p1]), color="black", width=1)

        # Типи комірок
        cell_types = np.full(num_cells, vtk_quadratic_hexahedron, dtype=np.uint8)

        grid = pv.UnstructuredGrid(cells_flat, cell_types, points)

        point_cloud = pv.PolyData(points)
        self.plotter.add_mesh(point_cloud, color='blue', point_size=8, render_points_as_spheres=True)

        #
        # point lables
        #
        #for i, pt in enumerate(self.fem.AKT):
            #self.plotter.add_point_labels(point_cloud, list(map(str, range(len(self.fem.AKT)))), point_size=0, font_size=12, text_color="blue", shape_opacity=0)

        #self.plotter.add_mesh(grid, show_edges=True, style="wireframe", color="black", line_width=1)

        self.plotter.add_axes()

    def remesh(self):
        self.fem = FEM(
                int(self.ax_input.text()),
                int(self.ay_input.text()),
                int(self.az_input.text()),
                int(self.nx_input.text()),
                int(self.ny_input.text()),
                int(self.nz_input.text()),
                float(self.e_input.text()),
                float(self.nu_input.text()),
                float(self.p_input.text()))
        self.fem.mesh()
        camera_position = self.plotter.camera_position
        self.display_mesh()
        self.plotter.camera_position = camera_position


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
