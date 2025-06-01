import numpy as np

class FEM():
    def __init__(self, ax, ay, az, nx, ny, nz):
        self.ax = ax
        self.ay = ay
        self.az = az
        self.nx = nx
        self.ny = ny
        self.nz = nz

    def mesh(self):
        AKT = []
        x_scale = (self.ax / self.nx) / 2
        y_scale = (self.ay / self.ny) / 2
        z_scale = (self.az / self.nz) / 2
        for iz in range(self.nz * 2 + 1):
            y_step = 1 + (iz % 2)
            for iy in range(0, self.ny * 2 + 1, y_step):
                x_step = 1 + ((iy + iz) % 2)
                for ix in range(0, self.nx * 2 + 1, x_step):
                    AKT.append([ix*x_scale, iy*y_scale, iz*z_scale])

        self.AKT = AKT
        self.nqp = len(AKT)
