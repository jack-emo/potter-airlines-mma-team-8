"""
Defines the Flight class and flight-related validation.
"""

class Flight:
    """
    Represents a flight with its detailed data.
    """
    def __init__(self, flight_id, origin, destination, departure_date, base_fare, capacity, seats_sold, time_factor, demand_factor, capacity_factor, seasonal_factor, adjusted_fare):
        self.flight_id = flight_id
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        self.base_fare = base_fare
        self.capacity = capacity
        self.seats_sold = seats_sold
        self.time_factor = time_factor
        self.demand_factor = demand_factor
        self.capacity_factor = capacity_factor
        self.seasonal_factor = seasonal_factor
        self.adjusted_fare = adjusted_fare

    def validate_flight(self):
        """
        Validates the flight details.
        """
        # Check for valid flight ID, origin, destination, and dates
        if not self.flight_id or not isinstance(self.flight_id, str):
            raise ValueError("Invalid flight ID.")

        # Check for valid origin and destination
        if not self.origin or not isinstance(self.origin, str):
            raise ValueError("Invalid origin.")
        if not self.destination or not isinstance(self.destination, str):
            raise ValueError("Invalid destination.")

        # Check for valid fare, capacity, and seats sold
        if self.base_fare < 0:
            raise ValueError("Base fare cannot be negative.")
        if self.capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        if self.seats_sold < 0 or self.seats_sold > self.capacity:
            raise ValueError("Seats sold must be between 0 and capacity.")
        if self.adjusted_fare < 0:
            raise ValueError("Adjusted fare cannot be negative.")

    
    def to_dictionary(self):
        """
        Converts the Flight object into a dictionary.
        """

        return {
            "flight_id": self.flight_id,
            "origin": self.origin,
            "destination": self.destination,
            "departure_date": self.departure_date.strftime("%Y-%m-%d"),
            "base_fare": round(self.base_fare, 2),
            "capacity": self.capacity,
            "seats_sold": self.seats_sold,
            #"seats_remaining": self.capacity - self.seats_sold,
        }