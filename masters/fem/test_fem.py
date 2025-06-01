import unittest
from fem import FEM  # adjust the import path if needed

import numpy as np


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



if __name__ == "__main__":
    unittest.main()
