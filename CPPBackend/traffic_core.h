#pragma once

#include <random>
#include <string>
#include <unordered_map>
#include <vector>

enum class RoadPriority {
    Main = 1,
    Secondary = 2,
    Lane = 3
};

enum class VehicleType {
    Car,
    Bus,
    Bike,
    Truck
};

struct Edge {
    int to = 0;
    double baseWeight = 0.0;
    double congestion = 0.0;
    bool incident = false;
    int usage = 0;
    RoadPriority priority = RoadPriority::Secondary;
    bool maintenance = false; // slows traffic heavily
};

struct Node {
    std::string name;
    int id = 0;
    double x = 0.0;
    double y = 0.0;
    bool green = true;
    double greenDuration = 40.0;
    double redDuration = 40.0;
    double timer = 0.0;
};

struct Vehicle {
    int id = 0;
    int from = 0;
    int to = 0;
    std::vector<int> path;
    size_t pathIndex = 0;
    double progress = 0.0;
    bool emergency = false;
    bool completed = false;
    double distanceTraveled = 0.0;
    VehicleType type = VehicleType::Car;
    double speedMultiplier = 1.0;
};

struct Stats {
    int totalVehicles = 0;
    int emergencyVehicles = 0;
    int routesCalculated = 0;
    int incidentsReported = 0;
    double totalDistance = 0.0;
};

struct TrafficState {
    std::vector<Node> nodes;
    std::vector<std::vector<Edge>> adj;
    std::mt19937 rng{ std::random_device{}() };
    std::unordered_map<std::string, int> nameToId;
    std::vector<Vehicle> vehicles;
    Stats stats;
    int nextVehicleId = 1;
    double simTimeHours = 6.0; // virtual clock, starts at 6 AM
};

TrafficState make_sample_state();
std::vector<int> dijkstra_route(const TrafficState& state, int startId, int endId, bool emergency);
void reroute_active(TrafficState& state);
bool add_vehicle(TrafficState& state, const std::string& start, const std::string& dest, bool emergency);
void step_simulation(TrafficState& state);
void add_random_incident(TrafficState& state);
void clear_all_incidents(TrafficState& state);
void reset_state(TrafficState& state);
std::string snapshot_json(const TrafficState& state);
void append_log(const TrafficState& state, const std::string& note);
Edge* find_edge(TrafficState& state, int u, int v);
bool set_signal_state(TrafficState& state, const std::string& nodeName, bool green);
bool set_signal_timing(TrafficState& state, const std::string& nodeName, double greenDur, double redDur);
bool set_block(TrafficState& state, const std::string& from, const std::string& to, bool blocked);
bool set_maintenance(TrafficState& state, const std::string& from, const std::string& to, bool on);
bool save_snapshot(const TrafficState& state, const std::string& path);
bool load_snapshot(TrafficState& state, const std::string& path);
void serve_stdin();





