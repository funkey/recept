from recept import evaluate, read_events, smooth, kalman_filter
import sys


if __name__ == '__main__':

    filename = sys.argv[1]
    mean_filter_size = 16
    sigma_x = 0.00001
    sigma_z = 100.0

    events = read_events(filename)

    gold_standard = smooth(events, 7, 5)
    mean_filtered = smooth(events, 0, mean_filter_size, center=False)
    kalman_filtered = kalman_filter(events, sigma_x, sigma_z, only_x=True)

    print()
    print(f"Baseline (mean filtered with size {mean_filter_size}):")
    evaluate(mean_filtered, gold_standard)
    print()
    print(f"Kalman filtered (sigma_x={sigma_x}, sigma_z={sigma_z}):")
    evaluate(kalman_filtered, gold_standard, show_plot=True, show_events=events)
