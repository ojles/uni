class FEM:
    def __init__(self):
        pass

    def mesh(self, ax, ay, az, nx, ny, nz):
        self.ax = ax
        self.ay = ay
        self.az = az

        self.nx = nx
        self.ny = ny
        self.nz = nz

    def calc(self, E, nu):
        self.E = E
        self.nu = nu
        self.lambda_ = E / ((1 + nu) * (1 - 2*nu))
        self.mu = E / (2 * (1 + nu))

