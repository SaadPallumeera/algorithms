#include <iostream>
#include <vector>
#include <stack>
#include <queue>
#include <algorithm>
#include <cmath>
#include <cassert>

using namespace std;

class TwoSAT {
public:
    int n, N;
    vector<vector<int>> g, gr;
    vector<int> order, comp;
    vector<bool> used;

    TwoSAT(int vars): n(vars), N(2 * vars), g(N), gr(N), used(N, false), comp(N, -1) {}

    inline int idx(int x) {
        int v = abs(x) - 1;
        return 2 * v + (x < 0);
    }

    void addImplication(int u, int v) {
        g[u].push_back(v);
        gr[v].push_back(u);
    }

    void addClause(int x, int y) {
        int u = idx(x), v = idx(y);
        addImplication(u ^ 1, v);
        addImplication(v ^ 1, u);
    }

    void dfs1(int v) {
        used[v] = true;
        for (int to : g[v]) {
            if (!used[to]) dfs1(to);
        }
        order.push_back(v);
    }

    void dfs2(int v, int cid) {
        comp[v] = cid;
        for (int to : gr[v]) {
            if (comp[to] == -1) dfs2(to, cid);
        }
    }

    bool solve(vector<bool> &ans) {
        order.clear();
        fill(used.begin(), used.end(), false);
        fill(comp.begin(), comp.end(), -1);

        for (int i = 0; i < N; i++) {
            if (!used[i]) dfs1(i);
        }

        int cid = 0;
        for (int i = N - 1; i >= 0; i--) {
            int v = order[i];
            if (comp[v] == -1) dfs2(v, cid++);
        }

        ans.assign(n, false);
        for (int i = 0; i < n; i++) {
            if (comp[2 * i] == comp[2 * i + 1])
                return false;  // UNSAT
            ans[i] = (comp[2 * i] > comp[2 * i + 1]);
        }
        return true;
    }
};

void runTest(int vars,const vector<pair<int,int>>& clauses,int id){
    TwoSAT solver(vars);
    for(auto [x,y]:clauses){
        assert(x!=0 && y!=0 && "Literal cannot be 0");
        assert(abs(x)<=vars && abs(y)<=vars && "Literal out of range");
        solver.addClause(x,y);
    }
    vector<bool> val; bool sat=solver.solve(val);
    cout<<"Test #"<<id<<": ";
    if(!sat){ cout<<"UNSAT\n"; return; }
    cout<<"SAT  ";
    for(int i=0;i<vars;++i){ cout<<(val[i]?1:0); if(i+1<vars) cout<<' '; }
    cout<<"\n";
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // ===== Define multiple test cases ===== //
    struct Case{int vars; vector<pair<int,int>> cls;};
    vector<Case> tests = {
        // 3‑var example (SAT)
        {3, {{1,2},{-1,3},{-2,-3}}},
        // 1‑var UNSAT: x ∧ ¬x
        {1, {{1,1},{-1,-1}}},
        // 15‑var chain example (SAT)
        {15, {
            {  1,  2},{ -1,  3},{ -2,  4},{ -3,  5},{ -4,  6},
            { -5,  7},{ -6,  8},{ -7,  9},{ -8, 10},{ -9, 11},
            {-10, 12},{-11, 13},{-12, 14},{-13, 15},{-14,-15}
        }}
    };

    int id=1;
    for(const auto& t:tests){ runTest(t.vars,t.cls,id++); }
    return 0;
}


