import sys
import random


def isSafe(matrix, v, path, pos):
    if matrix[path[pos - 1]][v] == 0:
        return False
    for i in range(pos):
        if path[i] == v:
            return False
    return True


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


def nearestneighbour(matrix):
    path = [0]
    value_paths = []
    visited = [False] * (len(matrix))
    visited[0] = True
    min_j = 0
    min_value = 9999
    z = 0
    i = 0
    for _ in range(len(matrix) - 1):
        for j in range(len(matrix)):
            if min_value > matrix[i][j] > 0 and not visited[j]:
                min_j = j
                min_value = matrix[i][j]
        if min_j != 0:
            path.append(min_j)
            visited[min_j] = True
            z += min_value
            value_paths.append(min_value)
            i = min_j
        min_j = 0
        min_value = 9999
    if matrix[path[-1]][0] > 0 and len(path) == len(visited) and len(value_paths) + 1 == len(visited):
        z += matrix[path[-1]][0]
        value_paths.append(matrix[path[-1]][0])
        path.append(0)
        print("Nearest neighbour: ", path, z)


def lowestedge(matrix):
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
        print("Lowest edge:", path, z)


def format_matrix(matrix):
    for i in matrix:
        print(i)


if __name__ == "__main__":
    # matrix = [[0, 61, 177, 188, 381, 104],
    #           [61, 0, 177, 118, 338, 165],
    #           [177, 177, 0, 294, 296, 165],
    #           [188, 118, 294, 0, 368, 255],
    #           [381, 338, 296, 368, 0, 440],
    #           [104, 165, 165, 255, 440, 0]]
    matrix = randomGraph(5, 100)
    format_matrix(matrix)
    print("----")
    # readFile("test")
    DFSsolution(matrix)
    print("Dynamic solution")
    print("------------------------")
    nearestneighbour(matrix)
    # print("Nearest neighbour algorithm")
    print("------------------------")
    lowestedge(matrix)
