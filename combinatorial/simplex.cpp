#include <iostream>
#include <vector>
#include <limits>

using namespace std;

class LinearProgram {
private:
    vector<vector<double>> tableau;
    vector<double> solution;
    int numVariables;
    int numConstraints;

public:
    LinearProgram(int numVariables, int numConstraints)
        : numVariables(numVariables), numConstraints(numConstraints) {
        tableau.resize(numConstraints + 1, vector<double>(numVariables + numConstraints + 1, 0));
        solution.resize(numVariables, 0.0);
    }

    void setObjective(const vector<double>& objective) {
        for (int i = 0; i < numVariables; ++i) {
            tableau[0][i] = -objective[i];
        }
    }

    void addConstraint(const vector<double>& constraint, double value, int index) {
        for (int i = 0; i < numVariables; ++i) {
            tableau[index + 1][i] = constraint[i];
        }
        tableau[index + 1][numVariables + numConstraints] = value;
        tableau[index + 1][numVariables + index] = 1.0;
    }

    void solve() {
        while (true) {
            int pivotCol = -1;
            double minValue = 0;
            
            // Find the entering variable (most negative coefficient in objective row)
            for (int i = 0; i < numVariables + numConstraints; ++i) {
                if (tableau[0][i] < minValue) {
                    minValue = tableau[0][i];
                    pivotCol = i;
                }
            }
            
            // If there are no negative coefficients in the objective row, we are done
            if (pivotCol == -1) break;

            // Find the leaving variable (smallest ratio test)
            int pivotRow = -1;
            double minRatio = numeric_limits<double>::max();

            for (int i = 1; i <= numConstraints; ++i) {
                if (tableau[i][pivotCol] > 0) {
                    double ratio = tableau[i][numVariables + numConstraints] / tableau[i][pivotCol];
                    if (ratio < minRatio) {
                        minRatio = ratio;
                        pivotRow = i;
                    }
                }
            }

            // If there is no valid pivot row, the problem is unbounded
            if (pivotRow == -1) {
                cout << "Unbounded solution" << endl;
                return;
            }

            // Perform the pivot operation
            pivot(pivotRow, pivotCol);
        }

        // Extract solution
        for (int i = 0; i < numVariables; ++i) {
            bool isBasic = false;
            for (int j = 1; j <= numConstraints; ++j) {
                if (tableau[j][i] == 1.0) {
                    solution[i] = tableau[j][numVariables + numConstraints];
                    isBasic = true;
                    break;
                }
            }
            if (!isBasic) solution[i] = 0;
        }
    }

    void pivot(int pivotRow, int pivotCol) {
        double pivotValue = tableau[pivotRow][pivotCol];

        // Normalize the pivot row
        for (int i = 0; i <= numVariables + numConstraints; ++i) {
            tableau[pivotRow][i] /= pivotValue;
        }

        // Eliminate the pivot column entries in other rows
        for (int i = 0; i <= numConstraints; ++i) {
            if (i != pivotRow) {
                double factor = tableau[i][pivotCol];
                for (int j = 0; j <= numVariables + numConstraints; ++j) {
                    tableau[i][j] -= factor * tableau[pivotRow][j];
                }
            }
        }
    }

    void printSolution() {
        for (int i = 0; i < numVariables; ++i) {
            cout << "x" << i + 1 << " = " << solution[i] << endl;
        }
    }
};
/*
int main() {
    int numVariables = 3;
    int numConstraints = 3;

    LinearProgram lp(numVariables, numConstraints);

    vector<double> objective = {1, 1, 1};
    lp.setObjective(objective);

    lp.addConstraint({1, 0, 0}, 50, 0); // x1 + x2 + x3 <= 100
    lp.addConstraint({0, 1, 0}, 100, 1); // 10x1 + 4x2 + 5x3 <= 600
    lp.addConstraint({0, 0, 1}, 100, 2); // 2x1 + 2x2 + 6x3 <= 300
    

    lp.solve();
    lp.printSolution();

    return 0;
} */