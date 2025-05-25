from ortools.init.python import init
from ortools.linear_solver import pywraplp
from collections import defaultdict


def mincostmatching(A,B,edges):
    edge_vars = {}
    weights = defaultdict(list)
    A_edges = defaultdict(list)
    B_edges = defaultdict(list)

    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        print("Solver not created.")
        return

    for i in edges: 
        var = solver.NumVar(0, 1, f'var_{i[0]}_{i[1]}')
        edge_vars[f'var_{i[0]}_{i[1]}'] = var
        A_edges[i[0]].append(f'var_{i[0]}_{i[1]}')
        B_edges[i[1]].append(f'var_{i[0]}_{i[1]}')
        weights[var] = i[2]


    for vertice in A_edges: 
        constraint = 0
        for i in A_edges[vertice]:
            constraint += edge_vars[i]
        solver.Add(constraint == 1)

    for vertice in B_edges: 
        constraint = 0
        for i in B_edges[vertice]:
            constraint += edge_vars[i]
        solver.Add(constraint == 1)

    #set objective
    objective = solver.Objective()

    for i in edges: 
        var = edge_vars[f'var_{i[0]}_{i[1]}']
        objective.SetCoefficient(var,weights[var])
    objective.SetMinimization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('edge matched', objective.Value())
        for  var in edge_vars:
            print(var, end = " ")
            print(edge_vars[var].solution_value())
    else:
        print('No optimal solution found.')
    
    #task 2 dual solution
    solver2 = pywraplp.Solver.CreateSolver("GLOP")

    if not solver:
        print("Solver not created.")
        return
    
    vertice_vars_A ={}
    vertice_vars_B ={}

    for i in range(1,A+1): 
        var = solver2.NumVar(0, solver2.infinity(), f'var_{i}')
        vertice_vars_A[f'var_{i}'] = var

    for i in range(1,A+1): 
        var = solver2.NumVar(0, solver2.infinity(), f'var_{i}')
        vertice_vars_B[f'var_{i}'] = var

    for i in edges: 
        constraint = 0
        constraint += vertice_vars_A[f'var_{i[0]}']
        constraint += vertice_vars_B[f'var_{i[1]}']
        solver2.Add(constraint <= i[2])
    
    objective2 = solver2.Objective()

    for i in range(1,A+1):
        var = vertice_vars_A[f'var_{i}']
        objective2.SetCoefficient(var,1)
    
    for i in range(1,B+1):
        var = vertice_vars_B[f'var_{i}']
        objective2.SetCoefficient(var,1)

    objective2.SetMaximization()

    status2 = solver2.Solve()

    if status2 == pywraplp.Solver.OPTIMAL:
        print('\n\nvertice_val', objective2.Value())
        for  var in vertice_vars_A:
            print(var, end = " ")
            print(vertice_vars_A[var].solution_value())
        for  var in vertice_vars_B:
            print(var, end = " ")
            print(vertice_vars_A[var].solution_value())
    else:
        print('No optimal solution found.')
    







    print (weights)
    #first we want to create variables for all of the edges 

def main():
    print('hello')
    edges = [
        (1, 1, 2), (1, 2, 3), (1, 3, 4), (1, 4, 1),
        (2, 1, 4), (2, 2, 2), (2, 3, 3), (2, 4, 2),
        (3, 1, 3), (3, 2, 4), (3, 3, 2), (3, 4, 1),
        (4, 1, 2), (4, 2, 1), (4, 3, 3), (4, 4, 4),
    ]
    mincostmatching(4, 4, edges)

if __name__ == "__main__":
    main()
