import math
import copy

def round_decimals_up(number:float, decimals:int=2):
    """
    Returns a value rounded up to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.ceil(number)

    factor = 10 ** decimals
    remainder = number - int(number)
    if remainder > 0.0000000001:
        return math.ceil(number * factor) / factor
    else:
        return math.floor(number * factor) / factor

def get_distance(gopher, hole):
    return math.sqrt(pow(gopher[0] - hole[0], 2) + pow(gopher[1] - hole[1], 2))

def remove_extra(residual, gopher_coords, hole_coords, time, m, n):
    for i, gopher in enumerate(gopher_coords):
        for j, hole in enumerate(hole_coords):
            if (get_distance(gopher, hole) > time):
                residual[1 + i][1 + m + j] = 0

def BFS(residual, parent, m, n):
    vertices = 2 + m + n
    #print(str(m) + " : " + str(n))
    visited = [False] * vertices
    queue = []

    # We add the outgoing starting node to the queue
    queue.append(0)
    visited[0] = True
    while(queue):
        current = queue.pop(0)

        for vertex, cost in enumerate(residual[current]):
            if (visited[vertex] == False and cost > 0):
                if (vertex == vertices - 1):
                    parent[vertex] = current
                    return True
                queue.append(vertex) 
                visited[vertex] = True
                parent[vertex] = current
    return False

def ford_fulkerson(residual, m, n):
    vertices = 2 + m + n
    parent = [-1] * (vertices)
    max_flow = 0
    while (BFS(residual, parent, m, n)):
        path_flow = 10000000000
        vertex = vertices - 1
        while (vertex != 0):
            path_flow = min(path_flow, residual[parent[vertex]][vertex])
            vertex = parent[vertex]
        max_flow += path_flow

        vertex = vertices - 1
        while (vertex != 0):
            residual[parent[vertex]][vertex] -= path_flow
            residual[vertex][parent[vertex]] += path_flow
            vertex = parent[vertex]
    return max_flow

def count_saved(graph, gopher_coords, hole_coords, time, m, n):
    residual = copy.deepcopy(graph)
    remove_extra(residual, gopher_coords, hole_coords, time, m, n)
    return ford_fulkerson(residual, m, n)



def main():
    iterations = int(input())
    for iteration in range(iterations):
        m, n, k = map(int, input().split())
        gopher_coords = [[0 for _ in range(2)] for _ in range(m)]
        hole_coords = [[0 for _ in range(2)] for _ in range(n)]

        for j in range(m):
            x, y = map(int, input().split())
            gopher_coords[j][0] = x
            gopher_coords[j][1] = y

        for j in range(n):
            x, y = map(int, input().split())
            hole_coords[j][0] = x
            hole_coords[j][1] = y
        
        residual = [[0 for i in range(2 + m + n)] for j in range(2 + m + n)]

        for i in range(m):
            residual[0][1 + i] = 1
        
        for i in range(m):
            for j in range(n):
                residual[1 + i][1 + m + j] = 1
        
        for j in range(n):
            residual[1 + m + j][1 + m + n] = 1
        
        min = -0.001
        max = 1000000
        while (min + 0.0000000001 < max):
            d = (min + max) / 2
            if (count_saved(residual, gopher_coords, hole_coords, d, m, n) < m - k):
                min = d
            else:
                max = d

        print("Case #" + str(iteration + 1) + ":")

        if (max < 1000000): 
            print("%0.3f" % round_decimals_up(max, 3))
        else:
            print("Too bad.")
        
main()