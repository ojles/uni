import unittest
from fem import FEM  # adjust the import path if needed

import numpy as np
import math


def mesh_reference_function(a, b, c, na, nb, nc):
    result = []
    step_a = a / na
    step_b = b / nb
    step_c = c / nc
    for k in range(2 * nc + 1):
        if k % 2 == 0:
            for j in range(2 * nb + 1):
                if j % 2 == 0:
                    for i in range(2 * na + 1):
                        result.append([i * step_a / 2, j * step_b / 2, k * step_c / 2])
                else:
                    for i in range(na + 1):
                        result.append([i * step_a, j * step_b / 2, k * step_c / 2])
        else:
            for j in range(nb + 1):
                for i in range(na + 1):
                    result.append([i * step_a, j * step_b, k * step_c / 2])
    return result


class TestFEM(unittest.TestCase):
    def test_init(self):
        fem = FEM(1,2,3,4,5,6)  # Create an instance (adjust args if needed)
        self.assertIsInstance(fem, FEM)  # Check the object type

    def test_mesh_1(self):
        fem = FEM(2, 2, 3, 1, 1, 2)
        fem.mesh()
        actual_mesh = np.array(fem.AKT)

        expected_mesh = np.array([
            [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [2.0, 0.0, 0.0],
            [0.0, 1.0, 0.0], [2.0, 1.0, 0.0], [0.0, 2.0, 0.0],
            [1.0, 2.0, 0.0], [2.0, 2.0, 0.0], [0.0, 0.0, 0.75],
            [2.0, 0.0, 0.75], [0.0, 2.0, 0.75], [2.0, 2.0, 0.75],
            [0.0, 0.0, 1.5], [1.0, 0.0, 1.5], [2.0, 0.0, 1.5],
            [0.0, 1.0, 1.5], [2.0, 1.0, 1.5], [0.0, 2.0, 1.5],
            [1.0, 2.0, 1.5], [2.0, 2.0, 1.5], [0.0, 0.0, 2.25],
            [2.0, 0.0, 2.25], [0.0, 2.0, 2.25], [2.0, 2.0, 2.25],
            [0.0, 0.0, 3.0], [1.0, 0.0, 3.0], [2.0, 0.0, 3.0],
            [0.0, 1.0, 3.0], [2.0, 1.0, 3.0], [0.0, 2.0, 3.0],
            [1.0, 2.0, 3.0], [2.0, 2.0, 3.0]])

        assert actual_mesh.shape == expected_mesh.shape, \
            f"Shape mismatch: {actual_mesh.shape} vs {expected_mesh.shape}"

        np.testing.assert_array_equal(actual_mesh, expected_mesh)

    def test_mesh_2(self):
        fem = FEM(4, 10, 20, 3, 5, 10)
        fem.mesh()
        actual_mesh = np.array(fem.AKT)

        expected_mesh = np.array(mesh_reference_function(4, 10, 20, 3, 5, 10))

        assert actual_mesh.shape == expected_mesh.shape, \
            f"Shape mismatch: {actual_mesh.shape} vs {expected_mesh.shape}"

        np.testing.assert_array_equal(actual_mesh, expected_mesh)

    def test_dPhi_dAlpha_1(self):
        fem = FEM(1, 1, 1, 1, 1, 1)

        alpha = 1
        beta = 2
        gamma = 3
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                for k in [-1, 0, 1]:
                    alpha_i = i
                    beta_i = j
                    gamma_i = k
                    result = fem._dPhi_dAlpha_1(alpha, beta, gamma, alpha_i, beta_i, gamma_i)
                    expected_result = (1 / 8) * (1 + beta * beta_i) * (1 + gamma * gamma_i) \
                            * (alpha_i * (-2 + alpha * alpha_i + gamma * gamma_i + beta * beta_i) \
                            + alpha_i * (1 + alpha * alpha_i))
                    assert result == expected_result, \
                            "Failed to calculate _dPhi_dAlpha_1"

    def test_dPhi_dBeta_1(self):
        fem = FEM(1, 1, 1, 1, 1, 1)

        alpha = 1
        beta = 2
        gamma = 3
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                for k in [-1, 0, 1]:
                    alpha_i = i
                    beta_i = j
                    gamma_i = k
                    result = fem._dPhi_dBeta_1(alpha, beta, gamma, alpha_i, beta_i, gamma_i)
                    expected_result = (1 / 8) * (1 + alpha * alpha_i) * (1 + gamma * gamma_i) \
                            * (beta_i * (-2 + alpha * alpha_i + gamma * gamma_i + beta * beta_i) \
                            + beta_i * (1 + beta * beta_i))
                    assert result == expected_result, \
                            "Failed to calculate _dPhi_dBeta_1"


    def test_dPhi_dGamma_1(self):
        fem = FEM(1, 1, 1, 1, 1, 1)

        alpha = 1
        beta = 2
        gamma = 3
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                for k in [-1, 0, 1]:
                    alpha_i = i
                    beta_i = j
                    gamma_i = k
                    result = fem._dPhi_dGamma_1(alpha, beta, gamma, alpha_i, beta_i, gamma_i)
                    expected_result = (1 / 8) * (1 + beta * beta_i) * (1 + alpha * alpha_i) \
                            * (gamma_i * (-2 + alpha * alpha_i + gamma * gamma_i + beta * beta_i) \
                            + gamma_i * (1 + gamma * gamma_i))
                    assert result == expected_result, \
                            "Failed to calculate _dPhi_dGamma_1"

    def test_DFIABG(self):
        # Expected functions ====================================================
        nol_shist = math.sqrt(0.6)
        alpha_for = [-nol_shist, 0, nol_shist]
        beta_for = [-nol_shist, 0, nol_shist]
        gamma_for = [-nol_shist, 0, nol_shist]
        local_points = [
            [-1, 1, -1],  # 1
            [1, 1, -1],  # 2
            [1, -1, -1],  # 3
            [-1, -1, -1],  # 4
            [-1, 1, 1],  # 5
            [1, 1, 1],  # 6
            [1, -1, 1],  # 7
            [-1, -1, 1],  # 8
            [0, 1, -1],  # 9
            [1, 0, -1],  # 10
            [0, -1, -1],  # 11
            [-1, 0, -1],  # 12
            [-1, 1, 0],  # 13
            [1, 1, 0],  # 14
            [1, -1, 0],  # 15
            [-1, -1, 0],  # 16
            [0, 1, 1],  # 17
            [1, 0, 1],  # 18
            [0, -1, 1],  # 19
            [-1, 0, 1]  # 20
        ]
        def DFIABG_Create():
            result = []
            for gamma in gamma_for:
                for beta in beta_for:
                    for alpha in alpha_for:
                        a = []
                        for point in local_points:
                            if local_points.index(point) > 7:
                                a.append(DFIABD_center_side(alpha, beta, gamma, point[0], point[1], point[2]))
                            else:
                                a.append(DFIABD_angle(alpha, beta, gamma, point[0], point[1], point[2]))
                        result.append(a)
            return result

        def DFIABD_angle(alpha, beta, gamma, alpha_i, beta_i, gamma_i):
            result = [
                (1 / 8) * (1 + beta * beta_i) * (1 + gamma * gamma_i) *
                (alpha_i * (-2 + alpha * alpha_i + gamma * gamma_i + beta * beta_i) + alpha_i * (1 + alpha * alpha_i)),

                (1 / 8) * (1 + alpha * alpha_i) * (1 + gamma * gamma_i) *
                (beta_i * (-2 + alpha * alpha_i + gamma * gamma_i + beta * beta_i) + beta_i * (1 + beta * beta_i)),

                (1 / 8) * (1 + beta * beta_i) * (1 + alpha * alpha_i) *
                (gamma_i * (-2 + alpha * alpha_i + gamma * gamma_i + beta * beta_i) + gamma_i * (1 + gamma * gamma_i))
            ]
            return result

        def DFIABD_center_side(alpha, beta, gamma, alpha_i, beta_i, gamma_i):
            result = [
                (1 / 4) * (1 + beta * beta_i) * (1 + gamma * gamma_i) *
                (alpha_i * (
                        -beta_i * beta_i * gamma_i * gamma_i * alpha * alpha
                        - beta * beta * gamma_i * gamma_i * alpha_i * alpha_i
                        - beta_i * beta_i * gamma * gamma * alpha_i * alpha_i + 1) -
                 (2 * beta_i * beta_i * gamma_i * gamma_i * alpha) * (alpha * alpha_i + 1)),

                (1 / 4) * (1 + alpha * alpha_i) * (1 + gamma * gamma_i) *
                (beta_i * (
                        -beta_i * beta_i * gamma_i * gamma_i * alpha * alpha
                        - beta * beta * gamma_i * gamma_i * alpha_i * alpha_i
                        - beta_i * beta_i * gamma * gamma * alpha_i * alpha_i + 1) -
                 (2 * beta * gamma_i * gamma_i * alpha_i * alpha_i) * (beta_i * beta + 1)),

                (1 / 4) * (1 + beta * beta_i) * (1 + alpha * alpha_i) *
                (gamma_i * (
                        -beta_i * beta_i * gamma_i * gamma_i * alpha * alpha
                        - beta * beta * gamma_i * gamma_i * alpha_i * alpha_i
                        - beta_i * beta_i * gamma * gamma * alpha_i * alpha_i + 1) -
                 (2 * beta_i * beta_i * gamma * alpha_i * alpha_i) * (gamma * gamma_i + 1))
            ]

            return result
        # Expected functions END ================================================

        fem = FEM(1, 1, 1, 1, 1, 1)
        fem.mesh()

        result = np.array(fem.DFIABG)
        expected_result = np.array(DFIABG_Create())

        assert result.shape == expected_result.shape, \
            f"Shape mismatch: {result.shape} vs {expected_result.shape}"

        np.testing.assert_array_equal(result, expected_result)

    def test_DXYZABG(self):
        def DExyzDEabg(xyz, dfiabj):
            result = []
            for i in range(27):
                summ_x_a = []
                summ_x_b = []
                summ_x_g = []
                summ_y_a = []
                summ_y_b = []
                summ_y_g = []
                summ_z_a = []
                summ_z_b = []
                summ_z_g = []
                for point in xyz:
                    index_of_nt = xyz.index(point)
                    summ_x_a.append(point[0] * dfiabj[i][index_of_nt][0])
                    summ_x_b.append(point[0] * dfiabj[i][index_of_nt][1])
                    summ_x_g.append(point[0] * dfiabj[i][index_of_nt][2])

                    summ_y_a.append(point[1] * dfiabj[i][index_of_nt][0])
                    summ_y_b.append(point[1] * dfiabj[i][index_of_nt][1])
                    summ_y_g.append(point[1] * dfiabj[i][index_of_nt][2])

                    summ_z_a.append(point[2] * dfiabj[i][index_of_nt][0])
                    summ_z_b.append(point[2] * dfiabj[i][index_of_nt][1])
                    summ_z_g.append(point[2] * dfiabj[i][index_of_nt][2])
                result.append([
                    [sum(summ_x_a), sum(summ_y_a), sum(summ_z_a)],
                    [sum(summ_x_b), sum(summ_y_b), sum(summ_z_b)],
                    [sum(summ_x_g), sum(summ_y_g), sum(summ_z_g)],
                ])
            return result

        fem = FEM(2, 2, 3, 1, 1, 2)
        fem.mesh()
        f_elem = fem.finite_elements[0]

        result = np.array(fem._DXYZABG(f_elem))
        expected_result = np.array(DExyzDEabg(f_elem, fem.DFIABG))

        assert result.shape == expected_result.shape, \
            f"Shape mismatch: {result.shape} vs {expected_result.shape}"

        np.testing.assert_array_equal(result, expected_result)




if __name__ == "__main__":
    unittest.main()
