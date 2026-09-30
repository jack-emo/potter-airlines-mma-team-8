# potter-airlines-mma-team-8
## Team Members: Sicily Chang, Nicolas Contreras, Jack Emo, Echo He, Andy Xin

# Potter Airlines Dynamic Revenue Management System

## 1. Project Overview

Potter Airlines is a fictional airline that uses dynamic pricing to adjust fares based on understandable business signals.

The system calculates an adjusted fare for each flight using:

```text
adjusted fare = base fare × time factor × demand factor × capacity factor × seasonal factor
```

The goal is not to build an advanced optimization model, but to demonstrate how changes in booking conditions can affect flight prices in a transparent and explainable way.

Our application uses Python, Pandas, NumPy, SQLite, and object-oriented programming to create, price, store, retrieve, analyze, and update flight data.

---

## 2. Project Workflow

The system follows this workflow:

```text
Generate flight data
        ↓
Save flight data to CSV
        ↓
Load data with Pandas
        ↓
Calculate pricing factors
        ↓
Calculate adjusted fares
        ↓
Store priced flights in SQLite
        ↓
Retrieve and rank flights
        ↓
Update an operational value
        ↓
Recalculate the fare
        ↓
Run validation and edge-case checks
```

The project uses:

* **CSV** for the generated flight dataset
* **Pandas/NumPy** for batch pricing calculations and analysis
* **SQLite** for persistent storage and CRUD operations
* **Python classes and functions** for the application logic

---

## 3. Project Structure

```text
potter-airlines-mma-team-8/
│
├── main.py
├── flight.py
├── pricing.py
├── analysis.py
├── database.py
├── create_data.py
├── constants.py
├── README.md
│
├── potter_flights_generated.csv
└── potter_airlines.db
```

### `main.py`

Runs the complete application workflow, including data generation, pricing, database operations, ranking, operational updates, and validation.

### `flight.py`

Defines the `Flight` class and validates important flight data assumptions.

### `pricing.py`

Contains the pricing functions for time, route demand, capacity, seasonality, and final fare calculation.

### `analysis.py`

Uses Pandas and NumPy-based pricing calculations across multiple flights and provides flight ranking.

### `database.py`

Handles SQLite persistence and CRUD operations.

### `create_data.py`

Generates fictional flight data and saves it to CSV.

### `constants.py`

Stores shared configuration such as file paths, the reference date, random seed, and route demand values.

---

## 4. Flight Data

The generated dataset contains varied fictional flights with:

* Flight ID
* Origin
* Destination
* Departure date
* Base fare
* Capacity
* Seats sold
* Seats remaining

`seats_remaining` is derived as:

```text
seats_remaining = capacity - seats_sold
```

It is calculated rather than independently stored as an operational value so that it cannot become inconsistent with capacity and seats sold.

The dataset is generated using a fixed random seed, making the example data reproducible.

The pricing calculations also use a fixed reference date (`2026-09-13`) so that the same input data produces consistent results when the program is run.

---

## 5. Dynamic Pricing Logic

The pricing model uses four business factors.

### Time Factor

The closer a flight is to departure, the higher the time factor.

| Days to departure | Time factor |
| ----------------- | ----------: |
| 7 days or less    |        1.40 |
| 8–21 days         |        1.20 |
| 22–45 days        |        1.00 |
| More than 45 days |        0.85 |

This represents the idea that fares may increase as departure approaches.

### Demand Factor

Each city is assigned a demand score in `constants.py`.

The route demand factor is calculated from the average demand scores of the origin and destination:

```text
demand factor =
(origin demand + destination demand) / 2
```

This provides a simple and explainable proxy for route demand.

### Capacity Factor

Capacity pressure is based on the proportion of seats remaining.

| Seats remaining      | Capacity factor |
| -------------------- | --------------: |
| 15% or less          |            1.50 |
| More than 15% to 40% |            1.25 |
| More than 40% to 70% |            1.00 |
| More than 70%        |            0.90 |

As fewer seats remain, the capacity factor increases.

### Seasonal Factor

The model increases fares during selected peak months and applies a weekend adjustment.

* June, July, August, and December: `1.25`
* January and February: `0.90`
* Other months: `1.00`
* Saturday/Sunday: additional `1.10` multiplier

The seasonal and weekend effects are combined into one seasonal factor.

---

## 6. Fare Bounds

After applying all pricing factors, the calculated fare is bounded relative to the base fare.

