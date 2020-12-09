from evaluate import evaluate
from events import read_events
from filter import smooth, kalman_filter
import sys


if __name__ == '__main__':

    filename = sys.argv[1]

    events = read_events(filename)

    gold_standard = smooth(events, 7, 5)
    mean_filtered = smooth(events, 0, 15, center=False)
    kalman_filtered = kalman_filter(events, 0.01, 100.0)

    evaluate(mean_filtered, gold_standard)
    evaluate(kalman_filtered, gold_standard, show_plot=True)
