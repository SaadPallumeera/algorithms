Algorithms Toolkit

This repository contains a collection of machine learning and theoretical computer science algorithms I've implemented from scratch. The goal is to clearly demonstrate how each algorithm works, highlight their real-world applications, and provide clean, reusable code.

Contents

Machine Learning Algorithms

1. Gaussian Mixture Models (GMM)

Purpose: Clusters data points based on probabilistic modeling, allowing soft assignment to multiple clusters.

Applications: Image segmentation, customer segmentation.

Complexity: O(nkd) per iteration (n=data points, k=clusters, d=dimensions).

2. Independent Component Analysis (ICA)

Purpose: Separates mixed signals into independent original components.

Applications: EEG/ECG signal analysis, blind source separation.

Complexity: O(n²) per iteration (depends on implementation specifics).

3. Principal Component Analysis (PCA)

Purpose: Reduces dimensionality of datasets by finding directions of maximum variance.

Applications: Visualization, noise reduction, feature extraction.

Complexity: O(n³) via eigendecomposition or SVD.

4. k-Means Clustering

Purpose: Partitions data into k distinct clusters based on centroid proximity.

Applications: Customer segmentation, recommendation systems.

Complexity: O(nkd) per iteration.

Optimization Algorithms

5. Simplex Method

Purpose: Solves linear programming problems efficiently.

Applications: Resource allocation, production scheduling.

Complexity: Exponential worst-case, typically efficient in practice.

6. LP-based Set Cover Approximation

Purpose: Approximates solutions to NP-hard set cover problems using linear programming.

Applications: Network design, coverage optimization.

Complexity: Polynomial approximation algorithm.

7. Minimum Bipartite Perfect Matching

Purpose: Matches nodes in bipartite graphs minimizing the total matching cost.

Applications: Assignment problems, job scheduling.

Complexity: polynomial using linear programming

Graph Algorithms

8. Hopcroft-Karp Algorithm

Purpose: Finds maximum matching in bipartite graphs efficiently.

Applications: Task assignments, network scheduling.

Complexity: O(√V * E).

9. Karger's Randomized Min-Cut

Purpose: Probabilistically computes the minimum cut of a graph.

Applications: Network reliability analysis, clustering.

Complexity: Repeated trials yield high probability of correctness, typically O(n²) per trial.

10. 2-SAT Solver (via Strongly Connected Components)

Purpose: Solves Boolean satisfiability problems restricted to two literals per clause.

Applications: Constraint solving, logic verification.

Complexity: O(V + E).

Number Theory Algorithms

11. Large Prime Generator (Miller-Rabin Primality Test)

Purpose: Efficiently generates large prime numbers suitable for cryptography.

Applications: RSA encryption, cryptographic keys.

Complexity: Probabilistic O(k log³n), very fast in practice.

12. Max Flow via Linear Programming
Purpose: Computes the maximum amount of flow that can be sent from a source node to a sink node in a flow network.

Method: Formulated as a linear program with flow variables on each edge, capacity constraints, and flow conservation at all non-terminal nodes.

Applications: Network routing, transportation logistics, bipartite matching.

Complexity: Solved in polynomial time using LP solvers; combinatorial algorithms (e.g., Dinic’s) are typically faster in practice.


