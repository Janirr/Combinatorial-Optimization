import sys
import random


def writeToFile(matrix):
    print(matrix)


def randomGraph(n, max_value=1000):
    edges = []
    max_edges = n * (n - 1)
    for i in range(n):
        for j in range(n):
            if i != j:
                edge = [i + 1, j + 1]
                edges.append(edge)
    # We are removing one by one values in reversed but sorted order.
    random_list = random.sample(range(1, max_edges), n)
    sorted_tab = edges
    graph = [[0] * n for _ in range(n)]
    for j in range(len(sorted_tab)):
        x = sorted_tab[j][0] - 1
        y = sorted_tab[j][1] - 1
        d = random.randint(1, max_value)
        graph[x][y] = d
        graph[y][x] = d
    return graph
