import tkinter as tk
from recordmanager.record_manager import RecordManager

class AddRecordPopup(tk.Toplevel):
    """
    A pop-up window for adding a new record.
    """

    def __init__(self, parent, record_type, record_manager, update_callback):
        """
        Initializes the AddRecordPopup window.

        Args:
            parent (tk.Widget): The parent widget.
            record_type (str): The type of record to add (e.g., Clients, Flights, Airline Companies).
            record_manager (RecordManager): The record manager instance.
            update_callback (function): The callback function to update the UI after adding a record.
        """
        super().__init__(parent)
        self.title(f"Add {record_type}")
        self.geometry("400x300")
        self.configure(bg="#D3D3D3")
        self.record_type = record_type
        self.record_manager = record_manager
        self.update_callback = update_callback

        self.entries = {}

        # Define fields for each record type
        fields = {
            "Clients": ["name", "email", "phone"],
            "Flights": ["flight_number", "arrival_time", "departure_city", "arrival_city"],
            "Airline Companies": ["name", "headquarters"]
        }

        # Create entry fields for each attribute
        for idx, field in enumerate(fields[record_type]):
            label = tk.Label(self, text=field, bg="#D3D3D3", font=("Arial", 12))
            label.pack(pady=5)
            entry = tk.Entry(self, width=30)
            entry.pack()
            self.entries[field] = entry

        # Submit button to add the record
        submit_button = tk.Button(self, text="Submit", bg="#90EE90", command=self.submit)
        submit_button.pack(pady=20)

    def submit(self):
        """
        Collects data from entry fields and creates a new record.
        """
        new_record_data = {field: entry.get() for field, entry in self.entries.items()}
        new_record = self.record_manager.create_record(self.record_type, **new_record_data)
        self.update_callback(new_record)
        self.destroy()

class DeleteConfirmationPopup(tk.Toplevel):
    """
    A pop-up window to confirm the deletion of records.
    """

    def __init__(self, parent, record_type, selected_ids, delete_callback):
        """
        Initializes the DeleteConfirmationPopup window.

        Args:
            parent (tk.Widget): The parent widget.
            record_type (str): The type of records to delete.
            selected_ids (list): The IDs of the records to delete.
            delete_callback (function): The callback function to delete the records.
        """
        super().__init__(parent)
        self.title(f"Confirm Deletion")
        self.geometry("400x200")
        self.configure(bg="#B22222")

        # Confirmation message
        label = tk.Label(
            self,
            text=f"Are you sure you want to delete these {record_type} records?",
            bg="#B22222",
            fg="white",
            font=("Arial", 14, "bold")
        )
        label.pack(side='top',fill="both", expand=False, pady=20)

        # Yes button to confirm deletion
        btn_yes = tk.Button(
            self,
            text="Yes",
            bg="#90EE90",
            command=lambda: [delete_callback(selected_ids), self.destroy()]
        )
        btn_yes.pack(side="left", padx=20, pady=20)

        # No button to cancel deletion
        btn_no = tk.Button(self, text="No", bg="#D8BFD8", command=self.destroy)
        btn_no.pack(side="right", padx=20, pady=20)

class EditRecordPopup(tk.Toplevel):
    """
    A pop-up window for editing an existing record.
    """

    def __init__(self, parent, record_type, record_manager, record_id, update_callback):
        """
        Initializes the EditRecordPopup window.

        Args:
            parent (tk.Widget): The parent widget.
            record_type (str): The type of record to edit (e.g., Clients, Flights, Airline Companies).
            record_manager (RecordManager): The record manager instance.
            record_id (int): The ID of the record to edit.
            update_callback (function): The callback function to update the UI after editing a record.
        """
        super().__init__(parent)
        self.title(f"Edit {record_type}")
        self.geometry("400x300")
        self.configure(bg="#D3D3D3")
        self.record_type = record_type
        self.record_manager = record_manager
        self.record_id = record_id
        self.update_callback = update_callback

        self.entries = {}

        # Get the record to edit
        record = next((rec for rec in self.record_manager.records[record_type] if rec["ID"] == record_id), None)

        # Define fields for each record type
        fields = {
            "Clients": ["name", "email", "phone"],
            "Flights": ["flight_number", "arrival_time", "departure_city", "arrival_city"],
            "Airline Companies": ["name", "headquarters"]
        }

        # Create entry fields for each attribute with pre-populated data
        for idx, field in enumerate(fields[record_type]):
            label = tk.Label(self, text=field, bg="#D3D3D3", font=("Arial", 12))
            label.pack(pady=5)
            entry = tk.Entry(self, width=30)
            entry.insert(0, record.get(field, ""))
            entry.pack()
            self.entries[field] = entry

        # Submit button to update the record
        submit_button = tk.Button(self, text="Submit", bg="#90EE90", command=self.submit)
        submit_button.pack(pady=20)

    def submit(self):
        """
        Collects data from entry fields and updates the record.
        """
        updated_data = {field: entry.get() for field, entry in self.entries.items()}
        updated_record = self.record_manager.update_record(self.record_type, self.record_id, **updated_data)
        self.update_callback(updated_record)
        self.destroy()