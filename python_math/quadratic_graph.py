from matplotlib import pyplot as plt


def draw_graph(start, final):
    x = list(range(start, final + 1))
    y = [x ** 2 + 2 * x + 1 for x in range(start, final + 1)]
    plt.plot(x, y)
    plt.xlabel('x-coordinate')
    plt.ylabel('y-coordinate')


if __name__ == '__main__':
    draw_graph(-100, 100)
    plt.show()

