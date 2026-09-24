"""
Handles operations across many flights using Pandas/NumPy, such as calculating prices,
filtering flights, sorting them, or ranking them (e.g. any vectorized operation).
"""

import pandas as pd

from constants import CSV_PATH, REFERENCE_DATE
from pricing import (
    calculate_fare,
    capacity_factor,
    demand_factor,
    seasonal_factor,
    time_factor,
)


def price_flights(csv_path=CSV_PATH, current_date=REFERENCE_DATE):
    """Load the raw flight CSV and add the pricing columns for every flight."""
    flights = pd.read_csv(csv_path)
    flights["time_factor"] = time_factor(flights["departure_date"], current_date)
    flights["demand_factor"] = demand_factor(flights["origin"], flights["destination"])
    flights["capacity_factor"] = capacity_factor(flights["seats_sold"], flights["capacity"])
    flights["seasonal_factor"] = seasonal_factor(flights["departure_date"])
    flights["adjusted_fare"] = calculate_fare(
        flights["base_fare"],
        flights["time_factor"],
        flights["demand_factor"],
        flights["capacity_factor"],
        flights["seasonal_factor"],
    )
    return flights


def rank_flights(flights_df, by="adjusted_fare", n=10):
    """Return the top n flights by a column."""
    return flights_df.sort_values(by, ascending=False).head(n)
