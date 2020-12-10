import numpy as np
import pandas as pd
import copy


class Events:

    def __init__(self, df):

        self.time = np.array(df['time'], dtype=np.int64)
        self.x = np.array(df['x'])
        self.y = np.array(df['y'])
        self.pressure = df['pressure']
        if 'distance' in df:
            self.distance = df['distance']
        self.tilt_x = df['tilt_x']
        self.tilt_y = df['tilt_y']
        self.speed_x = None
        self.speed_y = None
        self.acceleration_x = None
        self.acceleration_y = None

    def compute_speed_acceleration(self):

        self.speed_x = np.concatenate([[0], self.x[1:] - self.x[:-1]])
        self.speed_y = np.concatenate([[0], self.y[1:] - self.y[:-1]])
        self.acceleration_x = np.concatenate([
            [0],
            self.speed_x[1:] - self.speed_x[:-1]])
        self.acceleration_y = np.concatenate([
            [0],
            self.speed_y[1:] - self.speed_y[:-1]])

    @property
    def has_speed(self):
        return self.speed_x is not None and self.speed_y is not None

    def copy(self):
        return copy.deepcopy(self)

def read_events(filename):

    df = pd.read_csv(filename)
    return Events(df)
