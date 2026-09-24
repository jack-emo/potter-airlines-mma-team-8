"""
File for creating flight data for potter airlines project
"""

import pandas as pd
import random
from flight import Flight
from constants import CITIES, CSV_PATH, FLIGHT_INPUT_COLUMNS, REFERENCE_DATE, SEED


def generate_flight_data(number_of_flights=100):
    """Build raw Flight objects. Pricing factors are calculated later."""
    random.seed(SEED)

    capacities = [80, 100, 120, 150, 180]
    flights = []

    for i in range(number_of_flights):
        origin, destination = random.sample(CITIES, 2)
        days_until_departure = random.randint(1, 90)
        departure_date = pd.Timestamp(REFERENCE_DATE) + pd.Timedelta(days=days_until_departure)
        capacity = random.choice(capacities)
        seats_sold = random.randint(0, capacity)

        flight = Flight(
            flight_id=f"PD{i+1:03d}",
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            base_fare=round(random.uniform(100, 500), 2),
            capacity=capacity,
            seats_sold=seats_sold,
        )

        flight.validate_flight()
        flights.append(flight)

    return flights


def save_flights_csv(flights, csv_path=CSV_PATH):
    """Write raw flight inputs to CSV for later pricing and database insert."""
    flight_data = []
    for flight in flights:
        row = {column: getattr(flight, column) for column in FLIGHT_INPUT_COLUMNS}
        row["departure_date"] = flight.departure_date.strftime("%Y-%m-%d")
        flight_data.append(row)

    flights_df = pd.DataFrame(flight_data, columns=FLIGHT_INPUT_COLUMNS)
    flights_df.to_csv(csv_path, index=False)
    return flights_df
