"""
Contains Python functions that interact with SQLite: connecting to the database
and doing INSERT, SELECT, UPDATE, and DELETE operations using parameters.
"""
import sqlite3

import pandas as pd

from constants import DB_PATH

# Initialize database connection
def create_connection():
    """Create a database connection to the SQLite database specified by db_file."""
    return sqlite3.connect(DB_PATH)

# Create the flights table if it does not already exist
def create_table():
    """Create the flights table if it does not already exist."""
    with create_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS flights (
                flight_id TEXT PRIMARY KEY,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                departure_date TEXT NOT NULL,
                base_fare REAL NOT NULL,
                capacity INTEGER NOT NULL,
                seats_sold INTEGER NOT NULL,
                time_factor REAL NOT NULL,
                demand_factor REAL NOT NULL,
                capacity_factor REAL NOT NULL,
                seasonal_factor REAL NOT NULL,
                adjusted_fare REAL NOT NULL
            )
        """)

def insert_flight(flight):
    """Insert one flight into the database."""
    with create_connection() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO flights (
                flight_id,
                origin,
                destination,
                departure_date,
                base_fare,
                capacity,
                seats_sold,
                time_factor,
                demand_factor,
                capacity_factor,
                seasonal_factor,
                adjusted_fare
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                flight.flight_id,
                flight.origin,
                flight.destination,
                flight.departure_date,
                flight.base_fare,
                flight.capacity,
                flight.seats_sold,
                flight.time_factor,
                flight.demand_factor,
                flight.capacity_factor,
                flight.seasonal_factor,
                flight.adjusted_fare,
            ),
        )


def insert_flights(flights_df):
    """Insert each priced flight with insert_flight."""
    for flight in flights_df.itertuples(index=False):
        insert_flight(flight)

def get_all_flights():
    """Retrieve all flights."""
    with create_connection() as conn:
        cursor = conn.execute("SELECT * FROM flights")
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
    return pd.DataFrame(rows, columns=columns)

def get_flight(flight_id):
    """Retrieve one flight by ID."""
    with create_connection() as conn:
        cursor = conn.execute(
            "SELECT * FROM flights WHERE flight_id = ?",
            (flight_id,),
        )
        return cursor.fetchone()

def update_seats_sold(flight_id, seats_sold):
    """Update an operational value for a flight."""
    with create_connection() as conn:
        conn.execute(
            """
            UPDATE flights
            SET seats_sold = ?
            WHERE flight_id = ?
            """,
            (seats_sold, flight_id),
        )

def delete_flight(flight_id):
    """Delete a flight from the database."""
    with create_connection() as conn:
        conn.execute(
            "DELETE FROM flights WHERE flight_id = ?",
            (flight_id,),
        )
