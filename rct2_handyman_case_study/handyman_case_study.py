import copy
import random
import numpy as np

graph = {
    'A' : ['B'],
    'B' : ['A', 'C', 'I'],
    'C' : ['B', 'D', 'G'],
    'D' : ['C', 'E', 'F'],
    'E' : ['D'],
    'F' : ['D'],
    'G' : ['C'],
    'H' : ['I'],
    'I' : ['B', 'H', 'J'],
    'J' : ['I'],
}

paths_at_step = {}

######################################################################
''' Starting from 'A', the probability of reaching 'H' node within N-1 total steps from any given node and n current steps is equal to the sum of probabilities of its neighbors reaching 'H' starting at n+1 steps divided by the degree of the node. Of course, if the node itself is 'H' then the probability is 1, which may then be returned. '''

start = 'A'
end = 'H'
current = [start]

def dfs_probability(current_depth, N):
    # base case: at N number of steps, return 1 if 'H'. Otherwise, 0
    if current_depth == N:
        return 1 if current[-1] == end else 0
    
    # base case: if current node is 'H', return 1. This also prunes this part of the tree.
    if current[-1] == end:
        return 1
    
    # recursive step: find the sum of the current node's neighbors' probabilities and divide it by degree of the node. Return this value.
    next_nodes = graph[current[-1]]
    probabilities = []
    for i in range(len(next_nodes)):
        current.append(next_nodes[i])
        probabilities.append(dfs_probability(current_depth+1, N))
        current.pop()
    return sum(probabilities) / len(next_nodes)

print(dfs_probability(1, 15))

######################################################################
# simulate random walk of N-1 total steps starting from 'A'
# probably should have written it iteratively...

start = 'A'
end = 'H'
current = [start]

def walk_random(current_depth, N):
    if current_depth == N:
        return
    next_nodes = graph[current[-1]]
    current.append(next_nodes[random.randint(0, len(next_nodes)-1)])
    walk_random(current_depth+1, N)

# run simulations and find the ratio of paths containing H
num_simulations = 10000
h_in_path = 0
for i in range(num_simulations):
    walk_random(1, 15)
    if end in current:
        h_in_path += 1

    current = [start]

print(h_in_path, num_simulations, h_in_path/num_simulations)

######################################################################
# Simulate and find the average number of steps it takes to reach H

start = 'A'
end = 'H'
current = [start]
_max = 0
max_path = None
def path_until_h():
    global current
    global _max
    global max_path

    while True: 
        if current[-1] == end:
            break
        next_nodes = graph[current[-1]]
        current.append(next_nodes[random.randint(0, len(next_nodes)-1)])
    toReturn = len(current)
    if toReturn > _max:
        _max = toReturn
        max_path = copy.deepcopy(current)
    current = [start]
    return toReturn-1

total = 10000
lengths_sum = 0

for i in range(total):
    length = path_until_h()
    lengths_sum += length

# print(_max)
# print(max_path)
print(lengths_sum/total)


######################################################################
# We can represent the random walk as a stochastic system.
# Given the transition matrix from the graph, we can estimate the mean first passage times (MFPT)
P = []
for key in graph.keys():
    degree = len(graph[key])
    zeroInd = ord('A')
    row = np.zeros(10)
    for neighbor in graph[key]:
        index = ord(neighbor) - zeroInd
        row[index] = 1/degree
    P.append(row)
P = np.array(P)

def mfpt(P, max_iterations=1000):
    n = P.shape[0]
    M = np.zeros((n, n))
    
    for _ in range(max_iterations):
        M_new = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    M_new[i, j] = 1 + np.sum(P[i, :] * M[:, j])
        
        M = M_new
    
    return M

print(mfpt(P))