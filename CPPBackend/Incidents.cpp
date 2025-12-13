#include "traffic_core.h"

#include <random>

void add_random_incident(TrafficState& state) {
    if (state.adj.empty()) return;
    std::uniform_int_distribution<int> nodeDist(0, static_cast<int>(state.adj.size()) - 1);
    for (int tries = 0; tries < 20; ++tries) {
        int u = nodeDist(state.rng);
        if (state.adj[u].empty()) continue;
        std::uniform_int_distribution<int> edgeDist(0, static_cast<int>(state.adj[u].size()) - 1);
        int idx = edgeDist(state.rng);
        int v = state.adj[u][idx].to;
        Edge* e1 = find_edge(state, u, v);
        Edge* e2 = find_edge(state, v, u);
        if (!e1 || !e2) continue;
        if (e1->incident || e2->incident) continue;
        e1->incident = e2->incident = true;
        state.stats.incidentsReported++;
        append_log(state, "Incident on edge " + state.nodes[u].name + "-" + state.nodes[v].name);
        reroute_active(state);
        return;
    }
}

void clear_all_incidents(TrafficState& state) {
    for (auto& vec : state.adj) {
        for (auto& e : vec) e.incident = false;
    }
    append_log(state, "Cleared incidents");
    reroute_active(state);
}

