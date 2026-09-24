"""
Contains the actual pricing rules: time factor, demand factor, capacity factor,
seasonal factor, minimum/maximum fare limits, and final price calculation.
"""

import numpy as np
import pandas as pd

from constants import CITY_DEMAND, REFERENCE_DATE


def time_factor(departure_date, current_date=REFERENCE_DATE):
    """
    Fares rise as departure gets closer.
    - 7 days or less: 1.40x
    - 8-21 days: 1.20x
    - 22-45 days: 1.00x
    - 46+ days: 0.85x
    """
    days = (pd.to_datetime(departure_date) - pd.to_datetime(current_date)).dt.days
    return np.select(
        [days <= 7, days <= 21, days <= 45],
        [1.40, 1.20, 1.00],
        default=0.85,
    )


def demand_factor(origin, destination):
    """
    Busier cities produce a higher route multiplier.
    The demand factor is the average of the two cities' demand scores.
    """
    origin_demand = origin.map(CITY_DEMAND)
    destination_demand = destination.map(CITY_DEMAND)
    return ((origin_demand + destination_demand) / 2).round(2)


def capacity_factor(seats_sold, capacity):
    """
    Flights that have fewer seats remaining cost more.
    The ratio is seats still open divided by capacity.
    If the ratio is 0.15 or less, the factor is 1.50x.
    If the ratio is 0.16 to 0.40, the factor is 1.25x.
    If the ratio is 0.41 to 0.70, the factor is 1.00x.
    If the ratio is 0.71 or more, the factor is 0.90x.
    """
    seats_remaining_ratio = (capacity - seats_sold) / capacity
    return np.select(
        [seats_remaining_ratio <= 0.15, seats_remaining_ratio <= 0.40, seats_remaining_ratio <= 0.70],
        [1.50, 1.25, 1.00],
        default=0.90,
    )


def seasonal_factor(departure_date):
    """
    December and summer cost more, January and February cost less, and weekends cost more.
    Summer months and december = 1.25x
    January and February = 0.90x
    Weekends = 1.10x
    All other months = 1.00x
    The seasonal factor is the product of the month factor and the weekend factor.
    """
    dates = pd.to_datetime(departure_date)
    season = np.select(
        [dates.dt.month.isin([6, 7, 8, 12]), dates.dt.month.isin([1, 2])],
        [1.25, 0.90],
        default=1.00,
    )
    weekend = np.where(dates.dt.dayofweek >= 5, 1.10, 1.00)
    return np.round(season * weekend, 2)


def calculate_fare(base_fare, time_factor, demand_factor, capacity_factor, seasonal_factor):
    """
    Calculate the adjusted fare based on the base fare and all the factors.
    The adjusted fare stays between 70% and 180% of the base fare.
    """
    raw_fare = base_fare * time_factor * demand_factor * capacity_factor * seasonal_factor
    min_fare = base_fare * 0.7
    max_fare = base_fare * 1.8
    return np.round(np.clip(raw_fare, min_fare, max_fare), 2)
