"""
Contains the actual pricing rules: time factor, demand factor, capacity factor, 
seasonal factor, minimum/maximum fare limits (maybe), and final price calculation.
"""

# TODO: Implement factor calculations, can adjust the parameters as needed
def time_factor(departure_date, current_date):
    pass

def demand_factor(seats_sold, capacity):
    pass

def capacity_factor(seats_sold, capacity):
    pass

def seasonal_factor(departure_date):
    pass

def calculate_fare(base_fare, time_factor, demand_factor, capacity_factor, seasonal_factor):
    raw_fare = base_fare * time_factor * demand_factor * capacity_factor * seasonal_factor
    # Keep the final fare between 70% and 180% of the base fare
    min_fare = base_fare * 0.7
    max_fare = base_fare * 1.8
    adjusted_fare = max(min_fare, min(raw_fare, max_fare))

    return adjusted_fare