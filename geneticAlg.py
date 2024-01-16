import random
import networkx as nx
import sys
import copy

class Individual:
    def __init__(self, graph: nx.Graph, source_terminal_pairs: list) -> None:
        self.source_terminal_pairs = source_terminal_pairs
        self.edges: list = list(graph.edges())
        self.code: list = [random.random() < 0.5 for _ in range(len(self.edges))]
        self.fitness: int = self.calc_fitness(graph)
        
    def is_valid(self, graph: nx.Graph) -> bool:
        new_graph = nx.Graph()
        nodes_to_insert = graph.nodes()
        new_graph.add_nodes_from(nodes_to_insert)

        for i in range(len(self.code)):
            if self.code[i]:
                x,y = self.edges[i]
                new_graph.add_edge(x,y,weight = graph[x][y]['weight'])

        for x,y in self.source_terminal_pairs:
            x,y = str(x),str(y)
            if nx.has_path(new_graph,x,y):
                return False
        return True
        
    def calc_fitness(self, graph: nx.Graph) -> float:
        if not self.is_valid(graph):
            return float('-inf')

        value = 0
        for i in range(len(self.edges)):
            if not self.code[i]:
                x,y = self.edges[i]
                value += graph[x][y]['weight']

        if value == 0:
            return float('inf')
        return 1/value
    
def selection(population, tournament_size) -> Individual:
    chosen = random.sample(population, tournament_size)
    return max(chosen, key=lambda x: x.fitness)

def crossover(parent1: Individual, parent2, child1, child2) -> None:
    random_pos = random.randrange(0, len(parent1.code))
    
    child1.code[:random_pos] = parent1.code[:random_pos]
    child1.code[random_pos:] = parent2.code[random_pos:]
    
    child2.code[:random_pos] = parent2.code[:random_pos]
    child2.code[random_pos:] = parent1.code[random_pos:]

def mutation(individual, mutation_prob) -> None:
    for i in range(len(individual.code)):
        if random.random() < mutation_prob:
            individual.code[i] = not individual.code[i]

def ga(population_size, num_generations, tournament_size, elitism_size, mutation_prob, graph, source_terminal_pairs) -> Individual:
    population = [Individual(graph, source_terminal_pairs) for _ in range(population_size)]
    new_population = population.copy()
    
    for _ in range(num_generations):
        population.sort(key=lambda x: x.fitness, reverse=True)
        new_population[:elitism_size] = population[:elitism_size]
        for j in range(elitism_size, population_size, 2):
            parent1 = selection(population, tournament_size)
            parent2 = selection(population, tournament_size)
            
            crossover(parent1, parent2, child1=new_population[j], child2=new_population[j+1])

            mutation(new_population[j], mutation_prob)
            mutation(new_population[j+1], mutation_prob)
            
            new_population[j].fitness = new_population[j].calc_fitness(graph)
            new_population[j+1].fitness = new_population[j+1].calc_fitness(graph)
        
        population = new_population.copy()
    return max(population, key=lambda x: x.fitness)

if __name__ == '__main__':
    G = nx.read_gml("tests/test")
    import json

    with open('tests/test.json', 'r') as file:
        source_terminal_pairs = json.load(file)
    best = ga(
        population_size=1000,
        num_generations=7,
        tournament_size=7,
        elitism_size=10,
        mutation_prob=0.1,
        graph=G,
        source_terminal_pairs = source_terminal_pairs
    )
    print(best.code)
    print(best.fitness)