import json
import os
import time
import psutil
import random
import sys
import cProfile
import pstats

# Adjust sys.path to include the parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from src.recordmanager.record_manager import RecordManager  # Import from parent directory
except ModuleNotFoundError as e:
    raise ImportError(f"Unable to import 'record_manager': {e}. Ensure 'record_manager.py' exists in the parent directory and is correctly named.")

FILE_NAME = "records_perf_test.json"
"""Name of the JSON file used for storing records."""


class RecordManager:
    """Manages records stored in a JSON file."""

    def __init__(self):
        """Initializes the RecordManager and loads records."""
        self.records = self.load_records()

    def load_records(self):
        """Loads records from the JSON file or returns default if file doesn't exist."""
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                return json.load(file)
        return {"Clients": [], "Flights": [], "Airline Companies": []}

    def save_records(self):
        """Saves records to the JSON file."""
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(self.records, file, indent=4)

    def generate_id(self, category):
        """Generates a unique ID for a new record in the specified category."""
        prefix = {"Clients": 1000, "Flights": 2000, "Airline Companies": 3000}
        if self.records[category]:
            return max(rec["ID"] for rec in self.records[category]) + 1
        return prefix[category] + 1

    def create_record(self, category, **kwargs):
        """Creates a new record in the specified category and saves it."""
        record = {"ID": self.generate_id(category), **kwargs}
        self.records[category].append(record)
        self.save_records()
        return record

    def delete_record(self, category, record_id):
        """Deletes a record from the specified category and saves changes."""
        self.records[category] = [
            rec for rec in self.records[category] if rec["ID"] != record_id
        ]
        self.save_records()
        return True

    def update_record(self, category, record_id, **kwargs):
        """Updates a record in the specified category and saves changes."""
        for record in self.records[category]:
            if record["ID"] == record_id:
                record.update({k: v for k, v in kwargs.items() if v is not None})
                self.save_records()
                return record
        return None

    def search_records(self, category, keyword):
        """Searches records in the specified category for a keyword."""
        results = [
            rec
            for rec in self.records[category]
            if keyword.lower() in json.dumps(rec).lower()
        ]
        return results


def run_performance_test(iterations=10000):
    """Runs a performance test by updating records multiple times."""

    record_manager = RecordManager()

    # Create initial records
    for i in range(100):
        record_manager.create_record("Clients", name=f"Client {i}")

    # Get initial resource usage
    initial_cpu = psutil.cpu_percent(interval=None)
    initial_memory = psutil.virtual_memory().percent
    initial_disk_io = psutil.disk_io_counters()

    start_time = time.time()

    for _ in range(iterations):
        # Update a random record
        client_records = record_manager.records["Clients"]
        if client_records:
            random_record = random.choice(client_records)
            record_manager.update_record("Clients", random_record["ID"], name="Updated Name")

    end_time = time.time()

    # Get final resource usage
    final_cpu = psutil.cpu_percent(interval=None)
    final_memory = psutil.virtual_memory().percent
    final_disk_io = psutil.disk_io_counters()

    # Calculate differences
    cpu_usage = final_cpu - initial_cpu
    memory_usage = final_memory - initial_memory
    disk_read_diff = final_disk_io.read_bytes - initial_disk_io.read_bytes
    disk_write_diff = final_disk_io.write_bytes - initial_disk_io.write_bytes

    elapsed_time = end_time - start_time

    # Print results
    print(f"Performance Test Results ({iterations} iterations):")
    print(f"  Elapsed Time: {elapsed_time:.2f} seconds")
    print(f"  CPU Usage: {cpu_usage:.2f}%")
    print(f"  Memory Usage: {memory_usage:.2f}%")
    print(f"  Disk Read: {disk_read_diff / (1024 * 1024):.2f} MB")
    print(f"  Disk Write: {disk_write_diff / (1024 * 1024):.2f} MB")
    print(f"  Average time per update: {(elapsed_time/iterations)*1000} milliseconds")


if __name__ == "__main__":
    profile = cProfile.Profile()
    profile.run('run_performance_test()')
    profile.dump_stats('profile.prof') #save profile data to file
    stats = pstats.Stats(profile)
    stats.sort_stats('cumulative').print_stats(20)  # Print top 20 functions
    run_performance_test() # run the test again to get the resource usage.