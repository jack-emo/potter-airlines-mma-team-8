"""
The main entry point. 
This is the file to run to demonstrate the complete workflow from beginning to end.
"""

def main():
    """Main function to run the complete workflow."""
    from database import create_table, insert_flight

    # TODO: 1. Create the flights table if it does not already exist
    create_table()

    # TODO: 2. Create flight data and store it in csv

    # TODO: 3. Load flight data from csv and calculate factor rules

    # TODO: 4. Insert Rows into sqlite database using parameterized queries

    # TODO: 5. Retrieve the stored flights (SELECT) and print them

    # TODO: 6. Filter or rank the priced flights and print a short result
    
    ### TESTING
    
    # TODO: 7a. Update an operational value, then show the fare change
    
    # TODO: 7b. Run validation on a normal flight, then demonstrate one bad case

    # TODO: 7c. Delete one flight



if __name__ == "__main__":
    main()