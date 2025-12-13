#include "traffic_core.h"

#include <chrono>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>

namespace {
    double now_seconds() {
        using clock = std::chrono::system_clock;
        return std::chrono::duration<double>(clock::now().time_since_epoch()).count();
    }

    std::vector<std::string> split(const std::string& line) {
        std::vector<std::string> parts;
        std::istringstream iss(line);
        std::string p;
        while (iss >> p) parts.push_back(p);
        return parts;
    }
} // namespace

std::string snapshot_json(const TrafficState& state) {
    std::ostringstream out;
    out << std::fixed << std::setprecision(3);
    out << "{";
    out << "\"time\":" << state.simTimeHours << ",";
    out << "\"nodes\":[";
    for (size_t i = 0; i < state.nodes.size(); ++i) {
        const auto& n = state.nodes[i];
        if (i) out << ",";
        out << "{"
            << "\"id\":" << n.id << ",\"name\":\"" << n.name << "\","
            << "\"x\":" << n.x << ",\"y\":" << n.y << ","
            << "\"green\":" << (n.green ? "true" : "false") << ","
            << "\"timer\":" << n.timer
            << "}";
    }
    out << "],";

    out << "\"roads\":[";
    bool firstRoad = true;
    for (size_t u = 0; u < state.adj.size(); ++u) {
        for (const auto& e : state.adj[u]) {
            if (u < static_cast<size_t>(e.to)) { // avoid duplicate undirected
                if (!firstRoad) out << ",";
                firstRoad = false;
                out << "{"
                    << "\"from\":" << u << ",\"to\":" << e.to << ","
                    << "\"w\":" << e.baseWeight << ","
                    << "\"c\":" << e.congestion << ","
                    << "\"incident\":" << (e.incident ? "true" : "false") << ","
                    << "\"maintenance\":" << (e.maintenance ? "true" : "false") << ","
                    << "\"priority\":" << static_cast<int>(e.priority) << ","
                    << "\"usage\":" << e.usage
                    << "}";
            }
        }
    }
    out << "],";

    out << "\"vehicles\":[";
    for (size_t i = 0; i < state.vehicles.size(); ++i) {
        const auto& v = state.vehicles[i];
        if (i) out << ",";
        out << "{"
            << "\"id\":" << v.id << ","
            << "\"from\":" << v.from << ","
            << "\"to\":" << v.to << ","
            << "\"emergency\":" << (v.emergency ? "true" : "false") << ","
            << "\"type\":" << static_cast<int>(v.type) << ","
            << "\"done\":" << (v.completed ? "true" : "false") << ","
            << "\"progress\":" << v.progress << ","
            << "\"pathIndex\":" << v.pathIndex << ","
            << "\"path\":[";
        for (size_t j = 0; j < v.path.size(); ++j) {
            if (j) out << ",";
            out << v.path[j];
        }
        out << "]";
        out << "}";
    }
    out << "],";

    out << "\"stats\":{"
        << "\"totalVehicles\":" << state.stats.totalVehicles << ","
        << "\"emergencyVehicles\":" << state.stats.emergencyVehicles << ","
        << "\"routesCalculated\":" << state.stats.routesCalculated << ","
        << "\"incidentsReported\":" << state.stats.incidentsReported << ","
        << "\"totalDistance\":" << state.stats.totalDistance
        << "}";
    out << "}";
    return out.str();
}

void append_log(const TrafficState& state, const std::string& note) {
    std::ofstream file("traffic_log_cpp.txt", std::ios::app);
    if (!file) return;
    file << "=== Log @ " << now_seconds() << " ===\n";
    file << note << "\n";
    file << "vehicles=" << state.stats.totalVehicles
        << " emergency=" << state.stats.emergencyVehicles
        << " routes=" << state.stats.routesCalculated
        << " incidents=" << state.stats.incidentsReported
        << " distance=" << state.stats.totalDistance << "\n\n";
}

bool set_signal_state(TrafficState& state, const std::string& nodeName, bool green) {
    auto it = state.nameToId.find(nodeName);
    if (it == state.nameToId.end()) return false;
    auto& n = state.nodes[it->second];
    n.green = green;
    n.timer = green ? n.greenDuration : n.redDuration;
    append_log(state, "Manual signal set for " + nodeName);
    return true;
}

bool set_signal_timing(TrafficState& state, const std::string& nodeName, double greenDur, double redDur) {
    auto it = state.nameToId.find(nodeName);
    if (it == state.nameToId.end()) return false;
    auto& n = state.nodes[it->second];
    n.greenDuration = std::max(5.0, greenDur);
    n.redDuration = std::max(5.0, redDur);
    append_log(state, "Manual timing set for " + nodeName);
    return true;
}

