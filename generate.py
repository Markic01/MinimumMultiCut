import networkx as nx
import random
import json

nodes = 10
prob = 0.5

G: nx.Graph = nx.fast_gnp_random_graph(nodes, prob)

for edge in G.edges():
    G.edges[edge]['weight'] = random.randint(1, 10)

nx.write_gml(G, 'tests/test')
print(G)

nodes = list(G.nodes())
num_pairs = random.randint(1, max(2,len(nodes)//3))
source_terminal_pairs = []

for _ in range(num_pairs):
    source = random.choice(nodes)
    terminal_candidates = [node for node in nodes if node != source]
    terminal = random.choice(terminal_candidates)
    source_terminal_pairs.append((source, terminal))

print(source_terminal_pairs)

with open('tests/test.json', 'w') as file:
    json.dump(source_terminal_pairs, file)