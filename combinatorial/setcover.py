
"""Minimal example to call the GLOP solver."""
# [START program]
# [START import]
from ortools.init.python import init
from ortools.linear_solver import pywraplp
from collections import defaultdict

#solves using linear programming with greedy approach to rounding 
def approx_set_cover(elements, sets, weights): 
    element_vars = defaultdict(list)
    set_vars = []

    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        print("Solver not created.")
        return

    # Create variable for each element (indicator variable)
    for i in elements: 
        var = solver.NumVar(1, solver.infinity(), f'var_{i}')
        element_vars[var] = var

    # Create binary variable for each set
    for set_index in range(len(sets)): 
        var = solver.NumVar(0, 1, f'set_{set_index}')
        set_vars.append(var)
    
    element_sets = defaultdict(list)

    for set_index in range(len(sets)): 
        for j in sets[set_index]: 
            element_sets[j].append(set_index)

    # Create constraints for how much each element must be covered
    for i in elements: 
        constraint_sets = solver.Sum([set_vars[j] for j in element_sets[i]])
        solver.Add(constraint_sets >= 1)
    
    # Objective: minimize the total weight of sets used
    solver.Minimize(solver.Sum([set_vars[i] * weights[i] for i in range(len(set_vars))]))
    
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Optimal solution found.')
        
        # Output the LP variable values
        lp_values = [var.solution_value() for var in set_vars]
        for i in range(len(set_vars)):
            print(f'set_{i} = {lp_values[i]}')
        
        # Greedy rounding based on the LP values
        sorted_indices = sorted(range(len(set_vars)), key=lambda i: lp_values[i], reverse=True)
        
        selected_sets = set()
        covered_elements = set()
        for i in sorted_indices:
            if not covered_elements.issuperset(elements):
                selected_sets.add(i)
                covered_elements.update(sets[i])

        print('Total weight of selected sets:', sum(weights[i] for i in selected_sets))

    else:
        print('No optimal solution found.')

#solves using integer programming gaurunteeing optimal results
def optimal_set_cover(elements,sets,weights):
    element_vars = defaultdict(list)
    set_vars = []

    solver = pywraplp.Solver.CreateSolver("SAT")
    if not solver:
        print("Solver not created.")
        return

    # Create variable for each element (indicator variable)
    for i in elements: 
        var = solver.NumVar(1, solver.infinity(), f'var_{i}')
        element_vars[var] = var

    # Create binary variable for each set
    for set_index in range(len(sets)): 
        var = solver.NumVar(0, 1, f'set_{set_index}')
        set_vars.append(var)
    
    element_sets = defaultdict(list)

    for set_index in range(len(sets)): 
        for j in sets[set_index]: 
            element_sets[j].append(set_index)

    # Create constraints for how much each element must be covered
    for i in elements: 
        constraint_sets = solver.Sum([set_vars[j] for j in element_sets[i]])
        solver.Add(constraint_sets >= 1)
    
    # Objective: minimize the total weight of sets used
    solver.Minimize(solver.Sum([set_vars[i] * weights[i] for i in range(len(set_vars))]))
    
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Optimal solution found.')
        
        # Output the LP variable values
        lp_values = [var.solution_value() for var in set_vars]
        for i in range(len(set_vars)):
            print(f'set_{i} = {lp_values[i]}')
        
        # Greedy rounding based on the LP values
        sorted_indices = sorted(range(len(set_vars)), key=lambda i: lp_values[i], reverse=True)
        
        selected_sets = set()
        covered_elements = set()
        for i in sorted_indices:
            if not covered_elements.issuperset(elements):
                selected_sets.add(i)
                covered_elements.update(sets[i])

        print("\nGreedy Rounded Solution:")
        print('Selected sets:', selected_sets)
        print('Total weight of selected sets:', sum(weights[i] for i in selected_sets))

    else:
        print('No optimal solution found.')



def main():
    # New test case where the optimal and approximation differ
    elements = {1, 2, 3, 4, 5, 6}
    sets = [
        {1, 2},    # Set 0
        {2, 3},    # Set 1
        {3, 4},    # Set 2
        {4, 5},    # Set 3
        {5, 6},    # Set 4
        {1, 3, 5}, # Set 5
        {2, 4, 6}  # Set 6
    ]
    weights = [3, 2, 5, 4, 1, 7, 6]

    print("Approximation (Greedy) Solution:")
    approx_set_cover(elements, sets, weights)

    print("\nOptimal Solution:")
    optimal_set_cover(elements, sets, weights)

if __name__ == "__main__":
    main()

