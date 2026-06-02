import streamlit as st
import json
import os

from scheduler.scheduler_engine import SchedulerEngine
from utils.time_utils import minutes_to_time

st.set_page_config(page_title="Bus Charging Scheduler", layout="wide")

st.title("🚍 Bus Charging Scheduler")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_scenario(file_name):
    file_path = os.path.join(BASE_DIR, file_name)
    with open(file_path, "r") as f:
        return json.load(f)

scenario_files = {
    "Scenario 1": "data/scenario_1.json",
    "Scenario 2": "data/scenario_2.json",
    "Scenario 3": "data/scenario_3.json",
    "Scenario 4": "data/scenario_4.json",
    "Scenario 5": "data/scenario_5.json",
}

selected = st.selectbox("Choose Scenario", list(scenario_files.keys()))

data = load_scenario(scenario_files[selected])

class Bus:
    def __init__(self, d):
        self.bus_id = d["bus_id"]
        self.operator = d["operator"]
        self.direction = d["direction"]
        self.departure_time = d["departure_time"]

buses = [Bus(b) for b in data["buses"]]

weights = {
    "operator": 1.0
}

engine = SchedulerEngine(weights)

result = engine.generate_schedule(buses)

st.subheader("📌 Per Bus Timetable")

for r in result:
    st.markdown(f"### {r['bus_id']}")
    st.write(f"Direction: {r['direction']}")
    st.write(f"Departure: {r['departure']}")
    st.write(f"Final Arrival: {r['final_arrival']}")
    st.json(r["timeline"])

st.divider()

st.subheader("🏁 Station-wise Queue (Final Schedule)")

station_data = engine.station_manager.final_schedule

station_map = {}

for bus_id, stops in station_data.items():
    for stop in stops:
        station_map.setdefault(stop["station"], []).append({
            "bus_id": bus_id,
            "start_mins": stop["start"],  
            "end_mins": stop["end"]       
        })

for station in sorted(station_map.keys()):
    st.markdown(f"### Station {station}")
   
    sorted_raw_entries = sorted(station_map[station], key=lambda x: x["start_mins"])
 
    final_display_entries = []
    for entry in sorted_raw_entries:
        final_display_entries.append({
            "bus_id": entry["bus_id"],
            "start": minutes_to_time(entry["start_mins"]),
            "end": minutes_to_time(entry["end_mins"])
        })
        
    st.json(final_display_entries)