#include "traffic_core.h"

#include <algorithm>

namespace {
    double rand01(std::mt19937& rng) {
        std::uniform_real_distribution<double> dist(0.0, 1.0);
        return dist(rng);
    }

    double speed_multiplier(VehicleType type) {
        switch (type) {
        case VehicleType::Bus: return 0.8;
        case VehicleType::Bike: return 0.9;
        case VehicleType::Truck: return 0.7;
        case VehicleType::Car:
        default: return 1.0;
        }
    }
} // namespace

Edge* find_edge(TrafficState& s, int u, int v) {
    for (auto& e : s.adj[u]) {
        if (e.to == v) return &e;
    }
    return nullptr;
}

void step_simulation(TrafficState& state) {
    // Virtual clock tick (6 AM start). Each step ~6 minutes.
    state.simTimeHours += 0.1;
    if (state.simTimeHours >= 24.0) state.simTimeHours = 0.0;

    // Adjust signals based on local congestion
    for (auto& node : state.nodes) {
        double sum = 0.0;
        int cnt = 0;
        for (const auto& e : state.adj[node.id]) {
            sum += e.congestion;
            ++cnt;
        }
        double avg = cnt ? sum / cnt : 0.3;
        node.greenDuration = 35.0 * (1.0 + 0.7 * avg);
        node.redDuration = 35.0 * (1.0 - 0.4 * avg);
        node.timer -= 0.1;
        if (node.timer <= 0) {
            node.green = !node.green;
            node.timer = node.green ? node.greenDuration : node.redDuration;
        }
    }

    // Congestion drift (manual clamp to avoid relying on C++17 clamp)
    for (auto& vec : state.adj) {
        for (auto& e : vec) {
            double rushFactor = (state.simTimeHours >= 7.0 && state.simTimeHours <= 9.0) || (state.simTimeHours >= 17.0 && state.simTimeHours <= 19.0) ? 0.08 : 0.05;
            double updated = e.congestion + (rand01(state.rng) - 0.5) * rushFactor;
            if (updated < 0.05) updated = 0.05;
            if (updated > 1.0) updated = 1.0;
            e.congestion = updated;
        }
    }

    // Vehicle motion
    const double baseSpeed = 0.02;
    for (auto& v : state.vehicles) {
        if (v.completed || v.pathIndex >= v.path.size() - 1) {
            v.completed = true;
            continue;
        }

        int u = v.path[v.pathIndex];
        int w = v.path[v.pathIndex + 1];
        Edge* e = find_edge(state, u, w);
        if (!e) {
            v.completed = true;
            continue;
        }

        bool canGo = v.emergency || state.nodes[u].green || v.progress >= 0.5;
        if (!canGo) continue;

        double speed = baseSpeed * (v.emergency ? 2.2 : 1.0) * (1.2 - e->congestion) * speed_multiplier(v.type);
        if (e->maintenance) speed *= 0.35;
        v.progress += std::max(0.002, speed);

        if (v.progress >= 1.0) {
            v.pathIndex++;
            v.progress = 0.0;
            e->usage += 1;
            v.distanceTraveled += e->baseWeight;
            if (v.pathIndex >= v.path.size() - 1) {
                v.completed = true;
            }
        }
    }

    // Recompute aggregated distance
    state.stats.totalDistance = 0.0;
    for (const auto& v : state.vehicles) {
        state.stats.totalDistance += v.distanceTraveled;
    }
}

