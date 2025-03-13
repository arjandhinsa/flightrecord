import json
import os

FILE_NAME = "records.json"

class RecordManager:
    def __init__(self):
        self.records = self.load_records()

    def load_records(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        return {"Clients": [], "Flights": [], "Airline Companies": []}

    def save_records(self):
        with open(FILE_NAME, "w") as file:
            json.dump(self.records, file, indent=4)

    def generate_id(self, category):
        prefix = {"Clients": 1000, "Flights": 2000, "Airline Companies": 3000}
        if self.records[category]:
            return max(rec["ID"] for rec in self.records[category]) + 1
        return prefix[category] + 1

    def create_record(self, category, **kwargs):
        record = {"ID": self.generate_id(category), **kwargs}
        self.records[category].append(record)
        self.save_records()
        return record  # Returning record for UI integration

    def delete_record(self, category, record_id):
        self.records[category] = [rec for rec in self.records[category] if rec["ID"] != record_id]
        self.save_records()
        return True  # Returning status for UI integration

    def update_record(self, category, record_id, **kwargs):
        for record in self.records[category]:
            if record["ID"] == record_id:
                record.update({k: v for k, v in kwargs.items() if v is not None})
                self.save_records()
                return record  # Returning updated record for UI integration
        return None

    def search_records(self, category, keyword):
        results = [rec for rec in self.records[category] if keyword.lower() in json.dumps(rec).lower()]
        return results  # Returning list for UI integration

# Initialize record manager
record_manager = RecordManager()
