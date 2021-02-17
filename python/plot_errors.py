from recept import read_events, smooth
import sys
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':

    filename = sys.argv[1]

    events = read_events(filename)
    gold_standard = smooth(events, 7, 5)
    gold_standard.compute_speed_acceleration()

    diff_x = events.x - gold_standard.x
    diff_y = events.y - gold_standard.y
    speed = np.sqrt(gold_standard.speed_x**2 + gold_standard.speed_y**2)

    fig, axs = plt.subplots(2, 3, tight_layout=True)
    axs[0, 0].hist(diff_x, bins=100)
    axs[1, 0].hist(diff_y, bins=100)

    axs[0, 1].scatter(gold_standard.speed_y, diff_x, alpha=0.1)
    axs[1, 1].scatter(gold_standard.speed_x, diff_y, alpha=0.1)

    axs[0, 2].plot(gold_standard.acceleration_x)
    axs[1, 2].plot(gold_standard.acceleration_y)

    plt.show()
