import numpy as np


class Matches:

    def __init__(self, indices, distances, latencies):

        self.indices = indices
        self.distances = distances
        self.latencies = latencies

    def mean_latency(self):
        return self.latencies.mean()

    def mean_distance(self):
        return np.sqrt(self.distances).mean()

    def mean_distance_squared(self):
        return self.distances.mean()

    def max_distance(self):
        return np.sqrt(self.distances.max())


def match(events_a, events_b, window_size=50*1000):

    # naive implementation: get all pairwise distances

    len_a = len(events_a.time)
    len_b = len(events_b.time)

    print("Calculating event distances...")
    x_a = np.repeat(events_a.x, len_b).reshape(-1, len_b)
    x_b = np.tile(events_b.x, len_a).reshape(len_a, -1)
    y_a = np.repeat(events_a.y, len_b).reshape(-1, len_b)
    y_b = np.tile(events_b.y, len_a).reshape(len_a, -1)

    t_a = np.repeat(events_a.time, len_b).reshape(-1, len_b)
    t_b = np.tile(events_b.time, len_a).reshape(len_a, -1)
    delta_t = t_a - t_b

    dist = (x_a - x_b)**2 + (y_a - y_b)**2

    # don't match to events outside of window
    dist[np.abs(delta_t) > window_size] = 1e10

    print("...done")

    print("Matching events...")
    indices = np.argmin(dist, axis=1)
    print("...done")

    distances = dist[range(len_a), indices]
    latencies = delta_t[range(len_a), indices]

    return Matches(indices, distances, latencies)
