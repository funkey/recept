import numpy as np
import pandas as pd
import copy


class Events:

    def __init__(self, df):

        self.time = np.array(df['time'], dtype=np.int64)
        self.x = df['x']
        self.y = df['y']
        self.pressure = df['pressure']
        if 'distance' in df:
            self.distance = df['distance']
        self.tilt_x = df['tilt_x']
        self.tilt_y = df['tilt_y']
        self.speed_x = None
        self.speed_y = None

    @property
    def has_speed(self):
        return self.speed_x is not None and self.speed_y is not None

    def copy(self):
        return copy.deepcopy(self)

def read_events(filename):

    df = pd.read_csv(filename)
    return Events(df)
