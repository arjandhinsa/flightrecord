import json
import os

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the JSON file
FILE_NAME = os.path.join(current_dir, '..', 'json_db', 'records.json')

class RecordManager:
    """
    A class to manage records stored in a JSON file.
    """

    def __init__(self):
        """
        Initializes the RecordManager and loads records from the JSON file.
        """
        self.records = self.load_records()

    def load_records(self):
        """
        Loads records from the JSON file if it exists, otherwise returns default records.

        Returns:
            dict: A dictionary containing records for Clients, Flights, and Airline Companies.
        """
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        return {"Clients": [], "Flights": [], "Airline Companies": []}

    def save_records(self, records):
        """
        Saves the current records to the JSON file.

        Args:
            records (dict): The records to be saved.
        """
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            # Updated encoding to utf-8, as it is the default encoding for JSON files.
            json.dump(records, file, indent=4)

    def generate_id(self, category):
        """
        Generates a unique ID for a new record in the specified category.

        Args:
            category (str): The category for which to generate an ID.

        Returns:
            int: A unique ID for the new record.
        """
        prefix = {"Clients": 1000, "Flights": 2000, "Airline Companies": 3000}
        if self.records[category]:
            # Convert IDs to integers for comparison
            return max(int(rec["ID"]) for rec in self.records[category]) + 1
        return prefix[category] + 1

    def create_record(self, category, **kwargs):
        """
        Creates a new record in the specified category and saves it.

        Args:
            category (str): The category in which to create the record.
            **kwargs: Additional attributes for the record.

        Returns:
            dict: The newly created record.
        """
        record = {"ID": self.generate_id(category), **kwargs}
        self.records[category].append(record)
        self.save_records(self.records)  # Pass the current records to save
        return record

    def delete_record(self, category, record_id):
        """
        Deletes a record from the specified category and saves changes.

        Args:
            category (str): The category from which to delete the record.
            record_id (int): The ID of the record to delete.

        Returns:
            bool: True if the record was deleted, False otherwise.
        """
        self.records[category] = [rec for rec in self.records[category] if rec["ID"] != record_id]
        self.save_records(self.records)  # Pass the current records to save
        return True

    def update_record(self, category, record_id, **kwargs):
        """
        Updates a record in the specified category and saves changes.

        Args:
            category (str): The category of the record to update.
            record_id (int): The ID of the record to update.
            **kwargs: Updated attributes for the record.

        Returns:
            dict or None: The updated record, or None if the record was not found.
        """
        for record in self.records[category]:
            if record["ID"] == record_id:
                record.update({k: v for k, v in kwargs.items() if v is not None})
                self.save_records(self.records)  # Pass the current records to save
                return record
        return None

    def search_records(self, category, keyword):
        """
        Searches records in the specified category for a keyword.

        Args:
            category (str): The category to search within.
            keyword (str): The keyword to search for.

        Returns:
            list: A list of records that match the keyword.
        """
        results = [rec for rec in self.records[category] if keyword.lower() in json.dumps(rec).lower()]
        return results  # Returning list for UI integration

# Initialize record manager
record_manager = RecordManager()