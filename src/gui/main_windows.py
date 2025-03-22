import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from recordmanager.record_manager import RecordManager
from .tab_windows import ClientsTab, FlightsTab, AirlinesTab

# Define assets directory
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "../assets")

# Define paths for images
cloud_path = os.path.abspath(os.path.join(ASSETS_DIR, "cloud.png"))
plane_path = os.path.abspath(os.path.join(ASSETS_DIR, "plane.png"))

# Verify file paths
print(f"Checking cloud image path: {cloud_path}")
print(f"Checking plane image path: {plane_path}")
print("Cloud Image Exists:", os.path.exists(cloud_path))
print("Plane Image Exists:", os.path.exists(plane_path))

class FlightManagerApp(tk.Tk):
    """
    Main application window for the Flight Manager.
    """

    def __init__(self):
        """
        Initializes the Flight Manager application, setting up the main window and loading resources.
        """
        super().__init__()
        self.title("Flight Manager")
        self.geometry("800x600")
        self.configure(bg="#ADD8E6")  # Light Blue Background

        # Check if image files exist
        if not os.path.exists(cloud_path) or not os.path.exists(plane_path):
            print("ERROR: One or both image files are missing!")
            return

        # Load and resize images
        self.cloud_img = ImageTk.PhotoImage(Image.open(cloud_path).resize((800, 600)))
        self.plane_img = ImageTk.PhotoImage(Image.open(plane_path).resize((300, 150)))

        # Initialize record manager and load records
        self.record_manager = RecordManager()
        self.session_records = self.record_manager.load_records()

        # Create the main page
        self.create_main_page()

    def create_main_page(self):
        """
        Creates the main selection page with background and buttons for Clients, Flights, and Airline Companies.
        """
        canvas = tk.Canvas(self, width=800, height=600, bg="#ADD8E6", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Add background images
        canvas.create_image(400, 300, image=self.cloud_img, anchor="center")
        canvas.create_image(600, 200, image=self.plane_img, anchor="center")

        # Add title label
        title = tk.Label(self, text="Flight Manager", font=("Arial", 20, "bold"), bg="#ADD8E6")
        canvas.create_window(400, 50, window=title)

        # Create buttons for different tabs
        self.create_rounded_button(canvas, "Clients", "#FFCCCB", self.open_clients_tab, 400, 300)
        self.create_rounded_button(canvas, "Flights", "#FFFF99", self.open_flights_tab, 400, 370)
        self.create_rounded_button(canvas, "Airline Companies", "#A7E9A1", self.open_airlines_tab, 400, 440)

    def create_rounded_button(self, canvas, text, color, command, x, y):
        """
        Creates a rounded button on the canvas.

        Args:
            canvas (tk.Canvas): The canvas to place the button on.
            text (str): The text to display on the button.
            color (str): The background color of the button.
            command (function): The function to call when the button is clicked.
            x (int): The x-coordinate for the button placement.
            y (int): The y-coordinate for the button placement.
        """
        frame = tk.Frame(self, bg=color, bd=2, relief="ridge")
        button = tk.Button(frame, text=text, font=("Arial", 14, "bold"), bg=color, borderwidth=0, command=command)
        canvas.create_window(x, y, window=frame)
        button.pack(fill="both", expand=True)

    def open_clients_tab(self):
        """
        Opens the Clients tab.
        """
        ClientsTab(self, self.record_manager)

    def open_flights_tab(self):
        """
        Opens the Flights tab.
        """
        FlightsTab(self, self.record_manager)

    def open_airlines_tab(self):
        """
        Opens the Airline Companies tab.
        """
        AirlinesTab(self, self.record_manager)

if __name__ == "__main__":
    app = FlightManagerApp()
    app.mainloop()