import networkx as nx
import json
from bruteForce import calc_fitness
import time

def get_neighbours(solution):
    neighbours = []
    for i in range(len(solution)):
        new = solution.copy()
        new[i] = not solution[i]
        neighbours.append(new)
    
    return neighbours

def tabu_search(graph: nx.Graph, source_terminal_pairs, max_iters):
    iter = 0
    sol = [False for _ in range(len(graph.edges))]
    fitness = calc_fitness(sol, graph, source_terminal_pairs)
    best_sol = sol.copy()
    best_fitness = fitness
    tabu_list = [sol]
    while iter < max_iters:
        iter += 1
        neighbours = get_neighbours(sol)
        neighbours.sort(key=lambda neighbour: calc_fitness(neighbour, graph, source_terminal_pairs), reverse=True)

        sol = None
        for neighbour in neighbours:
            if neighbour not in tabu_list:
                sol = neighbour
                break
        
        if sol is None:
            sol = neighbours[0]
        
        tabu_list.append(sol)

        fitness = calc_fitness(sol, graph, source_terminal_pairs)
        if fitness > best_fitness:
            best_sol = sol.copy()
            best_fitness = fitness

    return best_sol, best_fitness


def tabu_main(graph: nx.Graph, source_terminal_pairs):
    return tabu_search(graph, source_terminal_pairs, 200)


if __name__ == '__main__':
    graph = nx.read_gml("tests/test_20_0.4.in")

    with open('tests/test_20_0.4.json', 'r') as file:
        source_terminal_pairs = json.load(file)

    start_time = time.time()
    best_code, best_fitness = tabu_main(graph, source_terminal_pairs)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(best_fitness)