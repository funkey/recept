from evaluate import evaluate
from events import read_events
from filter import smooth, kalman_filter
import numpy as np
import sys


if __name__ == '__main__':

    filename = sys.argv[1]

    events = read_events(filename)

    gold_standard = smooth(events, 7, 5)
    mean_filtered = smooth(events, 0, 15, center=False)

    baseline_distance, baseline_latency = evaluate(
        mean_filtered,
        gold_standard)

    best_kalman = None
    best_score = None
    best_distance = None
    best_latency = None

    for sigma_x in np.arange(0.001, 0.01, 0.001):
        for sigma_z in np.arange(1.0, 20.0, 1.0):

            kalman_filtered = kalman_filter(events, sigma_x, sigma_z)

            print(f"Testing Kalman filter with {sigma_x} {sigma_z}")
            distance, latency = evaluate(kalman_filtered, gold_standard)

            score = distance*latency
            if best_score is None or score < best_score:
                best_score = score
                best_distance = distance
                best_latency = latency
                best_kalman = (sigma_x, sigma_z)

    print(f"Best Kalman is {best_kalman} with:")
    print(f"mean distance : {best_distance}")
    print(f"mean latency  : {best_latency}")
    print()
    print("Baseline (mean filter):")
    print(f"mean distance : {baseline_distance}")
    print(f"mean latency  : {baseline_latency}")
