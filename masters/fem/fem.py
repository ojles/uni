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
        [-1, -1],
        [1, -1],
        [1, 1],
        [-1, 1],
        [0, -1],
        [1, 0],
        [0, 1],
        [-1, 0]
    ]

face_id_idxs = [
        [3, 2, 1, 0, 10, 9, 8, 11],  # bottom
        [7, 6, 5, 4, 18, 17, 16, 19],  # top
        [0, 1, 5, 4, 8, 13, 16, 12],  # front
        [3, 2, 6, 7, 10, 14, 18, 15],  # back
        [3, 0, 4, 7, 11, 12, 19, 15],  # left
        [1, 2, 6, 5, 9, 14, 17, 13]  # right
    ]


sqrt06 = math.sqrt(0.6)


class FEM():
    def __init__(self, ax, ay, az, nx, ny, nz, E=1, nu=0.3, P=0.5):
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

        self.set_params(E, nu, P)

        self.AKT = []

    def set_params(self, E, nu, P):
        self.E = E
        self.nu = nu
        self.lambda_ = self.E / ((1 + self.nu) * (1 - 2 * self.nu))
        self.mu = self.E / (2 * (1 + self.nu))
        self.P = P

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

    def calc(self, E, nu, P, zp, zu):
        if len(self.AKT) == 0:
            self.mesh()

        self.set_params(E, nu, P)

        self.ZU = zu
        self.ZP = zp

        self.DFIABG = self._DFIABG()
        print("fem: DFIABG done.")

        self.DPSITE = self._DPSITE()
        print("fem: DPSITE done.")

        self.DXYZABG = []
        len_felem = len(self.finite_elements)
        for fidx, f_elem in enumerate(self.finite_elements):
            print(f"fem: DXYZABG el ({fidx}/{len_felem})")
            self.DXYZABG.append(self._DXYZABG(f_elem))
        print("fem: DXYZABG done.")

        self.DJ = []
        for dxyzabg in self.DXYZABG:
            self.DJ.append(self._DJ(dxyzabg))

        self.DFIXYZ = []
        for elem_idx, _ in enumerate(self.finite_elements):
            print(f"fem: DFIXYZ el ({elem_idx}/{len_felem})")
            self.DFIXYZ.append(self._DFIXYZ(elem_idx))
        print("fem: DFIXYZ done.")

        self.MGE = []
        for el_idx, _ in enumerate(self.finite_elements):
            print(f"fem: MGE el ({el_idx}/{len_felem})")
            self.MGE.append(self._MGE(el_idx))
        print("fem: MGE done.")
        one_mge = self.MGE[1]


        FE = []
        for _ in range(len_felem):
            FE.append(np.zeros(60).tolist())
        for elem_id, face_id in self.ZP:
            print(" <<<<<<< FACE")
            FE[elem_id] = self._FE(self.finite_elements[elem_id], face_id)
        print("fem: FE done.")

        MG = self._MG(self.MGE)
        print("fem: MG done.")

        F = self._F(FE)
        print("fem: F done.")

        self.u = np.linalg.solve(MG, F)
        print("fem: Solved.")

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

    def _dpsi_dtau_14(self, e, t, ei, ti):
        return (1/4) * (ei*e + 1) * ti * (  ei*e + 2*ti*t)

    def _dpsi_deta_57(self, e, t, ei, ti):
        return (-t*ti - 1) * e

    def _dpsi_dtau_57(self, e, t, ei, ti):
        return (1/2) * (1 - e*e)*ti

    def _dpsi_deta_68(self, e, t, ei, ti):
        return (1/2) * (1 - t*t)*ei

    def _dpsi_dtau_68(self, e, t, ei, ti):
        return (-e*ei - 1)*t

    def _psi_i_14(self, e, t, ei, ti):
        return (1/4) * (t*ti + 1) * (e*ei + 1) * (e*ei + ti*t - 1)

    def _psi_i_57(self, e, t, ei, ti):
        return (1/2) * (-e*e + 1) * (ti*t + 1)

    def _psi_i_68(self, e, t, ei, ti):
        return (1/2) * (-t*t + 1) * (ei*e + 1)

    def _DPSITE(self):
        dpsite = []
        for eta in [-sqrt06, 0, sqrt06]:
            for tau in [-sqrt06, 0, sqrt06]:
                el = []
                for i, point in enumerate(face_local_coords):
                    if i < 4:
                        el.append([self._dpsi_deta_14(eta, tau, point[0], point[1]),
                                   self._dpsi_dtau_14(eta, tau, point[0], point[1])])
                    elif i == 4 or i == 6:
                        el.append([self._dpsi_deta_57(eta, tau, point[0], point[1]),
                                   self._dpsi_dtau_57(eta, tau, point[0], point[1])])
                    elif i == 5 or i == 7:
                        el.append([self._dpsi_deta_68(eta, tau, point[0], point[1]),
                                   self._dpsi_dtau_68(eta, tau, point[0], point[1])])
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

                            a23[i][j] += cm * cn * ck \
                                    * (self.lambda_ * self.nu * (d_phi[i][1] * d_phi[j][2]) \
                                    + self.mu * (d_phi[i][2] * d_phi[j][1])) \
                                    * self.DJ[el_idx][gauss_i]

                            gauss_i = gauss_i + 1

        return np.block([
                [a11, a12, a13],
                [a12, a22, a23],
                [a13, a23, a33]
            ]).tolist()

    def _DXYZDNT(self, surface):
        DXYZDNT = []
        gauss_i = 0
        for eta in [-sqrt06, 0, sqrt06]:
            for tau in [-sqrt06, 0, sqrt06]:
                dxyzdnt = [[0, 0],
                           [0, 0],
                           [0, 0]]
                for point_idx, point in enumerate(surface):
                    dxyzdnt[0][0] += point[0] * self.DPSITE[gauss_i][point_idx][0]
                    dxyzdnt[0][1] += point[0] * self.DPSITE[gauss_i][point_idx][1]
                    dxyzdnt[1][0] += point[1] * self.DPSITE[gauss_i][point_idx][0]
                    dxyzdnt[1][1] += point[1] * self.DPSITE[gauss_i][point_idx][1]
                    dxyzdnt[2][0] += point[2] * self.DPSITE[gauss_i][point_idx][0]
                    dxyzdnt[2][1] += point[2] * self.DPSITE[gauss_i][point_idx][1]

                DXYZDNT.append(dxyzdnt)
                gauss_i += 1

        return DXYZDNT

    def _PSIi(self):
        PSI_I = []
        for eta in [-sqrt06, 0, sqrt06]:
            for tau in [-sqrt06, 0, sqrt06]:
                psi_i = []
                for point_idx, point in enumerate(face_local_coords):
                    if point_idx < 4:
                        psi_i.append(self._psi_i_14(eta, tau, point[0], point[1]))
                    elif point_idx == 4 or point_idx == 6:
                        psi_i.append(self._psi_i_57(eta, tau, point[0], point[1]))
                    elif point_idx == 5 or point_idx == 7:
                        psi_i.append(self._psi_i_68(eta, tau, point[0], point[1]))
                PSI_I.append(psi_i)
        return PSI_I

    def _FE(self, element, face_id):
        # Choose top surface
        face_idxs = face_id_idxs[face_id]
        surface = [element[i] for i in face_idxs]

        DXYZDNT = self._DXYZDNT(surface)
        PSIi = self._PSIi()

        fe = np.zeros(60).tolist()
        for i in range(8):
            gauss_i = 0

            f1 = 0
            f2 = 0
            f3 = 0
            for cm in self.c:
                for cn in self.c:
                    dxyzdnt = DXYZDNT[gauss_i]
                    psi_i = PSIi[gauss_i][i]

                    f1 += cm * cn * self.P * (dxyzdnt[1][0] * dxyzdnt[2][1] - dxyzdnt[2][0] * dxyzdnt[1][1]) * psi_i
                    f2 += cm * cn * self.P * (dxyzdnt[2][0] * dxyzdnt[0][1] - dxyzdnt[0][0] * dxyzdnt[2][1]) * psi_i
                    f3 += cm * cn * self.P * (dxyzdnt[0][0] * dxyzdnt[1][1] - dxyzdnt[1][0] * dxyzdnt[0][1]) * psi_i

                    gauss_i += 1

            fe[face_idxs[i]] = f1
            fe[face_idxs[i] + 20] = f2
            fe[face_idxs[i] + 40] = f3

        return fe

    def _MG(self, MGE):
        MG = np.zeros((3 * self.nqp, 3 * self.nqp)).tolist()

        for mge_idx, mge in enumerate(MGE):
            for i in range(60):
                for j in range(60):
                    mg_i = self.NT[mge_idx][i % 20] * 3 + (i // 20)
                    mg_j = self.NT[mge_idx][j % 20] * 3 + (j // 20)
                    MG[mg_i][mg_j] += mge[i][j]

        for elem_id, face_id in self.ZU:
            el = self.finite_elements[elem_id]
            for local_point in face_id_idxs[face_id]:
                point = self.NT[elem_id][local_point]
                ix = 3 * point + 0
                iy = 3 * point + 1
                iz = 3 * point + 2
                MG[ix][ix] = float(10 ** 50)
                MG[iy][iy] = float(10 ** 50)
                MG[iz][iz] = float(10 ** 50)

        return MG

    def _F(self, FE):
        F = np.zeros((self.nqp * 3)).tolist()

        for fe_idx, fe in enumerate(FE):
            for i in range(60):
                f_idx = self.NT[fe_idx][i % 20] * 3 + (i // 20)
                F[f_idx] += fe[i]

        return F
