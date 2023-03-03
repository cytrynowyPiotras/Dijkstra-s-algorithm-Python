import argparse
import math


def dijkstra(start_x, start_y, graph: list):
    x, y = len(graph[0]), len(graph)
    visited = [[False for _ in range(x)] for _ in range(y)]
    cost = [[math.inf for _ in range(x)] for _ in range(y)]
    parents = [[(0, 0) for _ in range(x)] for _ in range(y)]
    cost[start_y][start_x] = 0
    for i_y in range(y):
        for i_x in range(x):
            min_cost = math.inf + 1
            min_cost_x = -1
            min_cost_y = -1
            for j_y in range(y):
                for j_x in range(x):
                    if not visited[j_y][j_x] and cost[j_y][j_x] < min_cost:
                        min_cost = cost[j_y][j_x]
                        min_cost_x = j_x
                        min_cost_y = j_y
            nodes = []
            if min_cost_y != 0:
                nodes.append((min_cost_y-1, min_cost_x))
            if min_cost_y != y - 1:
                nodes.append((min_cost_y+1, min_cost_x))
            if min_cost_x != 0:
                nodes.append((min_cost_y, min_cost_x-1))
            if min_cost_x != x - 1:
                nodes.append((min_cost_y, min_cost_x+1))
            for z in nodes:
                z_y, z_x = z
                temp = cost[min_cost_y][min_cost_x] + graph[z_y][z_x]
                if temp < cost[z_y][z_x]:
                    cost[z_y][z_x] = temp
                    parents[z_y][z_x] = (min_cost_y, min_cost_x)
            visited[min_cost_y][min_cost_x] = True
    return parents


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        type=str, dest='file',
        help='path to file'
    )
    return parser.parse_args()


def read_graph_from_file(fname):
    graph = []
    with open(fname) as fp:
        for line in fp:
            row = [int(weight) for weight in line.strip()]
            graph.append(row)
    return graph


def get_index_in_graph(value, graph):
    indexes = []
    for idy, i in enumerate(graph):
        for idx, j in enumerate(i):
            if j == value:
                indexes.append((idy, idx))
    return indexes


if __name__ == "__main__":
    graph = read_graph_from_file("graph.txt")
    zero_indexes = get_index_in_graph(0, graph)
    if len(zero_indexes) != 2:
        raise ValueError("Incorrect graph!")
    start, end = zero_indexes[0], zero_indexes[1]
    start_y, start_x = start
    parents = dijkstra(start_x, start_y, graph)
    path = [[None for _ in range(len(graph[0]))] for _ in range(len(graph))]
    while (end != start):
        e_y, e_x = end
        path[e_y][e_x] = graph[e_y][e_x]
        end = parents[e_y][e_x]
    path[start_y][start_x] = graph[start_y][start_x]
    for i in path:
        for j in i:
            print(j if j is not None else " ", end='')
        print('')
