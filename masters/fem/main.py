#!./venv/bin/python3

import sys
import numpy as np
import pyvista as pv
from pyvistaqt import QtInteractor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFrame, QCheckBox,
    QHBoxLayout, QLineEdit, QLabel, QPushButton, QRadioButton, QButtonGroup)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator

from fem import FEM
from collapsible_section import CollapsibleSection
import copy


vtk_quadratic_hexahedron = 25


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FEM")
        self.resize(1200, 800)

        main_layout = QHBoxLayout()

        self.vertices_actor = None
        self.vertex_labels_actor = None

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
        self.fem = FEM(2,2,2,2,2,2)
        self.fem.mesh()

        # Also init picked faces
        self.picked_faces_p = []
        self.picked_faces_u = []

        # Side panel (depends on self.fem)
        self.side_panel = self.create_side_panel()
        # Render side panel
        self.display_mesh()

        main_layout.addWidget(self.plotter, 3)
        main_layout.addWidget(self.side_panel, 1)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_side_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()

        # Cube size inputs
        mesh_section = CollapsibleSection("Сітка")
        mesh_section.add_widget(QLabel("Розмір (ax,ay,az)"))
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
        mesh_section.add_layout(cubesize_hbox)

        mesh_section.add_widget(QLabel("Поділ (nx,ny,nz)"))
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
        mesh_section.add_layout(cubemesh_hbox)

        update_btn = QPushButton("Згенерувати сітку")
        update_btn.clicked.connect(self.remesh)
        mesh_section.add_widget(update_btn)

        self.vertex_labels_checkbox = QCheckBox("Показати номери вершин")
        self.vertex_labels_checkbox.setChecked(False)
        self.vertex_labels_checkbox.stateChanged.connect(self.toggle_vertex_labels)
        self.vertex_checkbox = QCheckBox("Показати вершини")
        self.vertex_checkbox.setChecked(True)
        self.vertex_checkbox.stateChanged.connect(self.toggle_vertices)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        mesh_section.add_widget(line)
        mesh_section.add_widget(self.vertex_checkbox)
        mesh_section.add_widget(self.vertex_labels_checkbox)

        layout.addWidget(mesh_section)

        #line = QFrame()
        #line.setFrameShape(QFrame.HLine)
        #line.setFrameShadow(QFrame.Sunken)
        #layout.addWidget(line)
        layout.addSpacing(10)

        constants_section = CollapsibleSection("Константи")
        self.e_input = QLineEdit()
        self.e_input.setText(str(self.fem.E))
        self.e_input.setPlaceholderText("E")
        self.nu_input = QLineEdit()
        self.nu_input.setText(str(self.fem.nu))
        self.nu_input.setPlaceholderText("nu")
        constants_hbox = QHBoxLayout()
        constants_hbox.addWidget(QLabel("E:"), 1)
        constants_hbox.addWidget(self.e_input, 5)
        constants_hbox.addWidget(QLabel("nu:"), 1)
        constants_hbox.addWidget(self.nu_input, 5)
        constants_section.add_layout(constants_hbox)

        self.p_input = QLineEdit()
        self.p_input.setText(str(self.fem.P))
        self.p_input.setPlaceholderText("P")
        constants_hbox = QHBoxLayout()
        constants_hbox.addWidget(QLabel("P:"), 1)
        constants_hbox.addWidget(self.p_input, 11)
        constants_section.add_layout(constants_hbox)
        update_btn = QPushButton("Обчислити")
        update_btn.clicked.connect(self.calc)
        constants_section.add_widget(update_btn)
        go_back_btn = QPushButton("Повернутись до сітки")
        go_back_btn.clicked.connect(self.back_to_mesh)
        constants_section.add_widget(go_back_btn)
        layout.addWidget(constants_section)

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


    def display_mesh(self, apply_shift=False):
        self.plotter.clear()

        points = copy.deepcopy(self.fem.AKT)

        if apply_shift:
            for p_idx, p in enumerate(self.fem.u):
                points[p_idx // 3][p_idx % 3] += p

        if not apply_shift:
            self.grid, self.outer_faces = self.build_outer_faces_polydata(self.fem.AKT, self.fem.NT)
            _colors = []
            for i in range(self.grid.n_cells):
                if i in self.picked_faces_p:
                    _colors.append([0, 255, 0])
                elif i in self.picked_faces_u:
                    _colors.append([255, 0, 0])
                else:
                    _colors.append([255, 255, 255])
            self.grid.cell_data["colors"] = _colors
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


        #############Stress map ##################
        stress = [p[1] for p in points]
        cells = []
        for el in self.fem.NT:
            cells.append(np.hstack([8, *[*el[:4], *el[12:16]]]))
            cells.append(np.hstack([8, *[*el[12:16], *el[4:8]]]))
        cells = np.array(cells).ravel()
        cell_types = np.full(len(self.fem.NT)*2, pv.CellType.HEXAHEDRON)
        gr = pv.UnstructuredGrid(cells, cell_types, points)
        gr.point_data["stress"] = stress
        ##########################################

        self.plotter.add_mesh(mesh, color='black', line_width=1)
        if self.vertex_checkbox.isChecked():
            self.vertices_actor = self.plotter.add_mesh(mesh.points, color='blue', point_size=8, render_points_as_spheres=True)
        if apply_shift:
            self.plotter.add_mesh(gr, scalars="stress",
                                  cmap="bwr", clim=[-np.max(np.abs(stress)), np.max(np.abs(stress))],
                                  show_edges=False,
                                  opacity=0.5,
                                  show_scalar_bar=True,
                                  scalar_bar_args={"title": "Напруження"})
        if self.vertex_labels_checkbox.isChecked():
            labels = [str(i) for i in range(np.array(points).shape[0])]
            self.vertex_labels_actor = self.plotter.add_point_labels(
                    mesh.points,
                    labels,
                    font_size=12,
                    show_points=False,
                    text_color='black',
                    fill_shape=False)
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

    def toggle_vertex_labels(self, state):
        if self.vertex_labels_actor:
            self.plotter.remove_actor(self.vertex_labels_actor)
            self.plotter.renderer.RemoveActor(self.vertex_labels_actor)
            self.vertex_labels_actor = None
        if state == Qt.Checked:
            labels = [str(i) for i in range(np.array(self.fem.AKT).shape[0])]
            self.vertex_labels_actor = self.plotter.add_point_labels(
                    self.fem.AKT,
                    labels,
                    font_size=12,
                    show_points=False,
                    text_color='black',
                    fill_shape=False)
        self.plotter.update()

    def toggle_vertices(self, state):
            #self.plotter.renderer.RemoveActor(self.vertices_actor)
            #self.vertices_actor = None
        if self.vertices_actor:
            if state == Qt.Checked:
                self.plotter.add_actor(self.vertices_actor)
            else:
                self.plotter.remove_actor(self.vertices_actor)
        self.plotter.update()

    def calc(self):
        #if len(self.picked_faces_p) == 0 or len(self.picked_faces_u) == 0:
            #return

        zu = []
        print("U faces:", self.picked_faces_u)
        for uface in self.picked_faces_u:
            zu.append((self.outer_faces[uface][0], self.outer_faces[uface][1]))
        zu = list(set(zu))
        print("zu:", zu)

        zp = []
        print("P faces:", self.picked_faces_p)
        for pface in self.picked_faces_p:
            zp.append((self.outer_faces[pface][0], self.outer_faces[pface][1]))
        zp = list(set(zp))
        print("zp:", zp)

        self.fem.mesh()
        self.fem.calc(
                float(self.e_input.text()),
                float(self.nu_input.text()),
                float(self.p_input.text()), zp, zu)
        self.display_mesh(True)

    def back_to_mesh(self):
        camera_position = self.plotter.camera_position
        self.display_mesh()
        self.plotter.camera_position = camera_position


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
