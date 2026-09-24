"""
The main entry point.
This is the file to run to demonstrate the complete workflow from beginning to end.
"""

def main():
    """Main function to run the complete workflow."""
    from analysis import price_flights, rank_flights
    from create_data import generate_flight_data, save_flights_csv
    from database import (
        create_table,
        delete_flight,
        get_all_flights,
        get_flight,
        insert_flight,
        insert_flights,
        update_seats_sold,
    )
    from flight import Flight
    from pricing import calculate_fare, capacity_factor

    # 1. Create the flights table if it does not already exist
    create_table()

    # 2. Create flight data and store it in csv
    flights = generate_flight_data()
    save_flights_csv(flights)

    # 3. Load flight data from csv and calculate factor rules
    priced_flights = price_flights()

    # 4. Insert rows into sqlite using parameterized queries
    insert_flights(priced_flights)
    print(priced_flights.head())

    # 5. Retrieve the stored flights (SELECT) and print them
    stored_flights = get_all_flights()
    print(f"\nRetrieved {len(stored_flights)} flights.")
    print(get_flight(stored_flights["flight_id"].iloc[0]))

    # 6. Filter or rank the priced flights and print a short result
    print("\nHighest adjusted fares:")
    print(rank_flights(stored_flights, n=5)[["flight_id", "origin", "destination", "base_fare", "adjusted_fare"]])

    # 7a. Update an operational value, then show the fare change
    seats_remaining = stored_flights["capacity"] - stored_flights["seats_sold"]
    sample = stored_flights.loc[[seats_remaining.idxmax()]].copy()
    flight_id = sample["flight_id"].iloc[0]
    old_seats = int(sample["seats_sold"].iloc[0])
    new_seats = int(sample["capacity"].iloc[0])
    old_fare = float(sample["adjusted_fare"].iloc[0])

    update_seats_sold(flight_id, new_seats)
    sample["seats_sold"] = new_seats
    sample["capacity_factor"] = capacity_factor(sample["seats_sold"], sample["capacity"])
    sample["adjusted_fare"] = calculate_fare(
        sample["base_fare"],
        sample["time_factor"],
        sample["demand_factor"],
        sample["capacity_factor"],
        sample["seasonal_factor"],
    )
    insert_flight(next(sample.itertuples(index=False)))
    new_fare = float(sample["adjusted_fare"].iloc[0])
    print(f"\nUpdated {flight_id}: seats_sold {old_seats} updated to {new_seats}")
    print(f"adjusted_fare {old_fare:.2f} updated to {new_fare:.2f}")

    # 7b. Run validation on a normal flight, then demonstrate one bad case
    normal_flight = flights[0]
    normal_flight.validate_flight()
    print(f"\n{normal_flight.flight_id} passed validation.")

    bad_flight = Flight(
        flight_id="PD999",
        origin="Toronto",
        destination="Ottawa",
        departure_date="2026-10-01",
        base_fare=200,
        capacity=100,
        seats_sold=150,
    )
    try:
        bad_flight.validate_flight()
    except ValueError as error:
        print(f"Caught invalid flight {bad_flight.flight_id}: {error}")

    # 7c. Delete one flight
    deleted_id = "PD100" if flight_id != "PD100" else "PD099"
    delete_flight(deleted_id)
    print(f"\nDeleted {deleted_id}. Lookup now returns {get_flight(deleted_id)}.")
    print(f"{len(get_all_flights())} flights remain.")



if __name__ == "__main__":
    main()
