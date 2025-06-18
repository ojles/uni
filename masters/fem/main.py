#!./venv/bin/python3

import sys
import numpy as np
import pyvista as pv
from pyvistaqt import QtInteractor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFrame,
    QHBoxLayout, QLineEdit, QLabel, QPushButton, QRadioButton, QButtonGroup)
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
        self.plotter.enable_cell_picking(
            callback=self.on_pick,
            through=False,
            show_message=False,
            show=False,
            style='surface')

        #
        # Init FEM with default values
        self.fem = FEM(1,1,1,1,1,1)
        self.fem.mesh()
        self.display_mesh()
        # Side panel
        self.side_panel = self.create_side_panel()
        # Also init picked faces
        self.picked_faces_p = []
        self.picked_faces_u = []

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

        update_btn = QPushButton("Згенерувати сітку")
        update_btn.clicked.connect(self.remesh)
        layout.addWidget(update_btn)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        layout.addSpacing(10)

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
        update_btn.clicked.connect(self.calc)
        layout.addWidget(update_btn)

        ##############################################3
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        layout.addSpacing(15)
        layout.addWidget(QLabel("Задання області Г"))
        self.radio_p = QRadioButton("P")
        self.radio_p.setChecked(True)
        self.radio_u = QRadioButton("Закріпити")
        group = QButtonGroup(panel)
        group.addButton(self.radio_p)
        group.addButton(self.radio_u)
        somebox = QHBoxLayout()
        somebox.addWidget(self.radio_p, 1)
        somebox.addWidget(self.radio_u, 1)
        layout.addLayout(somebox)
        ###############################################

        layout.addStretch()
        panel.setLayout(layout)
        return panel

    def find_outer_faces(self, NT):
        face_quads = [
            [0, 1, 2, 3],  # bottom
            [4, 5, 6, 7],  # top
            [0, 1, 5, 4],  # front
            [2, 3, 7, 6],  # back
            [0, 3, 7, 4],  # left
            [1, 2, 6, 5]]  # right

        from collections import defaultdict
        face_map = defaultdict(list)

        for elem_id, element in enumerate(NT):
            for face_id, face in enumerate(face_quads):
                original_nodes = [element[i] for i in face]
                key = tuple(sorted(original_nodes))
                face_map[key].append((elem_id, face_id, original_nodes))

        # залишаємо тільки ті, що трапляються один раз
        outer_faces = []
        for face_key, refs in face_map.items():
            if len(refs) == 1:
                outer_faces.append(refs[0])  # (elem_id, face_id, original_nodes)

        return outer_faces

    def build_outer_faces_polydata(self, AKT, NT):
        outer_faces = self.find_outer_faces(NT)

        faces = []
        for _, _, node_ids in outer_faces:
            faces.append(4)
            faces.extend(node_ids)
        faces = np.array(faces)

        grid = pv.PolyData(AKT, faces)
        return grid, outer_faces

    def on_pick(self, mesh):
        if mesh is None or mesh.n_cells == 0:
            return

        picked_face = mesh.extract_cells(0)
        picked_center = picked_face.cell_centers().points[0]

        for idx, (_, _, node_ids) in enumerate(self.outer_faces):
            face_points = [self.fem.AKT[i] for i in node_ids]
            face_center = np.mean(face_points, axis=0)
            if np.allclose(face_center, picked_center, atol=1e-6):
                picked_cell = idx
                break
        else:
            print("Грань не знайдена.")
            return

        print(f"Клік по грані {picked_cell}")
        if self.radio_p.isChecked():
            pfaces = self.picked_faces_p
            otherfaces = self.picked_faces_u
        else:
            pfaces = self.picked_faces_u
            otherfaces = self.picked_faces_p
        try:
            pfaces.index(picked_cell)
            pfaces.remove(picked_cell)
        except ValueError:
            try:
                # This face is already used
                otherfaces.index(picked_cell)
                otherfaces.remove(picked_cell)
                pfaces.append(picked_cell)
            except ValueError:
                pfaces.append(picked_cell)

        print("pface:", pfaces)
        print("otherfaces:", otherfaces)

        self.grid.cell_data.active_scalars_name = "colors"
        _colors = []
        for i in range(self.grid.n_cells):
            if i in self.picked_faces_p:
                _colors.append([0, 255, 0])
            elif i in self.picked_faces_u:
                _colors.append([255, 0, 0])
            else:
                _colors.append([255, 255, 255])
        self.grid.cell_data["colors"] = np.array(_colors)
        self.actor.mapper.scalar_visibility = True
        self.actor.mapper.lookup_table = None
        self.plotter.update()


    def display_mesh(self):
        self.plotter.clear()

        points = self.fem.AKT.copy()

        # Apply shift
        #for p_idx, p in enumerate(self.fem.u):
            #points[p_idx // 3][p_idx % 3] += p

        self.grid, self.outer_faces = self.build_outer_faces_polydata(self.fem.AKT, self.fem.NT)
        colors = np.array([[255, 255, 255] for i in range(self.grid.n_cells)], dtype=np.uint8)
        self.grid.cell_data["colors"] = colors
        self.actor = self.plotter.add_mesh(self.grid, show_edges=True, rgb=True, opacity=0.9)

        serendip_edge_triplets = [
            (0,  8, 1), (1,  9, 2), (2, 10, 3), (3, 11, 0),  # bottom
            (4, 16, 5), (5, 17, 6), (6, 18, 7), (7, 19, 4),  # top
            (0, 12, 4), (1, 13, 5), (2, 14, 6), (3, 15, 7)]  # middle
        lines = []
        for element in self.fem.NT:
            for i, j, k in serendip_edge_triplets:
                lines.append(3)
                lines.append(element[i])
                lines.append(element[j])
                lines.append(element[k])
        mesh = pv.PolyData()
        mesh.points = points
        mesh.lines = lines

        self.plotter.add_mesh(mesh, color='black', line_width=1)
        self.plotter.add_mesh(mesh.points, color='blue', point_size=8, render_points_as_spheres=True)
        self.plotter.add_axes()

    def remesh(self):
        self.picked_faces_p = []
        self.picked_faces_u = []
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

    def calc(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
