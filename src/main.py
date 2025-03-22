from gui.main_windows import FlightManagerApp
from recordmanager.record_manager import RecordManager
 

"""Main function to initialize and run the Flight Manager application."""
def main():
    # Initialize the record manager
    manager = RecordManager()
    print("Flight Manager Backend initialized.")
    print("Records loaded successfully.")

    # Initialize the GUI application
    app = FlightManagerApp()
    app.mainloop()  # Start the Tkinter main loop

if __name__ == "__main__":
    main()