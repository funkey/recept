from plot import plot_matches
from match import match


def evaluate(filtered, gold_standard, show_plot=False):

    matches = match(filtered, gold_standard)

    print(f"mean distance²: {matches.mean_distance_squared()}")
    print(f"mean distance : {matches.mean_distance()}")
    print(f"max distance  : {matches.max_distance()}")
    print(f"mean latency  : {matches.mean_latency()}")
    print()

    if show_plot:
        plot_matches(filtered, gold_standard, matches)

    return matches.mean_distance(), matches.mean_latency()
