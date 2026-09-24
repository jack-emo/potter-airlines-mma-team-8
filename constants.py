"""Shared paths, dates, and pricing settings."""

CSV_PATH = "potter_flights_generated.csv"
DB_PATH = "potter_airlines.db"
REFERENCE_DATE = "2026-09-13"
SEED = 8

FLIGHT_INPUT_COLUMNS = [
    "flight_id",
    "origin",
    "destination",
    "departure_date",
    "base_fare",
    "capacity",
    "seats_sold",
]

# Higher scores are busier routes. The demand factor is the average of the two cities.
CITY_DEMAND = {
    "Toronto": 1.20,
    "Vancouver": 1.15,
    "Montreal": 1.10,
    "Calgary": 1.05,
    "Ottawa": 1.00,
    "Halifax": 0.95,
    "London": 0.90,
    "Hogsmeade": 1.30,
    "Diagon Alley": 1.25,
}

CITIES = list(CITY_DEMAND)
