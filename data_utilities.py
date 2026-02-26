"""Utility functions for loading and persisting data."""

from pandas import DataFrame, read_excel
import shelve

def load_excel(filepath: str) -> DataFrame | None:
    """Load an Excel file into a DataFrame.

    Args:
        filepath: Path to the Excel file.

    Returns:
        The loaded DataFrame on success, otherwise ``None``.
    """
    try:
        df = read_excel(filepath)                       # Load the Excel file into a DataFrame
        return df
    except Exception as e:                              # Catch any issues and show an error message
        print(f"Error loading Excel file: {e}")
        return None
    
def shelve_data(data: dict, filename: str) -> None:
    """Save key-value pairs to a shelve file.

    Args:
        data: Dictionary to persist.
        filename: Shelve filename (without extension handling).

    Returns:
        ``None``.
    """
    try:
        with shelve.open(filename) as db:               # Open/create the desired shelve file, creating the `db` variable to edit the saved dictionary
            for id, value in data.items():              # Iterate through the data dictionary...
                db[id] = value                          # ...and save each key-value pair to the shelved dictionary
        print(f"Data successfully saved to {filename}")
    except Exception as e:                              # Catch any issues and show an error message
        print(f"Error saving data to shelve: {e}")

def load_shelve(filename: str) -> dict | None:
    """Load all key-value pairs from a shelve file.

    Args:
        filename: Shelve filename to read.

    Returns:
        A dictionary containing shelved data on success, otherwise ``None``.
    """
    try:
        with shelve.open(filename) as db:           # Open the shelve file and create the `db` variable to access the saved dictionary
            data = {i: db[i] for i in db.keys()}    # Create a new dictionary by iterating through the shelved key-value pairs (copies the shelved data, rather than referencing it)
        return data
    except Exception as e:                          # Catch any issues and show an error message
        print(f"Error loading data from shelve: {e}")
        return None

def next_id(data: dict) -> int:
    """
    Return the next available ID for a new entry in a dictionary.

    Args:
        data: Dictionary representing existing data.

    Returns:
        The next available integer ID.
    """
    if len(data.keys()) == 0:       # If the dictionary is empty, start IDs at 0
        return 0

    return max(data.keys()) + 1     # Otherwise, increase the maximum existing key by 1 to get a unique new ID