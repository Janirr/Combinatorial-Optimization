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
    tmp = []
    for i in range(n):
        connection = list(map(int, f.readline().split(" ")))
        tmp.append(connection)
    f.close()
    return tmp


def DeepFirstSearch(tab):
    global minZ
    if len(tab) > 0:
        z = 0
        path = [0]
        visited = [False] * (len(tab))
        minZ = 9999
        for i in range(len(visited)):
            visited[i] = False
        visited[0] = True
        DFS(tab, 1, path, visited, z)


def DFS(tab, current_position, path, visited, z):
    global minZ
    if current_position == len(tab):
        if tab[path[-1]][path[0]] != 0:
            z += tab[0][path[-1]]
            path.append(0)
            if z < minZ and len(path) > len(tab):
                minZ = z
                print(path, z)
            z -= tab[0][path[-1]]
            path.pop()
    for v in range(len(tab)):
        if isSafe(tab, v, path, current_position) and not visited[v]:
            z += tab[v][path[-1]]
            path.append(v)
            visited[v] = True
            DFS(tab, current_position + 1, path, visited, z)
            visited[v] = False
            z -= tab[v][path[-1]]
            path.pop()
            z -= tab[v][path[-1]]


def randomGraph(n, max_value=1000):
    edgesList = []
    max_edges = n * (n - 1)
    for i in range(n):
        for j in range(n):
            if i != j:
                edge = [i + 1, j + 1]
                edgesList.append(edge)
    # We are removing one by one values in reversed but sorted order.
    random_list = random.sample(range(1, max_edges), n)
    graph = [[0] * n for _ in range(n)]
    for j in range(len(edgesList)):
        x = edgesList[j][0] - 1
        y = edgesList[j][1] - 1
        d = random.randint(1, max_value)
        graph[x][y] = d
        graph[y][x] = d
    return graph


def nearestNeighbour(tab):
    path = [0]
    valuePaths = []
    visited = [False] * (len(tab))
    visited[0] = True
    minIndex = 0
    minValue = 9999
    z = 0
    i = 0
    for _ in range(len(tab) - 1):
        for j in range(len(tab)):
            if minValue > tab[i][j] > 0 and not visited[j]:
                minIndex = j
                minValue = tab[i][j]
        if minIndex != 0:
            path.append(minIndex)
            visited[minIndex] = True
            z += minValue
            valuePaths.append(minValue)
            i = minIndex
        minIndex = 0
        minValue = 9999
    if tab[path[-1]][0] > 0 and len(path) == len(visited) and len(valuePaths) + 1 == len(visited):
        z += tab[path[-1]][0]
        valuePaths.append(tab[path[-1]][0])
        path.append(0)
        print(path, z)


def lowestEdge(tab):
    n = len(tab)
    tmp = []
    path = []
    visited = [[False, False] for _ in range(n)]
    z = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            if tab[i][j] > 0:
                block = [tab[i][j], i, j]
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
    # tab?
    n = len(matrix)
    # Exclude the last element - isomorphism
    pid = list(range(n-1))
    path = []
    z = 9999
    for i in itertools.permutations(pid):
        i = list(i)
        s = 0
        for j in range(1, len(i)):
            s += matrix[i[j]][i[j - 1]]
        # Add the distance between the last vertex of the permutation
        # to the last vertex and the last vertex to the first vertex of the permutation
        s += matrix[i[-1]][n-1] + matrix[n-1][i[0]]
        if s < z:
            z = s
            path = i

    # Because we need to add the last vertex
    path.append(n-1)
    return path, z


def fitness(path, tab):
    z = 0
    for i in range(1, len(path)):
        z += tab[path[i]][path[i - 1]]
    return [z, path]


def crossover(arr1, arr2, tab):
    path1 = arr1[1]
    path2 = arr2[1]
    half = len(path1) // 2
    new_path = []
    for i in path1[:half]:
        new_path.append(i)
    for city in path2:
        if city not in new_path:
            new_path.append(city)
    new_path.append(new_path[0])
    calculated = fitness(new_path, tab)
    return calculated


def geneticSolution(tab, maxPopulation=10, mutations=5, iterations=5):
    solutions = []
    for i in range(iterations):
        if i == 0:
            for _ in range(maxPopulation):
                path = random.sample(range(0, len(tab)), len(tab))
                path.append(path[0])
                solution = fitness(path, tab)
                solutions.append(solution)
        solutions.sort(reverse=True)
        paths = solutions
        for j in range(mutations):
            solutions.append(crossover(paths[j], paths[j + 1], matrix))
        solutions.sort()
        solutions = solutions[:maxPopulation]
    print(*solutions[0])


if __name__ == "__main__":
    for _ in range(1, 2, 1):
        matrix = readFile("test")
        print("Brute force:", bruteForce(matrix))
        print("--- DFS ---")
        DeepFirstSearch(matrix)
        print("--- NNA ---")
        nearestNeighbour(matrix)
        print("--- LEA ---")
        lowestEdge(matrix)
        print("--- GEN ---")
        geneticSolution(matrix)
