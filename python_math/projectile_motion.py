from math import sin, cos, radians
from matplotlib import pyplot as plt


def draw_graph(x, y):
    plt.plot(x, y)
    plt.xlabel('x-coordinate')
    plt.ylabel('y-coordinate')
    plt.title('Projectile motion of a ball')


def frange(start, final, interval):
    l = []
    while start < final:
        l.append(start)
        start += interval
    return l


def draw_trajectory(u, theta):
    theta = radians(theta)
    g = 9.8
    t_flight = 2 * u * sin(theta) / g
    intervals = frange(0, t_flight, 0.001)
    x = [u * cos(theta) * t for t in intervals]
    y = [u * sin(theta) * t - 0.5 * g * t ** 2 for t in intervals]
    draw_graph(x, y)


if __name__ == '__main__':
    us = [20, 40, 60]
    theta = 45
    for u in us:
        draw_trajectory(u, theta)
    plt.legend(us)
    plt.show()
