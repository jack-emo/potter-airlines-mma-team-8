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
    return base_fare * time_factor * demand_factor * capacity_factor * seasonal_factor