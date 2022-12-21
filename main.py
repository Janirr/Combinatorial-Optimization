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


def nearestNeighbour(matrix):
    path = [0]
    value_paths = []
    visited = [False] * (len(matrix))
    visited[0] = True
    min_j = 0
    min_value = float('inf')
    z = 0
    i = 0
    n = len(matrix)
    for _ in range(n - 1):
        for j in range(n):
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
        return path, z


<<<<<<< HEAD
def bruteForce(tab):
    # tab?
    n = len(tab)
=======
def bruteForce(matrix):
    # tab?
    n = len(matrix)
>>>>>>> 5d3caff1daff66b4cb53243920fbb27550b0b2bd
    # Exclude the last element - isomorphism
    pid = list(range(n-1))
    path = []
    z = 9999
    for i in itertools.permutations(pid):
        i = list(i)
        s = 0
        for j in range(1, len(i)):
<<<<<<< HEAD
            s += tab[i[j]][i[j - 1]]
        # Add the distance between the last vertex of the permutation
        # to the last vertex and the last vertex to the first vertex of the permutation
        s += tab[i[-1]][n-1] + tab[n-1][i[0]]
=======
            s += matrix[i[j]][i[j - 1]]
        # Add the distance between the last vertex of the permutation
        # to the last vertex and the last vertex to the first vertex of the permutation
        s += matrix[i[-1]][n-1] + matrix[n-1][i[0]]
>>>>>>> 5d3caff1daff66b4cb53243920fbb27550b0b2bd
        if s < z:
            z = s
            path = i

    # Because we need to add the last vertex
    path.append(n-1)
<<<<<<< HEAD
    path.append(path[0])
=======
>>>>>>> 5d3caff1daff66b4cb53243920fbb27550b0b2bd
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
    population = []
    for i in range(iterations):
        if i == 0:
            for _ in range(maxPopulation):
                path = random.sample(range(0, len(tab)), len(tab))
                path.append(path[0])
                solution = fitness(path, tab)
                population.append(solution)
        population.sort()
        paths = population
        for j in range(mutations):
            population.append(crossover(paths[j], paths[j + 1], matrix))
        population = population[:maxPopulation]
    return population[0]


if __name__ == "__main__":
    for i in range(5, 10, 1):
        matrix = randomGraph(i)
        # matrix = readFile("test")
        print("i:",i)
        print("-- Brute force --", *bruteForce(matrix))
        print("-- Nearest neighbour --", *nearestNeighbour(matrix))
        print("-- Genetic --",geneticSolution(matrix)[1],geneticSolution(matrix)[0])
