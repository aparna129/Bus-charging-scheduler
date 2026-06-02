from utils.time_utils import time_to_minutes, minutes_to_time
from scheduler.station_manager import StationQueueManager
from scheduler.config import (
    SEGMENT_DISTANCES,
    ROUTE_STATIONS,
    BATTERY_RANGE,
    BUS_SPEED_KMPH,
    CHARGING_TIME_MINUTES
)

class SchedulerEngine:
    def __init__(self, weights):
        self.weights = weights
        self.station_manager = StationQueueManager(["A", "B", "C", "D"])

    def get_route(self, direction):
        return ROUTE_STATIONS if direction == "Bengaluru->Kochi" else list(reversed(ROUTE_STATIONS))

    def get_segment_distance(self, a, b):
        return SEGMENT_DISTANCES.get((a, b)) or SEGMENT_DISTANCES.get((b, a))

    def travel_time(self, km):
        return int((km / BUS_SPEED_KMPH) * 60)

    def priority_score(self, bus):
        op_weight = {
            "kpn": 1.2,
            "freshbus": 1.0,
            "flixbus": 0.9
        }.get(bus.operator.lower(), 1.0)
        return self.weights.get("operator", 1.0) * op_weight

    def compute_stops(self, direction):
        """Maps operational node intervals per direction based on range boundaries."""
        route = self.get_route(direction)
        stops = []
        pos = 0
        while pos < len(route) - 1:
            furthest = pos
            for nxt in range(pos + 1, len(route)):
                dist = sum(self.get_segment_distance(route[k], route[k+1]) for k in range(pos, nxt))
                if dist <= BATTERY_RANGE:
                    furthest = nxt
                else:
                    break
            if furthest == len(route) - 1:
                break
            stops.append(route[furthest])
            pos = furthest
        return stops

    def generate_schedule(self, buses_raw):
    
        self.station_manager = StationQueueManager(["A", "B", "C", "D"])
        
        active_buses = []
        for b in buses_raw:
            route = self.get_route(b.direction)
            planned_stops = self.compute_stops(b.direction)
            dep_min = time_to_minutes(b.departure_time)
            
            active_buses.append({
                "bus_id": b.bus_id,
                "operator": b.operator,
                "direction": b.direction,
                "departure_time": b.departure_time, 
                "route": route,
                "planned_stops": planned_stops,
                "current_time": dep_min,
                "current_node_idx": 0,
                "priority": self.priority_score(b),
                "timeline_events": [],
                "completed": False
            })

        while any(not b["completed"] for b in active_buses):
            ready_buses = [b for b in active_buses if not b["completed"]]
          
            for b in ready_buses:
                curr_idx = b["current_node_idx"]
                route = b["route"]
                
                if b["planned_stops"]:
                    next_stop = b["planned_stops"][0]
                    next_stop_idx = route.index(next_stop)
                else:
                    next_stop = route[-1]
                    next_stop_idx = len(route) - 1
                
                distance = sum(self.get_segment_distance(route[k], route[k+1]) for k in range(curr_idx, next_stop_idx))
                b["next_event_arrival"] = b["current_time"] + self.travel_time(distance)
                b["next_stop_name"] = next_stop
                b["next_stop_idx"] = next_stop_idx

            ready_buses.sort(key=lambda x: (x["next_event_arrival"], -x["priority"], x["bus_id"]))
           
            next_bus = ready_buses[0]
            target_station = next_bus["next_stop_name"]
            arrival_at_station = next_bus["next_event_arrival"]
            
            if target_station in ["Bengaluru", "Kochi"]:
                next_bus["current_time"] = arrival_at_station
                next_bus["completed"] = True
                next_bus["final_arrival_minute"] = arrival_at_station
            else:
                charge_start, charge_end = self.station_manager.allocate_charger(
                    station=target_station,
                    arrival_time=arrival_at_station,
                    bus_id=next_bus["bus_id"]
                )
                
                next_bus["timeline_events"].append({
                    "station": target_station,
                    "arrival": minutes_to_time(arrival_at_station),
                    "start_charging": minutes_to_time(charge_start),
                    "charging_end": minutes_to_time(charge_end)
                })
                
                next_bus["current_time"] = charge_end
                next_bus["current_node_idx"] = next_bus["next_stop_idx"]
                next_bus["planned_stops"].pop(0)

        output_timeline = []
        for b in active_buses:
            output_timeline.append({
                "bus_id": b["bus_id"],
                "direction": b["direction"],
                "departure": b["departure_time"],
                "timeline": b["timeline_events"],
                "final_arrival": minutes_to_time(b["final_arrival_minute"])
            })
            
        return output_timeline