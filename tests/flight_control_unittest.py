import json
import os
import unittest
from unittest.mock import patch, mock_open, call
import sys

# Adjust sys.path to include the parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from src.recordmanager.record_manager import RecordManager  # Import from parent directory
except ModuleNotFoundError as e:
    raise ImportError(f"Unable to import 'record_manager': {e}. Ensure 'record_manager.py' exists in the parent directory and is correctly named.")

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the JSON file
FILE_NAME = os.path.join(current_dir, '..', 'src', 'json_db', 'records.json')


class flight_Control_unittest(unittest.TestCase):
    """Unit tests for the RecordManager class."""

    def setUp(self):
        """Sets up a clean RecordManager instance for each test."""
        self.record_manager = RecordManager()
        self.record_manager.records = {
            "Clients": [],
            "Flights": [],
            "Airline Companies": [],
        }

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data='{"Clients": [], "Flights": [], "Airline Companies": []}')
    def test_load_records_file_exists(self, mock_file, mock_exists):
        """Tests loading records when the file exists."""
        mock_exists.return_value = True
        records = self.record_manager.load_records()
        self.assertEqual(records, {"Clients": [], "Flights": [], "Airline Companies": []})

    @patch("os.path.exists")
    def test_load_records_file_not_exists(self, mock_exists):
        """Tests loading records when the file does not exist."""
        mock_exists.return_value = False
        records = self.record_manager.load_records()
        self.assertEqual(records, {"Clients": [], "Flights": [], "Airline Companies": []})

    @patch("builtins.open", new_callable=mock_open)
    def test_save_records(self, mock_file):
        """Tests if records are saved correctly to the file."""
        self.record_manager.records = {
            "Clients": [{"ID": 1001, "name": "Test Client"}],
            "Flights": [],
            "Airline Companies": [],
        }
        self.record_manager.save_records(self.record_manager.records)

        # Verify the content written to the file
        expected_content = json.dumps(self.record_manager.records, indent=4)
        written_content = ''.join(call.args[0] for call in mock_file().write.call_args_list)
        self.assertEqual(written_content, expected_content)
        
    def test_generate_id_empty_category(self):
        """Tests generating an ID for an empty category."""
        client_id = self.record_manager.generate_id("Clients")
        self.assertEqual(client_id, 1001)

    def test_generate_id_existing_records(self):
        """Tests generating an ID when records already exist."""
        self.record_manager.records["Clients"].append({"ID": 1005})
        client_id = self.record_manager.generate_id("Clients")
        self.assertEqual(client_id, 1006)

    def test_create_record(self):
        """Tests creating a new record."""
        record = self.record_manager.create_record("Clients", name="Alice")
        self.assertEqual(record["ID"], 1001)
        self.assertEqual(record["name"], "Alice")
        self.assertIn(record, self.record_manager.records["Clients"])

    def test_delete_record(self):
        """Tests deleting an existing record."""
        self.record_manager.records["Clients"].append({"ID": 1001, "name": "Alice"})
        result = self.record_manager.delete_record("Clients", 1001)
        self.assertTrue(result)
        self.assertEqual(self.record_manager.records["Clients"], [])

    def test_update_record(self):
        """Tests updating an existing record."""
        self.record_manager.records["Clients"].append({"ID": 1001, "name": "Alice"})
        updated_record = self.record_manager.update_record("Clients", 1001, name="Bob")
        self.assertEqual(updated_record["name"], "Bob")
        self.assertEqual(self.record_manager.records["Clients"][0]["name"], "Bob")

    def test_search_records(self):
        """Tests searching records for a keyword."""
        self.record_manager.records["Clients"].extend(
            [{"ID": 1001, "name": "Alice"}, {"ID": 1002, "name": "Bob"}]
        )
        results = self.record_manager.search_records("Clients", "alice")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Alice")

if __name__ == "__main__":
    unittest.main()