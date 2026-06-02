# Architectural Flow Design

## Step 1: Presentation Layer (`app.py`)
* Parses raw scenario configurations from local disk arrays.
* Maps JSON dictionary entities directly into `Bus` object wrappers.
* Hands the complete collection to the engine and renders the final sorted collections using `st.json()`.

## Step 2: Sequential Simulation Engine (`SchedulerEngine`)
* Iterates through the collection of buses chronologically based on initial departure times.
* Calculates active travel times, range depletion factors, and boundary arrival timestamps step-by-step.
* Evaluates route state to determine exactly when a charging event must be executed.

## Step 3: Resource Contention Resolution Layer (`StationManager`)
* Operates interactively with the engine loop rather than as a post-processing batch.
* Evaluates incoming bus arrivals against existing charger bay time-allocations.
* Injects necessary waiting constraints if a station collision occurs.
* Updates the shared `final_schedule` log, which the engine immediately uses to calculate subsequent downstream legs for that bus.