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
