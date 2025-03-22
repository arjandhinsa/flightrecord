import tkinter as tk
from tkinter import ttk
from .popup_windows import AddRecordPopup, DeleteConfirmationPopup

class TableWindow(tk.Toplevel):
    """
    A generic table window class for displaying and managing records.
    """

    def __init__(self, parent, title, bg_color, record_type, record_manager):
        """
        Initializes the TableWindow.

        Args:
            parent (tk.Widget): The parent widget.
            title (str): The title of the window.
            bg_color (str): The background color of the window.
            record_type (str): The type of records to manage.
            record_manager (RecordManager): The record manager instance.
        """
        super().__init__(parent)
        self.title(title)
        self.geometry("700x500")
        self.configure(bg=bg_color)
        self.record_type = record_type
        self.record_manager = record_manager

        # Search label and entry
        search_label = tk.Label(self, text="Search:", bg=bg_color, font=("Arial", 12))
        search_label.pack(pady=5)
        self.search_entry = tk.Entry(self, width=40)
        self.search_entry.pack()
        self.search_entry.bind("<Return>", self.search_records)

        # Table frame
        table_frame = tk.Frame(self, bg="#FFFFFF")
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview for displaying records
        self.tree = ttk.Treeview(table_frame, columns=self.get_columns(), show="headings")
        for col in self.get_columns():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        self.check_vars = {}
        self.load_records()

        # Vertical scrollbar
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=v_scrollbar.set)
        v_scrollbar.pack(side="right", fill="y")

        # Horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscroll=h_scrollbar.set)
        h_scrollbar.pack(side="bottom", fill="x")

        # Button frame
        btn_frame = tk.Frame(self, bg=bg_color)
        btn_frame.pack(pady=10)

        # Add and delete buttons
        add_button = tk.Button(btn_frame, text=f"Add {record_type}", font=("Arial", 12), bg="#87CEFA", command=self.add_record)
        add_button.pack(side="left", padx=5)

        delete_button = tk.Button(btn_frame, text=f"Delete {record_type}", font=("Arial", 12), bg="#FF6961", command=self.confirm_delete)
        delete_button.pack(side="right", padx=5)

    def get_columns(self):
        """
        Returns the columns for the treeview based on the record type.

        Returns:
            list: A list of column names.
        """
        if self.record_type == "Clients":
            return ["ID", "name", "email", "phone"]
        elif self.record_type == "Flights":
            return ["ID", "flight_number", "arrival_time", "departure_city", "arrival_city"]
        elif self.record_type == "Airline Companies":
            return ["ID", "name", "headquarters"]

    def load_records(self):
        """
        Loads records into the treeview.
        """
        records = self.record_manager.records[self.record_type]
        for record in records:
            check_var = tk.BooleanVar()
            self.check_vars[record["ID"]] = check_var
            values = [record.get(col, "") for col in self.get_columns()]
            self.tree.insert("", "end", iid=record["ID"], values=values)
            self.create_checkbutton(record["ID"])

    def create_checkbutton(self, record_id):
        """
        Creates a checkbutton for selecting records.

        Args:
            record_id (int): The ID of the record.
        """
        check_var = self.check_vars[record_id]
        checkbutton = tk.Checkbutton(self.tree, variable=check_var, onvalue=True, offvalue=False)
        self.tree.item(record_id, tags=(record_id,))
        self.tree.tag_bind(record_id, '<ButtonRelease-1>', lambda event, id=record_id: self.toggle_check(id))

    def toggle_check(self, record_id):
        """
        Toggles the check state of a record.

        Args:
            record_id (int): The ID of the record.
        """
        current_value = self.check_vars[record_id].get()
        self.check_vars[record_id].set(not current_value)

    def add_record(self):
        """
        Opens the AddRecordPopup to add a new record.
        """
        AddRecordPopup(self, self.record_type, self.record_manager, self.update_tree)

    def update_tree(self, new_record):
        """
        Updates the treeview with a new record.

        Args:
            new_record (dict): The new record to add.
        """
        check_var = tk.BooleanVar()
        self.check_vars[new_record["ID"]] = check_var
        values = [new_record.get(col, "") for col in self.get_columns()]
        self.tree.insert("", "end", iid=new_record["ID"], values=values)
        self.create_checkbutton(new_record["ID"])

    def confirm_delete(self):
        """
        Opens the DeleteConfirmationPopup to confirm deletion of selected records.
        """
        selected_ids = [record_id for record_id, var in self.check_vars.items() if var.get()]
        if selected_ids:
            DeleteConfirmationPopup(self, self.record_type, selected_ids, self.delete_record)

    def delete_record(self, selected_ids):
        """
        Deletes selected records from the treeview and record manager.

        Args:
            selected_ids (list): The IDs of the records to delete.
        """
        for record_id in selected_ids:
            self.tree.delete(record_id)
            del self.check_vars[record_id]
            self.record_manager.delete_record(self.record_type, record_id)

    def search_records(self, event):
        """
        Searches for records matching the keyword and updates the treeview.

        Args:
            event (tk.Event): The event triggering the search.
        """
        keyword = self.search_entry.get()
        results = self.record_manager.search_records(self.record_type, keyword)
        self.tree.delete(*self.tree.get_children())
        for record in results:
            check_var = tk.BooleanVar()
            self.check_vars[record["ID"]] = check_var
            values = [record.get(col, "") for col in self.get_columns()]
            self.tree.insert("", "end", iid=record["ID"], values=values)
            self.create_checkbutton(record["ID"])