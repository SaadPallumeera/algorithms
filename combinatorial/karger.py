import random
from copy import deepcopy
from math import log, ceil

def contract(u, v, adj):
    """
    Contract edge (u, v): merge v into u and remove self-loops.
    `adj` is mutated in place.
    """
    # Append v’s adjacency list to u’s
    adj[u].extend(adj[v])

    # Replace every occurrence of v with u in the graph
    for w in adj[v]:
        adj[w] = [u if x == v else x for x in adj[w]]

    # Remove self-loops that now point u-->u
    adj[u] = [x for x in adj[u] if x != u]

    # Delete vertex v
    del adj[v]

def karger_min_cut_once(adj):
    """
    Perform one run of Karger’s algorithm.
    Returns the cut size.
    """
    adj = deepcopy(adj)  # Work on a copy so caller’s graph stays intact
    while len(adj) > 2:
        u = random.choice(list(adj.keys()))
        v = random.choice(adj[u])
        contract(u, v, adj)
    # All remaining edges are between the two supernodes
    remaining_vertices = list(adj.keys())
    cut_size = len(adj[remaining_vertices[0]])
    return cut_size

def karger_min_cut(adj, trials=None):
    """
    Repeatedly run the algorithm and keep the best cut found.
    trials: number of repetitions.  If None, use ⌈n² · ln n⌉ which
    succeeds with probability ≥ 1 – 1/n.
    """
    n = len(adj)
    if trials is None:
        trials = ceil(n * n * log(n))

    best = float('inf')
    for _ in range(trials):
        cut = karger_min_cut_once(adj)
        best = min(best, cut)
    return best

# -------------- Example usage --------------
if __name__ == "__main__":
    # Undirected multigraph as adjacency list
    example_graph = {
        0: [1, 2, 3],
        1: [0, 2, 3],
        2: [0, 1, 3],
        3: [0, 1, 2]
    }
    print("Estimated min-cut:", karger_min_cut(example_graph, trials=50))
