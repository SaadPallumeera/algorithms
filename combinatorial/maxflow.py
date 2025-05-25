
"""Minimal example to call the GLOP solver."""
# [START program]
# [START import]
from ortools.init.python import init
from ortools.linear_solver import pywraplp
from collections import defaultdict
# [END import]


#edges = (start,end,weight)
#vertices = number of vertices from 1-n
#source = source vertice of flow
#sink = sink vertice of flow
def max_flow(edges, vertices, source, sink): 
    # Step 1: Initialize the graph structures
    outgoing = defaultdict(list)  
    incoming =  defaultdict(list)

    for start, end, weight in edges:
        incoming[end].append((start,weight))
        outgoing[start].append((end,weight))  


    solver = pywraplp.Solver.CreateSolver("GLOP")

    variables = {}

    #creating all of the variables
    for i in outgoing:
        for j in outgoing[i]:
            out = j[0]
            var = solver.NumVar(0.0, j[1], f'var_{i}_{out}')
            variables[f'var_{i}_{out}'] = var

    #set up objective function
    objective = solver.Objective()

    for i in outgoing[source]:
        out = i[0]
        var = variables[f'var_{source}_{out}']
        objective.SetCoefficient(var, 1)
    objective.SetMaximization()

    # Step 4: Create the constraints
    for vertex in range(1, vertices + 1):
        if vertex == sink or vertex == source:
            continue

        in_total = 0
        for j in incoming[vertex]:
            in_v = j[0]
            in_total+=variables[f'var_{in_v}_{vertex}']
        out_total = 0

        for j in outgoing[vertex]:
            out_v = j[0]
            out_total+=variables[f'var_{vertex}_{out_v}']

        solver.Add(in_total == out_total)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Optimal solution found.')
        print('Maximum flow:', objective.Value())
        for  var in variables:
            print(var, end = " ")
            print(variables[var].solution_value())
    else:
        print('No optimal solution found.')



def main():
    edges = [
        (0, 1, 100),
        (0, 2, 100),
        (0, 3, 100),
        (1, 4, 5),
        (2, 5, 7),
        (3, 6, 9),
        (4, 5, 8),
        (6, 5, 4),
        (5, 8, 12),
        (4, 8, 5),
        (4, 7, 3),
        (5, 7, 8),
        (5, 7, 8),
        (5, 7, 8),
        (5, 7, 8),
        (5, 7, 8),
    ]
    vertices = 13  # Number of vertices from 0 to 7
    source = 0  # Source vertex
    sink = 12  # Sink vertex

    max_flow(edges, vertices, source, sink)


if __name__ == "__main__":
    main()

    # [START solver]

