import numpy as np
import math


local_coords = [
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


face_local_coords = [
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


sqrt06 = math.sqrt(0.6)


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

        self.c = [5/9, 8/9, 5/9]

        self.E = 0
        self.nu = 0
        self.mu = 0
        self.lambda_ = 0
        self.P = 0

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

        self.ZP = []
        elems_count = len(self.finite_elements)
        for i in range(self.nx * self.ny):
            self.ZP.append([elems_count - i - 1, 6, self.P])

        self.NT = self._NT()

        self.DFIABG = self._DFIABG()

        self.DPSITE = self._DPSITE()

        self.DXYZABG = []
        for f_elem in self.finite_elements:
            self.DXYZABG.append(self._DXYZABG(f_elem))

        self.DJ = []
        for dxyzabg in self.DXYZABG:
            self.DJ.append(self._DJ(dxyzabg))

        self.DFIXYZ = []
        for elem_idx, _ in enumerate(self.finite_elements):
            self.DFIXYZ.append(self._DFIXYZ(elem_idx))

        FE = []
        for zp in self.ZP:
            FE.append(self._FE(zp))

        # Закріплюємо нижню грань
        self.ZU = []
        for point in self.AKT:
            if point[2] == 0:
                self.ZU.append(point)

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
        DFIABG = []
        for gamma in [-sqrt06, 0, sqrt06]:
            for beta in [-sqrt06, 0, sqrt06]:
                for alpha in [-sqrt06, 0, sqrt06]:
                    el = []
                    for i, abg_i in enumerate(local_coords):
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

    def _dpsi_deta_14(self, e, t, ei, ti):
        return (1/4) * (t*ti + 1) * ei * (2*ei*e +   ti*t)

    def _dpsi_dtao_14(self, e, t, ei, ti):
        return (1/4) * (ei*e + 1) * ti * (  ei*e + 2*ti*t)

    def _dpsi_deta_57(self, e, t, ei, ti):
        return (-t*ti - 1) * e

    def _dpsi_dtao_57(self, e, t, ei, ti):
        return (1/2) * (1 - e*e)*ti

    def _dpsi_deta_68(self, e, t, ei, ti):
        return (1/2) * (1 - t*t)*ei

    def _dpsi_dtao_68(self, e, t, ei, ti):
        return (-e*ei - 1)*t

    def _DPSITE(self):
        dpsite = []
        for eta in [-sqrt06, 0, sqrt06]:
            for tau in [-sqrt06, 0, sqrt06]:
                el = []
                for i, et in enumerate(face_local_coords):
                    if i < 4:
                        el.append([self._dpsi_deta_14(eta, tau, et[0], et[1]),
                                   self._dpsi_dtao_14(eta, tau, et[0], et[1])])
                    elif i == 4 or i == 6:
                        el.append([self._dpsi_deta_57(eta, tau, et[0], et[1]),
                                   self._dpsi_dtao_57(eta, tau, et[0], et[1])])
                    elif i == 5 or i == 7:
                        el.append([self._dpsi_deta_68(eta, tau, et[0], et[1]),
                                   self._dpsi_dtao_68(eta, tau, et[0], et[1])])
                dpsite.append(el)
        return dpsite

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

    def _MGE(self, el_idx):
        a11, a22, a33 = [np.zeros((20, 20)) for _ in range(3)]
        a12, a13, a23 = [np.zeros((20, 20)) for _ in range(3)]

        for i in range(20):
            for j in range(20):
                gauss_i = 0
                for cm in self.c:
                    for cn in self.c:
                        for ck in self.c:
                            d_phi = self.DFIXYZ[el_idx][gauss_i]

                            a11[i][j] += cm * cn * ck \
                                    * (self.lambda_ * (1 - self.nu) * d_phi[i][0] * d_phi[j][0] \
                                       + self.mu * (d_phi[i][1] * d_phi[j][1] + d_phi[i][2] * d_phi[j][2])) \
                                       * self.DJ[el_idx][gauss_i]

                            a22[i][j] += cm * cn * ck * \
                                       (self.lambda_ * (1 - self.nu) * (d_phi[i][1] * d_phi[j][1]) \
                                        + self.mu * (d_phi[i][0] * d_phi[j][0] + d_phi[i][2] * d_phi[j][2])) \
                                        * self.DJ[el_idx][gauss_i]

                            a33[i][j] += cm * cn * ck * \
                                       (self.lambda_ * (1 - self.nu) * (d_phi[i][2] * d_phi[j][2]) \
                                        + self.mu * ((d_phi[i][0] * d_phi[j][0]) + (d_phi[i][1] * d_phi[j][1]))) \
                                        * self.DJ[el_idx][gauss_i]

                            a12[i][j] += cm * cn * ck * (self.lambda_ * self.nu * (d_phi[i][0] * d_phi[j][1]) \
                                    + self.mu * (d_phi[i][1] * d_phi[j][0])) \
                                    * self.DJ[el_idx][gauss_i]

                            a13[i][j] += cm * cn * ck \
                                    * (self.lambda_ * self.nu * (d_phi[i][0] * d_phi[j][2]) \
                                    + self.mu * (d_phi[i][2] * d_phi[j][0])) \
                                    * self.DJ[el_idx][gauss_i]

                            a23 += cm * cn * ck \
                                    * (lambda_val * self.nu * (d_phi[i][1] * d_phi[j][2]) \
                                    + self.mu * (d_phi[i][2] * d_phi[j][1])) \
                                    * self.DJ[el_idx][gauss_i]

                            gauss_i = gauss_i + 1

        return np.block([
                [a11, a12, a13],
                [a12, a22, a23],
                [a13, a23, a33]
            ]).tolist()

    def DxyzDnt(self, xyz):
        result = []
        depsite = self.DPSITE()
        index_for_depsite = 0
        for eta in eta_for:
            for tau in tau_for:
                summ_x_eta = []
                summ_y_eta = []
                summ_z_eta = []
                summ_x_tau = []
                summ_y_tau = []
                summ_z_tau = []
                for point in xyz:
                    index_of_nt = xyz.index(point)
                    summ_x_eta.append(point[0] * depsite[index_for_depsite][index_of_nt][0])
                    summ_y_eta.append(point[1] * depsite[index_for_depsite][index_of_nt][0])
                    summ_z_eta.append(point[2] * depsite[index_for_depsite][index_of_nt][0])
                    summ_x_tau.append(point[0] * depsite[index_for_depsite][index_of_nt][1])
                    summ_y_tau.append(point[1] * depsite[index_for_depsite][index_of_nt][1])
                    summ_z_tau.append(point[2] * depsite[index_for_depsite][index_of_nt][1])
                result.append([
                    [sum(summ_x_eta), sum(summ_x_tau)],
                    [sum(summ_y_eta), sum(summ_y_tau)],
                    [sum(summ_z_eta), sum(summ_z_tau)]
                ])
                index_for_depsite += 1
        return result

    def _FE(self, a):
        pass
