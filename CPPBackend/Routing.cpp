#include "traffic_core.h"

#include <algorithm>
#include <queue>

std::vector<int> dijkstra_route(const TrafficState& state, int startId, int endId, bool emergency) {
    const int n = static_cast<int>(state.nodes.size());
    const double INF = 1e18;
    std::vector<double> dist(n, INF);
    std::vector<int> prev(n, -1);

    using QItem = std::pair<double, int>;
    std::priority_queue<QItem, std::vector<QItem>, std::greater<QItem>> pq;

    dist[startId] = 0.0;
    pq.push({ 0.0, startId });

    while (!pq.empty()) {
        QItem top = pq.top();
        double d = top.first;
        int u = top.second;
        pq.pop();
        if (d != dist[u]) continue;
        if (u == endId) break;

        const auto& adjList = state.adj[u];
        for (size_t idx = 0; idx < adjList.size(); ++idx) {
            const Edge& e = adjList[idx];
            if (e.incident) continue;
            double priorityFactor = (e.priority == RoadPriority::Main) ? 0.8 : (e.priority == RoadPriority::Secondary ? 1.0 : 1.15);
            double maintenanceFactor = e.maintenance ? 2.5 : 1.0;
            double weight = emergency ? e.baseWeight * 0.5 : e.baseWeight * (1.0 + e.congestion) * priorityFactor * maintenanceFactor;
            double nd = d + weight;
            if (nd < dist[e.to]) {
                dist[e.to] = nd;
                prev[e.to] = u;
                pq.push({ nd, e.to });
            }
        }
    }

    if (dist[endId] >= INF) return {};

    std::vector<int> path;
    for (int at = endId; at != -1; at = prev[at]) {
        path.push_back(at);
    }
    std::reverse(path.begin(), path.end());
    return path;
}

void reroute_active(TrafficState& state) {
    for (auto& v : state.vehicles) {
        if (v.completed) continue;
        int current = v.path.empty() ? v.from : static_cast<int>(v.path[v.pathIndex]);
        auto newPath = dijkstra_route(state, current, v.to, v.emergency);
        if (!newPath.empty()) {
            v.path = newPath;
            v.pathIndex = 0;
            v.progress = 0.0;
        }
    }
}

bool add_vehicle(TrafficState& state, const std::string& start, const std::string& dest, bool emergency) {
    auto itS = state.nameToId.find(start);
    auto itD = state.nameToId.find(dest);
    if (itS == state.nameToId.end() || itD == state.nameToId.end() || itS->second == itD->second) return false;

    auto path = dijkstra_route(state, itS->second, itD->second, emergency);
    if (path.empty()) return false;

    Vehicle v;
    v.id = state.nextVehicleId++;
    v.from = itS->second;
    v.to = itD->second;
    v.path = std::move(path);
    v.emergency = emergency;
    switch (v.id % 4) {
    case 0: v.type = VehicleType::Bus; break;
    case 1: v.type = VehicleType::Car; break;
    case 2: v.type = VehicleType::Bike; break;
    default: v.type = VehicleType::Truck; break;
    }
    state.vehicles.push_back(std::move(v));

    state.stats.totalVehicles++;
    if (emergency) state.stats.emergencyVehicles++;
    state.stats.routesCalculated++;
    append_log(state, "Added vehicle");
    return true;
}

