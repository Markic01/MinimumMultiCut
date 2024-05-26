import networkx as nx
import random
import json
import sys
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("usage: python3 generate.py nodes probability")
        exit()

    num_nodes = int(sys.argv[1])
    prob = float(sys.argv[2])
    if prob >= 1 or prob <= 0:
        prob = 0.5

    graph: nx.Graph = nx.fast_gnp_random_graph(num_nodes, prob)
    for edge in graph.edges():
        graph.edges[edge]['weight'] = random.randint(1, 10)

    nx.write_gml(graph, f'tests/test_{num_nodes}_{prob}.in')
    print(graph)

    nodes = list(graph.nodes())
    num_pairs = random.randint(1, 3)
    source_terminal_pairs = []

    for _ in range(num_pairs):
        source = random.choice(nodes)
        terminal_candidates = [node for node in nodes if node != source]
        terminal = random.choice(terminal_candidates)
        source_terminal_pairs.append((source, terminal))

    print(source_terminal_pairs)
    with open(f'tests/test_{num_nodes}_{prob}.json', 'w') as file:
        json.dump(source_terminal_pairs, file)