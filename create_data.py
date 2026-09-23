"""
File for creating flight data for potter airlines project
"""

import pandas as pd
import numpy as np
import random
import sqlite3
# from datetime import date, timedelta


random.seed(8) # Set seed for reproducibility, choose 8 because we are team 8
np.random.seed(8)

from flight import Flight

number_of_flights = 100
# reference_date = date(2026, 9, 13)

cities =[
    "Toronto",
    "Vancouver",
    "Montreal",
    "Halifax",
    "Calgary",
    "Ottawa",
    "London",
    "Hogsmeade",
    "Diagon Alley",
]

capacities = [80, 100, 120, 150, 180]

flights = []

for i in range(number_of_flights):
    origin, destination = random.sample(cities, 2)

    days_until_departure = random.randint(1, 90)  # Randomly choose a departure date within the next 90 days
    departure_date = pd.Timestamp.now() + pd.Timedelta(days=days_until_departure)

    capacity = random.choice(capacities)
    seats_sold = random.randint(0, capacity) # Would it be better to do seats_remaining?

    flight = Flight(
        flight_id=f"PD{i+1:03d}",
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        base_fare=random.uniform(100, 500),  # Random base fare between $100 and $500
        capacity=capacity,
        seats_sold=seats_sold,
        time_factor=1,  # Random time factor between 0.8 and 1.2
        demand_factor=1,  # Random demand factor between 0.8 and 1.2
        capacity_factor=1,  # Random capacity factor between 0.8 and 1.2
        seasonal_factor=1,  # Random seasonal factor between 0.8 and 1.2
        adjusted_fare=1  # Random adjusted fare between $100 and $500
    )

    # Validate the flight data
    flight.validate_flight()
    flights.append(flight)

# Convert Flight objects into a DataFrame
flight_data = [
flight.to_dictionary()
    for flight in flights]

# CSV output to check the generated data
flights_df = pd.DataFrame(flight_data)
flights_df.to_csv("potter_flights_generated.csv", index=False)

# Create the SQLite database
with sqlite3.connect("potter_airlines.db") as connection:
    flights_df.to_sql(
        "flights",
        connection,
        if_exists="replace",
        index=False,
    )

    count = connection.execute(
        "SELECT COUNT(*) FROM flights"
    ).fetchone()[0]

print(f"Created potter_airlines.db with {count} flights.")
print(flights_df.head())