import networkx as nx
import json
from bruteForce import calc_fitness
import time

def greedy(graph: nx.Graph, source_terminal_pairs):
    solution = [False for _ in range(len(graph.edges))]
    fitness = calc_fitness(solution, graph, source_terminal_pairs)
    improved = True

    while improved:
        improved = False
        best_i = None
        best_fitness = fitness
        for i in range(len(solution)):
            if solution[i]:
                continue
            solution[i] = True
            new_fitness = calc_fitness(solution, graph, source_terminal_pairs)
            if new_fitness > best_fitness:
                best_fitness = new_fitness
                improved = True
                best_i = i
            solution[i] = not solution[i]
        if improved:
            solution[best_i] = not solution[best_i]
            fitness = best_fitness

    return solution, fitness


if __name__ == '__main__':
    graph = nx.read_gml("tests/test_20_0.4.in")

    with open('tests/test_20_0.4.json', 'r') as file:
        source_terminal_pairs = json.load(file)
    start_time = time.time()
    best_code, best_fitness = greedy(graph, source_terminal_pairs)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(best_fitness)