import sys
import random
import numpy as np


class Distances:

    def __init__(self, tab):
        self.matrix = tab
        self.hasHamCycle = False
        self.bestPath = []
        self.minZ = 999999

    def isSafe(self, v, path, pos):
        if self.matrix[path[pos - 1]][v] == 0:
            return False
        for i in range(pos):
            if path[i] == v:
                return False
        return True

    def dynamicsolution(self):
        if len(self.matrix) > 0:
            z = 0
            path = [0]
            visited = [False] * (len(self.matrix))
            for i in range(len(visited)):
                visited[i] = False
            # Starting from the first value so we change it that is has been visited
            visited[0] = True
            self.findHamCycle(1, path, visited, z)

    def findHamCycle(self, current_position, path, visited, z):
        n = len(self.matrix)
        # If we have all the vertexes in path, we have possible Hamiltonian cycle
        if current_position == len(self.matrix):
            # If it isn't 0 obviously ; )
            if self.matrix[path[-1]][path[0]] != 0:
                z += self.matrix[0][path[-1]]
                path.append(0)
                if z < self.minZ and len(path) > n:
                    self.minZ = z
                    print(path, self.minZ)
                z -= self.matrix[0][path[-1]]
                path.pop()

        for v in range(len(self.matrix)):
            if self.isSafe(v, path, current_position) and not visited[v]:
                z += self.matrix[v][path[-1]]
                path.append(v)
                visited[v] = True
                self.findHamCycle(current_position + 1, path, visited, z)
                # Change the value of the vertex to not visited and substract it's value.
                visited[v] = False
                z -= self.matrix[v][path[-1]]
                path.pop()
                z -= self.matrix[v][path[-1]]

    def readFile(self, file_name):
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
        self.matrix = tmp_tab
        f.close()

    def randomGraph(self, n, density, max_value=1000):
        # edgest_list
        edges = []
        max_edges = (n * (n - 1))
        for i in range(n):
            for j in range(n):
                if i != j:
                    edge = [i + 1, j + 1]
                    edges.append(edge)
        # We are removing one by one values in reversed but sorted order.
        # This way we won't pop somet
        random_list = random.sample(range(1, max_edges), int(abs(density - 100) / 100 * max_edges))
        random_list.sort(reverse=True)
        for j in random_list:
            edges.pop(j)
        sorted_tab = edges
        graph = [[0] * n for _ in range(n)]
        for j in range(len(sorted_tab)):
            x = sorted_tab[j][0] - 1
            y = sorted_tab[j][1] - 1
            d = random.randint(1, max_value)
            graph[x][y] = d
            graph[y][x] = d
        self.matrix = graph
        for k in self.matrix:
            print(k)
        print("-------------------")

    def nearestneighbour(self):
        # We will start from the first value, we will add it
        # to the path and to the tab visited
        path = [0]
        value_paths = []
        visited = [False] * (len(self.matrix))
        visited[0] = True
        # Initiate temporary variables to detect minimum values
        min_j = 0
        min_value = 9999
        # Variable z will be responsible for adding the values
        # from the matrix that we will visit
        z = 0
        i = 0
        for _ in range(len(self.matrix) - 1):
            for j in range(len(self.matrix)):
                if min_value > self.matrix[i][j] > 0 and not visited[j]:
                    min_j = j
                    min_value = self.matrix[i][j]
            # Check if the if statement happened
            if min_j != 0:
                path.append(min_j)
                visited[min_j] = True
                z += min_value
                value_paths.append(min_value)
                i = min_j
            # Reset the values
            min_j = 0
            min_value = 9999
        # Going back to 0, since we want a Hamiltonian cycle
        # but we need to make sure there is path!
        if self.matrix[path[-1]][0] > 0 and len(path) == len(visited) and len(value_paths) + 1 == len(visited):
            z += self.matrix[path[-1]][0]
            value_paths.append(self.matrix[path[-1]][0])
            path.append(0)
            print("Nearest neighbour: ", path, z)
        else:
            print("Nearest neighbour: No solution. The path would include zeros")

    def lowestedge(self):
        n = len(self.matrix)
        tmp = []
        path = []
        allvalues = []
        z = 0
        for i in range(n - 1):
            for j in range(i + 1, n):
                if self.matrix[i][j] > 0:
                    block = [self.matrix[i][j], i, j]
                    tmp.append(block)
        tmp.sort()
        for i in range(len(tmp)):
            if allvalues.count(tmp[0][1]) < 2 and allvalues.count(tmp[0][2]) < 2:
                if allvalues.count(tmp[0][1]) == 1 and allvalues.count(tmp[0][2]) == 1:
                    if len(path) == n-1:
                        connection = [tmp[0][1], tmp[0][2]]
                        allvalues.append(tmp[0][1])
                        allvalues.append(tmp[0][2])
                        path.append(connection)
                        z += tmp[0][0]
                else:
                    if len(path) < n-1:
                        connection = [tmp[0][1], tmp[0][2]]
                        allvalues.append(tmp[0][1])
                        allvalues.append(tmp[0][2])
                        path.append(connection)
                        z += tmp[0][0]
            tmp.pop(0)
        if len(path) == n:
            print("Lowest edge:", path, z)
        else:
            print("Cycle:", path, z)


if __name__ == "__main__":
    matrix = Distances([])
    matrix.randomGraph(5, 100, max_value=10)
    # matrix.readFile("test")
    matrix.dynamicsolution()
    print("Dynamic solution")
    print("------------------------")
    matrix.nearestneighbour()
    # print("Nearest neighbour algorithm")
    print("------------------------")
    matrix.lowestedge()
