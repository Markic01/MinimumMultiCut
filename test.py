from bruteForce import brute_force_main
from vns import vns_main
from geneticAlg import ga_main
import networkx as nx
import json
import os

def do_brute_force(graph: nx.Graph) -> bool:
    return len(graph.edges) < 23


input_files = []
input_json_files = []

for filename in os.listdir('tests'):
    if filename.endswith('.json'):
        input_json_files.append(filename)
        input_files.append(filename[:-5])

for i in range(len(input_files)):
    graph = nx.read_gml('tests/' + input_files[i])

    with open('tests/' + input_json_files[i], 'r') as file:
        source_terminal_pairs = json.load(file)

    print(graph,' ', source_terminal_pairs, '\n')

    repeat = 2

    if do_brute_force(graph):
        best_code, best_fitness = brute_force_main(graph, source_terminal_pairs)
        print(f'brute force:')
        print(f'\tbest fitness: {best_fitness}\n')
    else:
        print(f'brute force:\n\ttakes too long\n')
    
    vns_fitness = []
    for _ in range(repeat):
        a,b = ga_main(graph, source_terminal_pairs)
        vns_fitness.append(b)
    print(f'variable neighborhood search:')
    print(f'\tbest={max(vns_fitness):<10} worst={min(vns_fitness):<10} average={sum(vns_fitness)/repeat:<10}\n')
    ga_fitness = []
    for _ in range(repeat):
        a,b = ga_main(graph, source_terminal_pairs)
        ga_fitness.append(b)
    print(f'genetic algorithm')
    print(f'\tbest={max(ga_fitness):<10} worst={min(ga_fitness):<10} average={sum(ga_fitness)/repeat:<10}')

    print()
