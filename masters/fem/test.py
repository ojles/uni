#!./venv/bin/python3

import sys
import numpy as np
import pyvista as pv
from pyvistaqt import QtInteractor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLineEdit, QLabel, QPushButton
)
from PyQt5.QtCore import Qt
from vtk import VTK_QUADRATIC_HEXAHEDRON


def create_serendipitous_cube(scale=1.0):
    corners = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 1, 1],
    ], dtype=float) * scale

    edge_mids = np.array([
        [(0 + 1)/2, 0, 0],
        [1, (0 + 1)/2, 0],
        [(1 + 0)/2, 1, 0],
        [0, (1 + 0)/2, 0],
        [(0 + 1)/2, 0, 1],
        [1, (0 + 1)/2, 1],
        [(1 + 0)/2, 1, 1],
        [0, (1 + 0)/2, 1],
        [0, 0, (0 + 1)/2],
        [1, 0, (0 + 1)/2],
        [1, 1, (0 + 1)/2],
        [0, 1, (0 + 1)/2],
    ], dtype=float) * scale

    points = np.vstack([corners, edge_mids])
    cell = np.array([
        20, 0, 1, 2, 3, 4, 5, 6, 7,
        8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
    ])
    grid = pv.UnstructuredGrid(
        np.array([cell], dtype=np.int64),
        np.array([VTK_QUADRATIC_HEXAHEDRON], dtype=np.uint8),
        points
    )
    return grid, points


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Serendipitous Cube Viewer")
        self.resize(1200, 800)

        main_layout = QHBoxLayout()

        # 3D viewer
        self.plotter = QtInteractor(self)
        self.plotter.set_background("white")
        self.add_cube_mesh()

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

        self.scale_input = QLineEdit()
        self.scale_input.setPlaceholderText("Cube scale (e.g., 1.0)")
        layout.addWidget(QLabel("Cube Scale:"))
        layout.addWidget(self.scale_input)

        update_btn = QPushButton("Update Cube")
        update_btn.clicked.connect(self.update_cube)
        layout.addWidget(update_btn)

        layout.addStretch()
        panel.setLayout(layout)
        return panel

    def add_cube_mesh(self, scale=1.0):
        self.plotter.clear()

        grid, points = create_serendipitous_cube(scale=scale)
        self.plotter.add_mesh(grid, show_edges=True, color="lightgreen", opacity=0.8)

        # Black dots at points
        self.plotter.add_mesh(
            pv.PolyData(points),
            color='black', point_size=15, render_points_as_spheres=True
        )

        # Numbered labels (shifted a bit)
        offset = np.array([0.05, 0.05, 0.05]) * scale
        label_points = points + offset
        labels = [str(i + 1) for i in range(points.shape[0])]
        self.plotter.add_point_labels(
            label_points,
            labels,
            font_size=14,
            text_color='red',
            shape_opacity=0.5  # Optional: semi-transparent background
        )

        self.plotter.add_axes()

    def update_cube(self):
        try:
            scale = float(self.scale_input.text())
        except ValueError:
            scale = 1.0  # fallback

        self.add_cube_mesh(scale=scale)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