bool set_block(TrafficState& state, const std::string& from, const std::string& to, bool blocked) {
    auto itA = state.nameToId.find(from);
    auto itB = state.nameToId.find(to);
    if (itA == state.nameToId.end() || itB == state.nameToId.end()) return false;
    Edge* e1 = find_edge(state, itA->second, itB->second);
    Edge* e2 = find_edge(state, itB->second, itA->second);
    if (!e1 || !e2) return false;
    e1->incident = e2->incident = blocked;
    append_log(state, std::string("Manual block ") + (blocked ? "on " : "off ") + from + "-" + to);
    reroute_active(state);
    return true;
}

bool set_maintenance(TrafficState& state, const std::string& from, const std::string& to, bool on) {
    auto itA = state.nameToId.find(from);
    auto itB = state.nameToId.find(to);
    if (itA == state.nameToId.end() || itB == state.nameToId.end()) return false;
    Edge* e1 = find_edge(state, itA->second, itB->second);
    Edge* e2 = find_edge(state, itB->second, itA->second);
    if (!e1 || !e2) return false;
    e1->maintenance = e2->maintenance = on;
    append_log(state, std::string("Maintenance ") + (on ? "on " : "off ") + from + "-" + to);
    reroute_active(state);
    return true;
}

bool save_snapshot(const TrafficState& state, const std::string& path) {
    std::ofstream out(path, std::ios::trunc);
    if (!out) return false;
    out << snapshot_json(state);
    return true;
}

bool load_snapshot(TrafficState& state, const std::string& path) {
    // Placeholder: loading would require JSON parsing; return false for now.
    (void)state;
    (void)path;
    return false;
}

void serve_stdin() {
    TrafficState state = make_sample_state();
    std::string line;
    while (std::getline(std::cin, line)) {
        auto args = split(line);
        if (args.empty()) continue;
        const std::string& cmd = args[0];

        if (cmd == "SNAPSHOT") {
            std::cout << snapshot_json(state) << std::endl;
        }
        else if (cmd == "ROUTE" && args.size() >= 4) {
            bool ok = add_vehicle(state, args[1], args[2], args[3] == "1");
            std::cout << (ok ? "OK" : "ERR") << std::endl;
        }
        else if (cmd == "STEP") {
            step_simulation(state);
            std::cout << "OK" << std::endl;
        }
        else if (cmd == "INCIDENT") {
            add_random_incident(state);
            std::cout << "OK" << std::endl;
        }
        else if (cmd == "CLEAR") {
            clear_all_incidents(state);
            std::cout << "OK" << std::endl;
        }
        else if (cmd == "RESET") {
            reset_state(state);
            std::cout << "OK" << std::endl;
        }
        else if (cmd == "REROUTE") {
            reroute_active(state);
            std::cout << "OK" << std::endl;
        }
        else if (cmd == "SET_SIGNAL" && args.size() >= 3) {
            bool ok = set_signal_state(state, args[1], args[2] == "1");
            std::cout << (ok ? "OK" : "ERR") << std::endl;
        }
        else if (cmd == "SET_TIMING" && args.size() >= 4) {
            bool ok = set_signal_timing(state, args[1], std::stod(args[2]), std::stod(args[3]));
            std::cout << (ok ? "OK" : "ERR") << std::endl;
        }
        else if (cmd == "BLOCK" && args.size() >= 3) {
            bool ok = set_block(state, args[1], args[2], true);
            std::cout << (ok ? "OK" : "ERR") << std::endl;
        }
        else if (cmd == "UNBLOCK" && args.size() >= 3) {
            bool ok = set_block(state, args[1], args[2], false);
            std::cout << (ok ? "OK" : "ERR") << std::endl;
        }
        else if (cmd == "MAINT" && args.size() >= 3) {
            bool ok = set_maintenance(state, args[1], args[2], true);
            std::cout << (ok ? "OK" : "ERR") << std::endl;
        }
        else if (cmd == "UNMAINT" && args.size() >= 3) {
            bool ok = set_maintenance(state, args[1], args[2], false);
            std::cout << (ok ? "OK" : "ERR") << std::endl;
        }
        else if (cmd == "SAVE" && args.size() >= 2) {
            bool ok = save_snapshot(state, args[1]);
            std::cout << (ok ? "OK" : "ERR") << std::endl;
        }
        else if (cmd == "LOAD" && args.size() >= 2) {
            bool ok = load_snapshot(state, args[1]);
            std::cout << (ok ? "OK" : "ERR") << std::endl;
        }
        else if (cmd == "QUIT") {
            std::cout << "BYE" << std::endl;
            break;
        }
        else {
            std::cout << "UNKNOWN" << std::endl;
        }
    }
}

