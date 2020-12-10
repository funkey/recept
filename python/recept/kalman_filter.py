import numpy as np
from numpy.linalg import inv


class KalmanFilter:

    def __init__(
            self,
            sigma_x,
            sigma_z=None,
            outlier_distance=None,
            std_z_window=16):

        self.sigma_x = sigma_x
        self.sigma_z = sigma_z
        self.outlier_distance = outlier_distance
        self.std_z_window = std_z_window
        self.skip_limit = 10
        self.skipped = 0
        self.float_t = np.float32

        self.x = None
        self.eye = np.array([
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ], dtype=self.float_t)
        self.H = np.array([
                [1, 0, 0]
            ], dtype=self.float_t)
        self.R = self.sigma_z

        self.z_errors = []

    def reset(self):

        self.x = None

    def step(self, z, delta_t_us):

        if self.x is None:

            self.x = np.array([z, 0, 0], dtype=self.float_t)
            self.P = np.array([
                    [1.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0],
                    [0.0, 0.0, 1.0]
                ], dtype=self.float_t)

            return np.array([z, 0, 0], dtype=self.float_t)

        delta_t_ms = delta_t_us/1000.0
        delta_t_ms_2 = delta_t_ms*delta_t_ms

        G = np.array([0.5*delta_t_ms_2, delta_t_ms, 1.0], dtype=self.float_t)
        self.Q = np.outer(G, G)
        self.Q *= self.sigma_x
        self.F = np.array([
                [1, delta_t_ms, 0.5*delta_t_ms_2],
                [0, 1,          delta_t_ms],
                [0, 0,          1]
            ], dtype=self.float_t)

        # predict
        self.x = self.F@self.x
        self.P = self.F@self.P@self.F.T + self.Q


        # prepare update
        e = z - self.H@self.x
        if self.sigma_z is None:
            self.z_errors.append(e)
            self.R = np.std(self.z_errors[-self.std_z_window:])**2
        Ree = self.H@self.P@self.H.T + self.R

        # compute Mahalanobis distance of z
        md = (np.sqrt(e*e)/Ree)[0, 0]

        if (
                self.outlier_distance is not None and
                self.skipped < self.skip_limit):

            if md > self.outlier_distance:
                # skip update
                self.skipped += 1
                return np.array([self.x[0], self.x[1], md])
        self.skipped = 0

        # update
        self.K = self.P@self.H.T@inv(Ree)
        self.x = self.x + self.K@e
        self.P = (self.eye - self.K@self.H)@self.P

        return np.array([self.x[0], self.x[1], md])
