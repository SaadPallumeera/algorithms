#include <bits/stdc++.h>
using namespace std;

// Implementation of Hopcroft-Karp algorithm for maximum bipartite matching
// Left side vertices are 1..n, right side are 1..m

struct HopcroftKarp {
    int n, m;
    vector<vector<int>> adj;    
    vector<int> pairU, pairV, dist; 
    const int INF = 1e9;

    HopcroftKarp(int n, int m) : n(n), m(m) {
        adj.assign(n + 1, {});
        pairU.assign(n + 1, 0);
        pairV.assign(m + 1, 0);
        dist.assign(n + 1, 0);
    }

    // add edge from left vertex u to right vertex v
    void addEdge(int u, int v) {
        adj[u].push_back(v);
    }

    // BFS builds layers and returns true if there is an augmenting path
    bool bfs() {
        queue<int> q;
        for (int u = 1; u <= n; u++) {
            if (pairU[u] == 0) {
                dist[u] = 0;
                q.push(u);
            } else {
                dist[u] = INF;
            }
        }
        int found = INF;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            if (dist[u] < found) {
                for (int v : adj[u]) {
                    if (pairV[v] == 0) {
                        // free vertex on right, potential shortest augmenting path
                        found = dist[u] + 1;
                    } else if (dist[pairV[v]] == INF) {
                        dist[pairV[v]] = dist[u] + 1;
                        q.push(pairV[v]);
                    }
                }
            }
        }
        return found != INF;
    }

    // DFS to find augmenting paths following layers
    bool dfs(int u) {
        for (int v : adj[u]) {
            if (pairV[v] == 0 || (dist[pairV[v]] == dist[u] + 1 && dfs(pairV[v]))) {
                pairU[u] = v;
                pairV[v] = u;
                return true;
            }
        }
        dist[u] = INF;
        return false;
    }


    int maxMatching() {
        int matching = 0;
        while (bfs()) {
            for (int u = 1; u <= n; u++) {
                if (pairU[u] == 0 && dfs(u)) {
                    matching++;
                }
            }
        }
        return matching;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, e;

    cin >> n >> m >> e;
    HopcroftKarp hk(n, m);
    for (int i = 0; i < e; i++) {
        int u, v;
        cin >> u >> v;
        hk.addEdge(u, v);
    }

    int result = hk.maxMatching();
    cout << result << "\n";
    return 0;
}