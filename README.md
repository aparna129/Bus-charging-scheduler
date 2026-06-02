1. Project Overview:
   The Bus Charging Scheduler is a web-based optimization and simulation dashboard built with Streamlit. It solves the operational problem of scheduling electric intercity fleet buses traveling between Bengaluru and Kochi. The core engine ensures that buses are charged adequately along their route while managing infrastructure bottlenecks - specifically, a constraint where each charging station has only one available charging bay.

2. Key Features:

- Interactive Scenario Selector: Easily switch between 5 different operational scenarios via a dropdown menu to test how the scheduler handles different fleets.

- Discrete Event Simulation Engine: Dynamically calculates travel timelines, battery depletion, and cascading downstream delays on-the-fly.

- FIFO Charging Queue Resolution: Eliminates resource conflicts at charging stations by ensuring buses wait their turn if a bay is occupied.

- Alphabetically Sorted Dashboards: Station queues are cleanly presented in alphabetical order (Station A, B, C, D) for easier tracking.

- Perfect Chronological Alignment: Time formatting tracks seamlessly across the midnight barrier, displaying clear HH:MM 24-hour clock strings.

3. Project Directory Structure:
bus-charging-scheduler/
   data/
      scenario_1.json
      scenario_2.json
      scenario_3.json
      scenario_4.json
      scenario_5.json
   scheduler/
      scheduler_engine.py
   utils/
      time_utils.py
   app.py
   ARCHITECTURE.md
   README.md
   requirements.txt

4. Installation & Setup Instructions:
   4.1 Prerequisites
   Make sure you have Python 3.10+ installed on your machine.

   4.2 Step 1: Install Required Libraries
   Open your terminal or command prompt, navigate to your project directory, and install Streamlit:
   pip install streamlit

   4.3 Step 2: Run the Application
   Launch the local Streamlit web server by running:
   streamlit run app.py

   4.4 Step 3: View the Dashboard
   Once the server starts, it will automatically open your default web browser to:
   http://localhost:8501
   (If it doesn't open automatically, you can copy and paste that address into your browser).

5. How to Use the Application:
   Select a Scenario: Use the "Choose Scenario" dropdown at the very top of the webpage to select any scenario (Scenario 1 to Scenario 5).

   Review Per-Bus Timetables: Look through the "📌 Per Bus Timetable" section to trace individual bus paths, view their custom      departure/arrival times, and look inside their expandable timeline logs to track exactly when they arrive and finish charging.

   Verify Station Queues: Scroll to the bottom "🏁 Station-wise Queue (Final Schedule)" section to examine the fleet from the charging stations' perspective. Verify that no two buses share an overlapping slot and that all queues are ordered perfectly by time.
