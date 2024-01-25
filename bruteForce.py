import networkx as nx
import copy
import json

def number_to_fixed_length_boolean_list(number, fixed_length):
    binary_string = bin(number)[2:]
    binary_string = binary_string.zfill(fixed_length)
    boolean_list = [bit == '1' for bit in binary_string]
    return boolean_list

def is_valid(code, graph: nx.Graph, source_terminal_pairs) -> bool:
    edges = list(graph.edges())
    new_graph = nx.Graph()
    nodes_to_insert = graph.nodes()
    new_graph.add_nodes_from(nodes_to_insert)

    for i in range(len(code)):
        if code[i]:
            x,y = edges[i]
            new_graph.add_edge(x,y,weight = graph[x][y]['weight'])

    for x,y in source_terminal_pairs:
        x,y = str(x),str(y)
        if nx.has_path(new_graph,x,y):
            return False

    return True

def calc_fitness(code, graph: nx.Graph, source_terminal_pairs) -> float:
    if not is_valid(code, graph, source_terminal_pairs):
        return float('-inf')
        
    edges = list(graph.edges())
    value = 0
    for i in range(len(code)):
        if not code[i]:
            x,y = edges[i]
            value += graph[x][y]['weight']

    if value == 0:
        return float('inf')
    return 1/value

def brute_force_main(graph: nx.Graph, source_terminal_pairs):
    num_edges = len(graph.edges())

    best_code = None
    best_fitness = float('-inf')

    for i in range(1 << num_edges):
        code = number_to_fixed_length_boolean_list(i, num_edges)
        fit = calc_fitness(code, graph, source_terminal_pairs)
        if best_code == None or best_fitness < fit:
            best_code = copy.deepcopy(code)
            best_fitness = copy.deepcopy(fit)

    return best_code, best_fitness


if __name__ == '__main__':
    graph = nx.read_gml("tests/test_5_0.6")

    with open('tests/test_5_0.6.json', 'r') as file:
        source_terminal_pairs = json.load(file)

    best_code, best_fitness = brute_force_main(graph, source_terminal_pairs)
    print(best_fitness)