class StationQueueManager:
    def __init__(self, stations):
        self.station_free_time = {s: 0 for s in stations}
    
        self.final_schedule = {}

    def allocate_charger(self, station, arrival_time, bus_id):
        """
        Dynamically allocates a charger to a bus based on its true arrival time,
        properly accounting for any queue or delay from preceding buses.
        """
      
        start_charging = max(arrival_time, self.station_free_time[station])
        wait_time = start_charging - arrival_time
        end_charging = start_charging + 25

        self.station_free_time[station] = end_charging

        event = {
            "station": station,
            "arrival": arrival_time,
            "wait_time": wait_time,
            "start": start_charging,
            "end": end_charging
        }

        if bus_id not in self.final_schedule:
            self.final_schedule[bus_id] = []
        self.final_schedule[bus_id].append(event)

        return start_charging, end_charging