# Minimum Multi Cut

## Overview

Welcome to the Minimum Multi Cut project! This computational intelligence project tackles the NP-hard problem of finding the minimum multi cut in a graph. The optimization techniques employed include Variable Neighbourhood Search (VNS) and Genetic Algorithm (GA).

## Problem Definition

- **Instance:** A graph G(V, E), a set S ⊆ V × V of source-terminal pairs, and a weight function w: E → N.
  
- **Solution:** Find a multi-cut E' ⊆ E such that removing E' disconnects each source s from its corresponding terminal t for every pair (s, t) ∈ S.
  
- **Measure:** Minimize the weight of the cut, defined as the sum of weights in E'

## Optimization Techniques

### 1. Variable Neighbourhood Search (VNS)

Variable Neighbourhood Search is a metaheuristic optimization algorithm that explores the search space by systematically changing the neighborhood structure.

### 2. Genetic Algorithm (GA)

Genetic Algorithm is an evolutionary algorithm inspired by the process of natural selection. It operates on a population of candidate solutions, evolving them through generations to find the optimal solution.
