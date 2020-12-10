import matplotlib.pyplot as plt
import numpy as np


def plot_events(*events_list):

    for events in events_list:

        if events.has_speed:

            speed = np.sqrt(events.speed_x**2 + events.speed_y**2)
            size = 100*speed

        else:

            size = None

        plt.scatter(events.y, events.x, c=events.time, s=size)
        plt.plot(events.y, events.x)

        if events.has_speed:
            plt.quiver(
                events.y, events.x,
                events.speed_y, events.speed_x,
                angles='xy', scale_units='xy', scale=1.0)

    plt.show()


def plot_matches(events_a, events_b, matches, show_events=None):

    a_to_b = matches.indices
    distances = matches.distances
    latencies = matches.latencies

    match_x = events_b.x[a_to_b] - events_a.x
    match_y = events_b.y[a_to_b] - events_a.y
    same_time_x = events_b.x - events_a.x
    same_time_y = events_b.y - events_a.y

    if show_events is not None:
        plt.scatter(show_events.y, show_events.x, color='red', alpha=0.5)

    plt.scatter(events_a.y, events_a.x, c=latencies, s=distances*10)
    plt.plot(events_a.y, events_a.x, color='purple')
    plt.quiver(
        events_a.y, events_a.x,
        same_time_y, same_time_x,
        angles='xy', scale_units='xy', scale=1.0,
        color='gray',
        width=0.001)
    plt.quiver(
        events_a.y, events_a.x,
        match_y, match_x,
        angles='xy', scale_units='xy', scale=1.0,
        color='black',
        width=0.002)

    plt.scatter(events_b.y, events_b.x, color='orange')
    plt.plot(events_b.y, events_b.x, color='orange')

    plt.show()
