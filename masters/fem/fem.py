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

sqrt06 = math.sqrt(0.6)

gauss_points_3d = []
for gamma in [-sqrt06, 0, sqrt06]:
    for beta in [-sqrt06, 0, sqrt06]:
        for alpha in [-sqrt06, 0, sqrt06]:
            gauss_points_3d.append([alpha, beta, gamma])

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
        [3, 2, 1, 0, 10, 9, 8, 11],    # bottom
        [5, 6, 7, 4, 17, 18, 19, 16],  # top
        [0, 1, 5, 4, 8, 13, 16, 12],   # front
        [2, 3, 7, 6, 10, 15, 18, 14],  # back
        [3, 0, 4, 7, 11, 12, 19, 15],  # left
        [1, 2, 6, 5, 9, 14, 17, 13]    # right
    ]


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
        print("AKT")
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
        #for nt in self.NT:
            #for el in nt:
                #print(el, ",", sep="", end="")
            #print()

    def calc(self, E, nu, P, zp, zu):
        if len(self.AKT) == 0:
            self.mesh()

        self.set_params(E, nu, P)

        self.ZU = zu
        self.ZP = zp

        self.DFIABG = self._DFIABG(gauss_points_3d)
        print("fem: DFIABG done.")

        self.DPSITE = self._DPSITE()
        print("fem: DPSITE done.")

        self.DXYZABG = []
        len_felem = len(self.finite_elements)
        for fidx, f_elem in enumerate(self.finite_elements):
            print(f"fem: DXYZABG el ({fidx}/{len_felem})")
            self.DXYZABG.append(self._DXYZABG(f_elem, self.DFIABG))
        print("fem: DXYZABG done.")

        self.DJ = []
        for dxyzabg in self.DXYZABG:
            self.DJ.append(self._DJ(dxyzabg))

        self.DFIXYZ = []
        for elem_idx, _ in enumerate(self.finite_elements):
            print(f"fem: DFIXYZ el ({elem_idx}/{len_felem})")
            self.DFIXYZ.append(self._DFIXYZ(elem_idx, self.DXYZABG, self.DFIABG))
        print("fem: DFIXYZ done.")

        self.MGE = []
        for el_idx, _ in enumerate(self.finite_elements):
            print(f"fem: MGE el ({el_idx}/{len_felem})")
            self.MGE.append(self._MGE(el_idx))
        #for mge in self.MGE[0]:
            #for x in mge:
                #print(x, ",", end="")
            #print()
        print("fem: MGE done.")

        FE = []
        for _ in range(len_felem):
            FE.append(np.zeros(60).tolist())
        for elem_id, face_id in self.ZP:
            FE[elem_id] = self._FE(self.finite_elements[elem_id], face_id)
        print("fem: FE done.")

        MG = self._MG(self.MGE)
        print("fem: MG done.")

        F = self._F(FE)
        print("fem: F done.")

        self.u = np.linalg.solve(MG, F)
        print("fem: Solved.")

        print("")
        print("fem: Calc stress..")
        self.DFIABG_Local = self._DFIABG(local_coords)
        print("fem: DFIABG(local) done.")

        self.DXYZABG_Local = []
        for fidx, f_elem in enumerate(self.finite_elements):
            print(f"fem: DXYZABG(local) el ({fidx}/{len_felem})")
            self.DXYZABG_Local.append(self._DXYZABG(f_elem, self.DFIABG_Local))
        print("fem: DXYZABG(local) done.")

        self.DFIXYZ_Local = []
        for elem_idx, _ in enumerate(self.finite_elements):
            print(f"fem: DFIXYZ(local) el ({elem_idx}/{len_felem})")
            self.DFIXYZ_Local.append(self._DFIXYZ(elem_idx, self.DXYZABG_Local, self.DFIABG_Local))
        print("fem: DFIXYZ(local) done.")

        self.DUXYZ = []
        for elem_idx, _ in enumerate(self.finite_elements):
            self.DUXYZ.append(self._DUXYZ(elem_idx, self.DFIXYZ_Local))
        print("fem: DUXYZ(local) done.")

        self.SIGMA_Comp = []
        for elem_idx, _ in enumerate(self.finite_elements):
            self.SIGMA_Comp.append(self._SIGMA_Comp(el_idx))
        print("fem: SIGMA_Comp(local) done.")

        self.J123 = []
        for elem_idx, _ in enumerate(self.finite_elements):
            self.J123.append(self._J123(el_idx))

        self.SIGMA = []
        for elem_idx, _ in enumerate(self.finite_elements):
            self.SIGMA.append(self._SIGMA(el_idx, self.J123[el_idx]))

        self.stress = self._stress()
        for si, s in enumerate(self.stress):
            print(si, ":", s)
        print(np.min(self.stress))
        print(np.max(self.stress))



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

    def _DFIABG(self, points):
        DFIABG = []
        for p in points:
            el = []
            for i, abg_i in enumerate(local_coords):
                if i <= 7:
                    el.append([
                        self._dPhi_dAlpha_1(p[0], p[1], p[2], abg_i[0], abg_i[1], abg_i[2]),
                        self._dPhi_dBeta_1( p[0], p[1], p[2], abg_i[0], abg_i[1], abg_i[2]),
                        self._dPhi_dGamma_1(p[0], p[1], p[2], abg_i[0], abg_i[1], abg_i[2])])
                else:
                    el.append([
                        self._dPhi_dAlpha_2(p[0], p[1], p[2], abg_i[0], abg_i[1], abg_i[2]),
                        self._dPhi_dBeta_2( p[0], p[1], p[2], abg_i[0], abg_i[1], abg_i[2]),
                        self._dPhi_dGamma_2(p[0], p[1], p[2], abg_i[0], abg_i[1], abg_i[2])])
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

    def _DXYZABG(self, el, dfiabg):
        DXYZABG = []
        for i in range(len(dfiabg)):
            #   [dx/da, dy/da, dz/da]
            #   [dx/db, dy/db, dz/db]
            #   [dx/dg, dy/dg, dz/dg]
            j = [[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]
            for point_idx, point in enumerate(el):
                for abg_i in range(3):
                    for xyz_i in range(3):
                        j[abg_i][xyz_i] += point[xyz_i] * dfiabg[i][point_idx][abg_i]
            DXYZABG.append(j)
        return DXYZABG

    def _DFIXYZ(self, elem_idx, dxyzabg, dfiabg):
        DFIXYZ = []
        for i in range(len(dfiabg)):
            dfixyz = []
            for phi_i_abg in dfiabg[i]:
                x = np.linalg.solve(dxyzabg[elem_idx][i], phi_i_abg).tolist()
                dfixyz.append(x)
            DFIXYZ.append(dfixyz)
        return DFIXYZ

    def _DUXYZ(self, el_idx, dfixyz):
        DUXYZ = []
        for point_idx in range(len(dfixyz[el_idx])):
            #   [du_x/dx, du_x/dy, du_x/dz]
            #   [du_y/dx, du_y/dy, du_y/dz]
            #   [du_z/dx, du_z/dy, du_z/dz]
            du = [[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]

            for pi in range(len(self.NT[el_idx])):
                for du_xyz in range(3):
                    for d_xyz in range(3):
                        du[du_xyz][d_xyz] += self.u[self.NT[el_idx][pi]*3+du_xyz] * dfixyz[el_idx][point_idx][pi][d_xyz]

            DUXYZ.append(du)

        return DUXYZ

    def _SIGMA_Comp(self, el_idx):
        SIGMA_Comp = []
        for p in range(len(self.NT[el_idx])):
            s_xx = self.lambda_ * ((1 - self.nu) * self.DUXYZ[el_idx][p][0][0] + self.nu * (self.DUXYZ[el_idx][p][1][1] + self.DUXYZ[el_idx][p][2][2]))
            s_yy = self.lambda_ * ((1 - self.nu) * self.DUXYZ[el_idx][p][1][1] + self.nu * (self.DUXYZ[el_idx][p][0][0] + self.DUXYZ[el_idx][p][2][2]))
            s_zz = self.lambda_ * ((1 - self.nu) * self.DUXYZ[el_idx][p][2][2] + self.nu * (self.DUXYZ[el_idx][p][0][0] + self.DUXYZ[el_idx][p][1][1]))
            s_xy = self.mu * (self.DUXYZ[el_idx][p][0][1] + self.DUXYZ[el_idx][p][1][0])
            s_yz = self.mu * (self.DUXYZ[el_idx][p][1][2] + self.DUXYZ[el_idx][p][2][1])
            s_xz = self.mu * (self.DUXYZ[el_idx][p][0][2] + self.DUXYZ[el_idx][p][2][0])
            SIGMA_Comp.append([s_xx, s_yy, s_zz, s_xy, s_yz, s_xz])
        return SIGMA_Comp

    def _J123(self, el_idx):
        J123 = []
        for p in range(len(self.NT[el_idx])):
            s_xx = self.SIGMA_Comp[el_idx][p][0]
            s_yy = self.SIGMA_Comp[el_idx][p][1]
            s_zz = self.SIGMA_Comp[el_idx][p][2]
            s_xy = self.SIGMA_Comp[el_idx][p][3]
            s_yz = self.SIGMA_Comp[el_idx][p][4]
            s_xz = self.SIGMA_Comp[el_idx][p][5]
            J123.append([s_xx + s_yy + s_zz,
                         s_xx*s_yy + s_yy*s_zz + s_xx*s_zz - (s_xy*s_xy + s_yz*s_yz + s_xz*s_xz),
                         s_xx*s_yy*s_zz + 2*s_xy*s_xz*s_yz - (s_xx*s_yz*s_yz + s_yy*s_xz*s_xz + s_zz*s_xy*s_xy)])
        return J123

    def _SIGMA(self, el_idx, j123):
        sigma = []
        for p in range(len(self.NT[el_idx])):
            coefficients = [1, -j123[p][0], j123[p][1], -j123[p][2]]
            roots = np.roots(coefficients)
            real_roots = [r.real for r in roots if np.isclose(r.imag, 0)]
            sigma.append(real_roots)
        return sigma

    def _stress(self):
        stress = np.zeros(self.nqp).tolist()
        stress_values = np.zeros((self.nqp, 10)).tolist()
        stress_count = np.zeros(self.nqp).tolist()
        for elem_idx, _ in enumerate(self.finite_elements):
            for p_idx, p in enumerate(self.NT[elem_idx]):
                if len(self.SIGMA[elem_idx][p_idx]) == 1:
                    stress[p] += self.SIGMA[elem_idx][p_idx][-1]
                    stress_values[p][int(stress_count[p])] = self.SIGMA[elem_idx][p_idx][-1]
                else:
                    stress[p] += self.SIGMA[elem_idx][p_idx][-1]
                    stress_values[p][int(stress_count[p])] = self.SIGMA[elem_idx][p_idx][-1]
                stress_count[p] += 1

        for s_idx, _ in enumerate(stress):
            stress[s_idx] /= stress_count[s_idx]

        #print(stress_values)

        return stress



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
                [a12.T, a22, a23],
                [a13.T, a23.T, a33]
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
                    #print(mge_idx, ",", mg_i, ",", mg_j, ",", i, ",", j, ",", MG[mg_i][mg_j], sep="")

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
