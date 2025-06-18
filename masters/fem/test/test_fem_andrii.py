import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import unittest
from fem import FEM

import numpy as np
import numpy.testing as npt

import csv


def read_csv_and_round(file_path, round_to):
    data = []
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            rounded_row = [round(float(value), round_to) for value in row]
            data.append(rounded_row)
    return data


class TestFEM_FromAndrii(unittest.TestCase):
    def test_dfiabg(self):
        fem = FEM(1,1,1,1,1,1,1,0.3,1)
        fem.calc()
        dfiabg = np.array(fem.DFIABG)

        round_to = 5

        expected_data = read_csv_and_round('dfiabg_1.csv', round_to)

        # flatten fem.DFIABG
        dfiabg_flat = dfiabg.reshape(-1, 3)
        dfiabg_flat = np.round(dfiabg_flat, round_to)

        npt.assert_array_equal(dfiabg_flat, expected_data)


    def test_jakobians(self):
        fem = FEM(1,1,1,2,2,2,1,0.3,1)
        fem.calc()
        print(len(fem.DXYZABG))
        print(np.array(fem.DXYZABG).shape)
        print(np.array(fem.DXYZABG))


if __name__ == "__main__":
    unittest.main()
