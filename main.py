import itertools
import sys
import random
import time


def isSafe(matrix, v, path, pos):
    if matrix[path[pos - 1]][v] == 0:
        return False
    for i in range(pos):
        if path[i] == v:
            return False
    return True


def readFile(file_name):
    try:
        f = open(file_name)
    except OSError:
        print("Could not open/read file:", file_name)
        sys.exit()
    n = int(f.readline())
    tmp_tab = []
    for i in range(n):
        connection = list(map(int, f.readline().split(" ")))
        tmp_tab.append(connection)
    f.close()
    return tmp_tab


def DFSsolution(matrix):
    global minZ
    if len(matrix) > 0:
        z = 0
        path = [0]
        visited = [False] * (len(matrix))
        minZ = 9999
        for i in range(len(visited)):
            visited[i] = False
        visited[0] = True
        DFS(matrix, 1, path, visited, z)


def DFS(matrix, current_position, path, visited, z):
    global minZ
    n = len(matrix)
    if current_position == len(matrix):
        if matrix[path[-1]][path[0]] != 0:
            z += matrix[0][path[-1]]
            path.append(0)
            if z < minZ and len(path) > n:
                minZ = z
                print(path, z)
            z -= matrix[0][path[-1]]
            path.pop()
    for v in range(len(matrix)):
        if isSafe(matrix, v, path, current_position) and not visited[v]:
            z += matrix[v][path[-1]]
            path.append(v)
            visited[v] = True
            DFS(matrix, current_position + 1, path, visited, z)
            visited[v] = False
            z -= matrix[v][path[-1]]
            path.pop()
            z -= matrix[v][path[-1]]


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


def nearestNeighbour(matrix):
    path = [0]
    valuePaths = []
    visited = [False] * (len(matrix))
    visited[0] = True
    minIndex = 0
    minValue = 9999
    z = 0
    i = 0
    for _ in range(len(matrix) - 1):
        for j in range(len(matrix)):
            if minValue > matrix[i][j] > 0 and not visited[j]:
                minIndex = j
                minValue = matrix[i][j]
        if minIndex != 0:
            path.append(minIndex)
            visited[minIndex] = True
            z += minValue
            valuePaths.append(minValue)
            i = minIndex
        minIndex = 0
        minValue = 9999
    if matrix[path[-1]][0] > 0 \
            and len(path) == len(visited) \
            and len(valuePaths) + 1 == len(visited):
        z += matrix[path[-1]][0]
        valuePaths.append(matrix[path[-1]][0])
        path.append(0)
        print(path, z)


def lowestEdge(matrix):
    n = len(matrix)
    tmp = []
    path = []
    visited = [[False, False] for _ in range(n)]
    z = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            if matrix[i][j] > 0:
                block = [matrix[i][j], i, j]
                tmp.append(block)
    tmp.sort()
    for i in range(len(tmp)):
        if visited[tmp[0][1]].count(True) < 2 and visited[tmp[0][2]].count(True) < 2:
            if visited[tmp[0][1]].count(True) == 1 and visited[tmp[0][2]].count(True) == 1:
                if len(path) == n - 1:
                    connection = [tmp[0][1], tmp[0][2]]
                    visited[tmp[0][1]][1] = True
                    visited[tmp[0][2]][1] = True
                    path.append(connection)
                    z += tmp[0][0]
            else:
                if len(path) < n - 1:
                    connection = [tmp[0][1], tmp[0][2]]
                    if visited[tmp[0][1]][0]:
                        visited[tmp[0][1]][1] = True
                    else:
                        visited[tmp[0][1]][0] = True
                    if visited[tmp[0][2]][0]:
                        visited[tmp[0][2]][1] = True
                    else:
                        visited[tmp[0][2]][0] = True
                    path.append(connection)
                    z += tmp[0][0]
        tmp.pop(0)
    if len(path) == n:
        print(path, z)


def bruteForce(matrix):
    n = len(matrix)
    pid = [l for l in range(n)]
    path = []
    z = 99999999
    for i in itertools.permutations(pid):
        i = list(i)
        s = 0
        for j in range(1, len(i)):
            s += matrix[i[j]][i[j - 1]]
        s += matrix[i[j]][i[0]]
        if s < z:
            z = s
            path = i
    return path, z


if __name__ == "__main__":
    for i in range(1, 2, 1):
        matrix = readFile("test")
        print("Brute force:", bruteForce(matrix))
        print("--- DFS ---")
        DFSsolution(matrix)
        print("--- NNA ---")
        nearestNeighbour(matrix)
        print("--- LEA ---")
        lowestEdge(matrix)