```text
minimum fare = 70% of base fare
maximum fare = 180% of base fare
```

NumPy's `clip` operation ensures that the final fare stays within these bounds.

This prevents extreme factor combinations from producing unreasonable fares.

---

## 7. Pandas and NumPy

The system calculates pricing factors across many flights using vectorized Pandas and NumPy operations rather than calculating each flight through a Python loop.

For example, time-to-departure values are calculated for the flight DataFrame and `np.select()` is used to assign pricing factors based on conditions.

The resulting DataFrame contains columns such as:

```text
time_factor
demand_factor
capacity_factor
seasonal_factor
adjusted_fare
```

The system can then rank flights by adjusted fare using Pandas sorting.

---

## 8. SQLite Persistence

The project uses SQLite to persist flight information.

The `flights` table stores:

* Flight ID
* Origin
* Destination
* Departure date
* Base fare
* Capacity
* Seats sold
* Time factor
* Demand factor
* Capacity factor
* Seasonal factor
* Adjusted fare

The database layer creates the database schema and demonstrates the required data operations:

* **CREATE TABLE**: creates the `flights` table
* **INSERT**: stores generated and priced flights
* **SELECT**: retrieves all flights or a specific flight
* **UPDATE**: changes operational information such as seats sold
* **DELETE**: removes a flight

SQL parameters are used for values instead of constructing SQL statements from user input.

---

## 9. Operational Update

The application demonstrates how an operational change can affect pricing.

For example, the system selects a flight and updates its number of seats sold to the full capacity.

The capacity factor is then recalculated and the fare is recalculated using the updated capacity information.

In the example run:

```text
PD024
Seats sold: 8 → 180
Adjusted fare: $577.51 → $815.69
```

This demonstrates the relationship between remaining capacity and dynamic pricing.

---

## 10. Validation and Edge Cases

The `Flight` class validates important assumptions, including:

* Flight ID must be provided
* Origin and destination must be provided
* Base fare cannot be negative
* Capacity must be positive
* Seats sold cannot be negative
* Seats sold cannot exceed capacity
* Adjusted fare cannot be negative when provided

The application also demonstrates an invalid flight:

```text
Capacity = 100
Seats sold = 150
```

The validation correctly raises and catches a `ValueError`:

```text
Seats sold must be between 0 and capacity.
```

This provides an explicit check for an important operational edge case.

---

## 11. How to Run

### Requirements

The project requires Python 3 and the following packages:

```text
pandas
numpy
```

SQLite is included with Python through the standard `sqlite3` library.

### Set up

From the project directory, install the required packages with:

```bash
python3 -m pip install pandas numpy
```

Optional: create and use a virtual environment to keep the project dependencies isolated:

```bash
python3 -m venv myenv
source myenv/bin/activate
python3 -m pip install pandas numpy
```

### Run the application

Run the main script with:

```bash
python3 main.py
```

The program will:

1. Generate 100 fictional flights
2. Save the flight data to CSV
3. Calculate dynamic prices
4. Store the results in SQLite
5. Retrieve and display stored flights
6. Rank flights by adjusted fare
7. Update an operational value and recalculate the fare
8. Validate a normal flight
9. Demonstrate an invalid-flight edge case
10. Delete a flight and verify the deletion

---

## 12. Design Choices

The project separates data generation, pricing, analysis, persistence, and application execution into different modules.

A `Flight` class represents individual flight data and provides validation.

Pricing functions are kept separate from database operations so that pricing logic can be changed without rewriting the persistence layer.

Seats sold is treated as the operational value, while seats remaining is derived from capacity and seats sold. This avoids storing duplicate information that could become inconsistent.

A fixed random seed and reference date are used to make the generated data and pricing results reproducible.

---

## 13. Known Limitations

This is an educational dynamic-pricing prototype rather than a production airline revenue management system.

Current limitations include:

* Route demand is represented using simple predefined city scores rather than real booking or market data.
* Pricing uses rule-based factors rather than statistical or machine-learning forecasting.
* The dataset is fictional.
* The reference date is fixed for reproducibility rather than automatically using the current date.
* The application uses a simple script-based workflow rather than a web or graphical interface.

These choices keep the system explainable and within the scope of the Python programming project.

---

## 14. Optional LLM/API

No LLM or external API is required for the core system.

The fare is always determined by the programmed pricing logic. An LLM, if added in the future, could explain an existing fare decision but would not determine or override the fare.
