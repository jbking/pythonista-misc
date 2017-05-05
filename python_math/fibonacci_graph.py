import matplotlib.pyplot as plt


def draw_graph(final):
    if final <= 1:
        raise ValueError("specify number bigger than 1")
    
    fibonacci = [1, 1]
    for _ in range(final - 2):
        fibonacci.append(fibonacci[-1] + fibonacci[-2])

    ys = [fibonacci[x + 1] / fibonacci[x] for x in range(len(fibonacci) - 1)]
    
    plt.plot(range(final - 1), ys)
    plt.xlabel("No.")
    plt.ylabel("Ratio")
    plt.title("Ratio between consecutive Fibonacci numbers")
    

if __name__ == '__main__':
    draw_graph(100)
    plt.show()
