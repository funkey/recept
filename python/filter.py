from kalman_filter import KalmanFilter
from scipy import ndimage
import numpy as np


def moving_average(raw, window_size, center=True):

    if center:
        origin = 0
    else:
        origin = window_size//2 - (1 - window_size % 2)

    return ndimage.uniform_filter(
        raw,
        size=window_size,
        mode='nearest',
        origin=origin)


def moving_median(raw, window_size, center=True):

    if center:
        origin = 0
    else:
        origin = window_size//2 - (1 - window_size % 2)

    return ndimage.median_filter(
        raw,
        size=window_size,
        mode='nearest',
        origin=origin)


def smooth(events, median_window_size, mean_window_size, center=True):
    '''If center is False, perform smoothing in the past.'''

    smoothed = events.copy()

    if median_window_size > 0:
        smoothed.x = moving_median(smoothed.x, median_window_size, center)
        smoothed.y = moving_median(smoothed.y, median_window_size, center)

    smoothed.x = moving_average(smoothed.x, mean_window_size, center)
    smoothed.y = moving_average(smoothed.y, mean_window_size, center)

    return smoothed


def kalman_1d(time, raw, sigma_x, sigma_z, outlier_distance=None):

    kalman = KalmanFilter(sigma_x, sigma_z, outlier_distance)

    ret = np.stack(
        [
            kalman.step(raw[i], time[i] - time[max(0, i - 1)])
            for i in range(len(raw))
        ])

    # position, speed, MD
    return ret[:, 0], ret[:, 1]  # , ret[:, 2]


def kalman_filter(events, sigma_x, sigma_z, outlier_distance=None):

    kalman_filtered = events.copy()

    kalman_filtered.x, kalman_filtered.speed_x = kalman_1d(
        kalman_filtered.time,
        kalman_filtered.x,
        sigma_x, sigma_z,
        outlier_distance)
    kalman_filtered.y, kalman_filtered.speed_y = kalman_1d(
        kalman_filtered.time,
        kalman_filtered.y,
        sigma_x, sigma_z)

    return kalman_filtered
