from bruteForce import calc_fitness
import networkx as nx
import json
import random
from copy import deepcopy
from time import perf_counter
import time

def local_search_invert_best_improvement(solution, value, graph: nx.Graph, source_terminal_pairs):
    improved = True
    while improved:
        improved = False
        best_i = None
        best_value = value
        for i in range(len(solution)):
            solution[i] = not solution[i]
            new_value = calc_fitness(solution, graph, source_terminal_pairs)
            if new_value > best_value:
                best_value = new_value
                improved = True
                best_i = i
            solution[i] = not solution[i]
        if improved:
            solution[best_i] = not solution[best_i]
            value = best_value

    return solution, value

def shaking(solution, k):
    new_solution = deepcopy(solution)
    chosen_indices = random.sample(range(len(solution)), min(k,len(solution)))
    for idx in chosen_indices:
        new_solution[idx] = not new_solution[idx]

    return new_solution


def vns(graph: nx.Graph, source_terminal_pairs, vns_params: dict):
    start_time = perf_counter()
    solution = initialize(graph)
    value = calc_fitness(solution, graph, source_terminal_pairs)
    iters = 0

    while iters < vns_params['iters'] and perf_counter() - start_time < vns_params['time_limit']:
        iters += 1
        for k in range(vns_params['k_min'], vns_params['k_max']):
            new_solution = shaking(solution, k)
            new_value = calc_fitness(new_solution, graph, source_terminal_pairs)
            new_solution, new_value = local_search_invert_best_improvement(
                new_solution,
                new_value,
                graph,
                source_terminal_pairs
            )
            if new_value > value or (new_value == value and random.random() < vns_params['move_prob']):
                value = new_value
                solution = deepcopy(new_solution)

    return solution, value

def vns_main(graph: nx.Graph, source_terminal_pairs):
    vns_params = {
        'iters': 20000,
        'time_limit': 5,
        'k_min': 2,
        'k_max': 6,
        'move_prob': 0.1,
    }
    best_code, best_fitness = vns(graph, source_terminal_pairs, vns_params)
    return best_code, best_fitness


def initialize(graph: nx.Graph):
    return [random.random() < 0.1 for _ in range(len(graph.edges()))]
    
if __name__ == '__main__':
    graph = nx.read_gml('tests/test_20_0.4.in')

    with open('tests/test_20_0.4.json', 'r') as file:
        source_terminal_pairs = json.load(file)

    start_time = time.time()
    best_code, best_fitness = vns_main(graph, source_terminal_pairs)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(best_fitness)