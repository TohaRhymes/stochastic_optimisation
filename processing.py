import matplotlib.pyplot as plt
from numpy import genfromtxt
import numpy as np
import time
from random import randint


def generate_new_dataset(amount=200):
    array = []
    for i in range(amount):
        array.append([randint(0, 1500), randint(0, 1500)])
    name = f"tsp_coord_{str(int(time.time() * 100000))}.csv"
    np.savetxt(name, np.array(array), fmt='%i', delimiter=",")
    return name


def read_dataset(path_to_csv, indexes=False):
    data = genfromtxt(path_to_csv, delimiter=',')

    return np.array(data[:, indexes:])


def draw_way(data, title, length):
    x = data[:, 0:1].T[0]
    y = data[:, 1:2].T[0]

    fig, ax = plt.subplots(figsize=(10, 10))
    colors = ['#2300A8', '#00A658', 'aquamarine']

    for i in range(len(data) - 1):
        x1 = x[i]
        x2 = x[i + 1]
        y1 = y[i]
        y2 = y[i + 1]
        ax.plot([x1, x2], [y1, y1], c=colors[1])
        ax.plot([x2, x2], [y1, y2], c=colors[1])

    ax.scatter(x, y, alpha=0.7, c=colors[0], label=f'Length = {length}')
    ax.scatter(x[0], y[0], s=100, c=colors[2], label=f'Ends')
    ax.scatter(x[-1], y[-1], s=100, c=colors[2])
    x_min, x_max = min(x), max(x)
    x_diff = x_max - x_min
    y_min, y_max = min(y), max(y)
    y_diff = y_max - y_min
    ax.scatter(x_min - x_diff*0.05, y_min - y_diff*0.05, alpha=0)
    ax.scatter(x_max + x_diff*0.05, y_max + y_diff*0.05, alpha=0)

    # adds a title and axes labels
    ax.set_title(title, fontsize=20)
    leg = plt.legend(prop={'size': 17})

    plt.show()


def launching(path, method, method_name, iters=10000000, **params):
    data = read_dataset(path)
    start = time.time()
    new_data, new_len = method(data, iters=iters, **params)
    draw_way(new_data, method_name, new_len)
    print(f'{time.time() - start} sec')
