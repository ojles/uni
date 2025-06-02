import numpy as np
import math


FE_local_coords = [
        [-1, 1, -1],
        [1, 1, -1],
        [1, -1, -1],
        [-1, -1, -1],
        [-1, 1, 1],
        [1, 1, 1],
        [1, -1, 1],
        [-1, -1, 1],
        [0, 1, -1],
        [1, 0, -1],
        [0, -1, -1],
        [-1, 0, -1],
        [-1, 1, 0],
        [1, 1, 0],
        [1, -1, 0],
        [-1, -1, 0],
        [0, 1, 1],
        [1, 0, 1],
        [0, -1, 1],
        [-1, 0, 1]
    ]


class FEM():
    def __init__(self, ax, ay, az, nx, ny, nz):
        self.ax = ax
        self.ay = ay
        self.az = az
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.dx = ax / nx
        self.dy = ay / ny
        self.dz = az / nz

    def mesh(self):
        AKT = []
        x_scale = self.dx / 2
        y_scale = self.dy / 2
        z_scale = self.dz / 2
        for iz in range(self.nz * 2 + 1):
            y_step = 1 + (iz % 2)
            for iy in range(0, self.ny * 2 + 1, y_step):
                x_step = 1 + ((iy + iz) % 2)
                for ix in range(0, self.nx * 2 + 1, x_step):
                    AKT.append([ix*x_scale, iy*y_scale, iz*z_scale])

        self.AKT = AKT
        self.nqp = len(AKT)

        # Finite elements array
        self.finite_elements = self._finite_elements()

        self.NT = self._NT()

        self.DFIABG = self._DFIABG()

        self.DXYZABG = []
        for f_elem in self.finite_elements:
             self.DXYZABG.append(self._DXYZABG(f_elem))

        self.DJ = []
        for dxyzabg in self.DXYZABG:
            self.DJ.append(self._DJ(dxyzabg))

        self.DFIXYZ = []
        for elem_idx, _ in enumerate(self.finite_elements):
             self.DFIXYZ.append(self._DFIXYZ(elem_idx))

    def _finite_element(self, x0, y0, z0):
        x1 = x0 + self.dx
        y1 = y0 + self.dy
        z1 = z0 + self.dz
        x05 = (x0 + x1) / 2
        y05 = (y0 + y1) / 2
        z05 = (z0 + z1) / 2
        return [
                # 1, 2, 3, 4
                [x0, y1, z0],
                [x1, y1, z0],
                [x1, y0, z0],
                [x0, y0, z0],
                # 5, 6, 7, 8
                [x0, y1, z1],
                [x1, y1, z1],
                [x1, y0, z1],
                [x0, y0, z1],
                # 9, 10, 11, 12
                [x05, y1, z0],
                [x1, y05, z0],
                [x05, y0, z0],
                [x0, y05, z0],
                # 13, 14, 15, 16
                [x0, y1, z05],
                [x1, y1, z05],
                [x1, y0, z05],
                [x0, y0, z05],
                # 17, 18, 19, 20
                [x05, y1, z1],
                [x1, y05, z1],
                [x05, y0, z1],
                [x0, y05, z1],
            ]


    def _finite_elements(self):
        finite_elements = []
        for zi in range(self.nz):
            for yi in range(self.ny):
                for xi in range(self.nx):
                    f_elem = self._finite_element(xi * self.dx, yi * self.dy, zi * self.dz)
                    finite_elements.append(f_elem)
        return finite_elements


    def _NT(self):
        nt = []
        for f_elem in self.finite_elements:
            nt0 = []
            for vertex in f_elem:
                nt0.append(self.AKT.index(vertex))
            nt.append(nt0)
        return nt


    def _dPhi_dAlpha_1(self, a, b, g, ai, bi, gi):
        return (1/8) * ai * (1 + b*bi) * (1 + g*gi) * (2*a*ai + b*bi + g*gi - 1)

    def _dPhi_dBeta_1(self, a, b, g, ai, bi, gi):
        return (1/8) * bi * (1 + a*ai) * (1 + g*gi) * (a*ai + 2*b*bi + g*gi - 1)

    def _dPhi_dGamma_1(self, a, b, g, ai, bi, gi):
        return (1/8) * gi * (1 + a*ai) * (1 + b*bi) * (a*ai + b*bi + 2*g*gi - 1)

    def _dPhi_dAlpha_2(self, a, b, g, ai, bi, gi):
        return (1/4) * (1 + b*bi) * (1 + g*gi) \
                * (ai*(1 - a*a*bi*bi*gi*gi - b*b*ai*ai*gi*gi - g*g*ai*ai*bi*bi) - 2*a*(1+a*ai)*bi*bi*gi*gi)

    def _dPhi_dBeta_2(self, a, b, g, ai, bi, gi):
        return (1/4) * (1 + a*ai) * (1 + g*gi) \
                * (bi*(1 - a*a*bi*bi*gi*gi - b*b*ai*ai*gi*gi - g*g*ai*ai*bi*bi) - 2*b*(1+b*bi)*ai*ai*gi*gi)

    def _dPhi_dGamma_2(self, a, b, g, ai, bi, gi):
        return (1/4) * (1 + a*ai) * (1 + b*bi) \
                * (gi*(1 - a*a*bi*bi*gi*gi - b*b*ai*ai*gi*gi - g*g*ai*ai*bi*bi) - 2*g*(1+g*gi)*ai*ai*bi*bi)

    def _DFIABG(self):
        sqrt06 = math.sqrt(0.6)

        DFIABG = []
        for gamma in [-sqrt06, 0, sqrt06]:
            for beta in [-sqrt06, 0, sqrt06]:
                for alpha in [-sqrt06, 0, sqrt06]:
                    el = []
                    for i, abg_i in enumerate(FE_local_coords):
                        if i <= 7:
                            el.append([
                                self._dPhi_dAlpha_1(alpha, beta, gamma, abg_i[0], abg_i[1], abg_i[2]),
                                self._dPhi_dBeta_1( alpha, beta, gamma, abg_i[0], abg_i[1], abg_i[2]),
                                self._dPhi_dGamma_1(alpha, beta, gamma, abg_i[0], abg_i[1], abg_i[2])])
                        else:
                            el.append([
                                self._dPhi_dAlpha_2(alpha, beta, gamma, abg_i[0], abg_i[1], abg_i[2]),
                                self._dPhi_dBeta_2( alpha, beta, gamma, abg_i[0], abg_i[1], abg_i[2]),
                                self._dPhi_dGamma_2(alpha, beta, gamma, abg_i[0], abg_i[1], abg_i[2])])
                    DFIABG.append(el)
        return DFIABG

    def _DXYZABG(self, el):
        DXYZABG = []
        for gauss_i in range(3*3*3):
            #   [dx/da, dy/da, dz/da]
            #   [dx/db, dy/db, dz/db]
            #   [dx/dg, dy/dg, dz/dg]
            j = [[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]
            for point_idx, point in enumerate(el):
                for abg_i in range(3):
                    for xyz_i in range(3):
                        j[abg_i][xyz_i] += point[xyz_i] * self.DFIABG[gauss_i][point_idx][abg_i]
            DXYZABG.append(j)
        return DXYZABG

    def _DFIXYZ(self, elem_idx):
        DFIXYZ = []
        for gauss_i in range(3*3*3):
            dfixyz = []
            for phi_i_abg in self.DFIABG[gauss_i]:
                x = np.linalg.solve(self.DXYZABG[elem_idx][gauss_i], phi_i_abg).tolist()
                dfixyz.append(x)
            DFIXYZ.append(dfixyz)
        return DFIXYZ

    def _det(self, j):
        return j[0][0] * j[1][1] * j[2][2] \
                + j[0][1] * j[1][2] * j[2][0] \
                + j[0][2] * j[1][0] * j[2][1] \
                - j[0][2] * j[1][1] * j[2][0] \
                - j[0][0] * j[1][2] * j[2][1] \
                - j[0][1] * j[1][0] * j[2][2]

    def _DJ(self, dxyzabg):
        dj = []
        for j in dxyzabg:
             dj.append(self._det(j))
        return dj
