"""
The main entry point. 
This is the file to run to demonstrate the complete workflow from beginning to end.
"""

def main():
    """Main function to run the complete workflow."""
    from database import create_table, insert_flight

    # Create the flights table if it does not already exist
    create_table()

if __name__ == "__main__":
    main()