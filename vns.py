from bruteForce import calc_fitness
import networkx as nx
import json
import random
from copy import deepcopy
from time import perf_counter

def local_search_invert_best_improvement(
    solution,
    value: int,
    graph,
    source_terminal_pairs
):
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
    chosen_indices = random.sample(range(len(solution)), k)
    for idx in chosen_indices:
        new_solution[idx] = not new_solution[idx]
    return new_solution


def vns(graph, source_terminal_pairs, vns_params: dict):
    start_time = perf_counter()
    solution = initialize(graph)
    value = calc_fitness(solution, graph, source_terminal_pairs)
    while perf_counter() - start_time < vns_params['time_limit']:
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


def initialize(graph):
    return [random.random() < 0.5 for _ in range(len(graph.edges()))]
    
if __name__ == '__main__':
    graph = nx.read_gml('tests/test')

    with open('tests/test.json', 'r') as file:
        source_terminal_pairs = json.load(file)

    vns_params = {
        'time_limit': 2,
        'k_min': 2,
        'k_max': 6,
        'move_prob': 0.1,
    }
    a,b = vns(graph, source_terminal_pairs, vns_params)
    print(a)
    print(b)