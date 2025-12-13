#include "traffic_core.h"

#include <chrono>

namespace {
    double rand01(std::mt19937& rng) {
        std::uniform_real_distribution<double> dist(0.0, 1.0);
        return dist(rng);
    }

    void add_edge(TrafficState& s, int u, int v, double w) {
        s.adj[u].push_back(Edge{ v, w, 0.3 + 0.4 * rand01(s.rng), false, 0, RoadPriority::Secondary, false });
        s.adj[v].push_back(Edge{ u, w, 0.3 + 0.4 * rand01(s.rng), false, 0, RoadPriority::Secondary, false });
    }
} // namespace

TrafficState make_sample_state() {
    TrafficState state;
    state.rng.seed(static_cast<unsigned>(std::chrono::steady_clock::now().time_since_epoch().count()));

    const std::vector<std::pair<std::string, std::pair<double, double>>> coords = {
        {"A", {100, 120}}, {"B", {300, 120}}, {"C", {500, 120}}, {"J", {700, 120}},
        {"D", {100, 260}}, {"E", {300, 260}}, {"F", {500, 260}}, {"K", {700, 260}},
        {"G", {100, 400}}, {"H", {300, 400}}, {"I", {500, 400}}, {"L", {700, 400}},
        {"M", {100, 540}}, {"N", {300, 540}}, {"O", {500, 540}}, {"P", {700, 540}},
    };

    state.nodes.reserve(coords.size());
    state.adj.assign(coords.size(), {});

    int idx = 0;
    for (const auto& c : coords) {
        Node n;
        n.name = c.first;
        n.id = idx;
        n.x = c.second.first;
        n.y = c.second.second;
        n.green = rand01(state.rng) > 0.5;
        n.greenDuration = 40;
        n.redDuration = 40;
        n.timer = 20 + 40 * rand01(state.rng);
        state.nodes.push_back(n);
        state.nameToId[n.name] = idx;
        ++idx;
    }

    // Core grid
    add_edge(state, 0, 1, 10); add_edge(state, 1, 2, 8);  add_edge(state, 2, 3, 9);
    add_edge(state, 4, 5, 8);  add_edge(state, 5, 6, 7);  add_edge(state, 6, 7, 9);
    add_edge(state, 8, 9, 9);  add_edge(state, 9, 10, 7); add_edge(state, 10, 11, 8);
    add_edge(state, 12, 13, 9); add_edge(state, 13, 14, 7); add_edge(state, 14, 15, 8);

    // Verticals
    add_edge(state, 0, 4, 7); add_edge(state, 4, 8, 10); add_edge(state, 8, 12, 9);
    add_edge(state, 1, 5, 6); add_edge(state, 5, 9, 6);  add_edge(state, 9, 13, 8);
    add_edge(state, 2, 6, 9); add_edge(state, 6, 10, 8); add_edge(state, 10, 14, 7);
    add_edge(state, 3, 7, 9); add_edge(state, 7, 11, 8); add_edge(state, 11, 15, 7);

    // Diagonals / cross links
    add_edge(state, 1, 4, 6);
    add_edge(state, 2, 5, 6);
    add_edge(state, 5, 8, 7);
    add_edge(state, 6, 9, 7);
    add_edge(state, 9, 12, 8);
    add_edge(state, 10, 13, 8);

    // Mark main vertical roads as higher priority (columns B/E/H/N)
    auto mark_main = [&](int id) {
        for (auto& e : state.adj[id]) e.priority = RoadPriority::Main;
    };
    mark_main(1); mark_main(5); mark_main(9); mark_main(13);

    return state;
}

void reset_state(TrafficState& state) {
    state = make_sample_state();
    append_log(state, "Reset simulation");
}

