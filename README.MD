# Flight Manager

Flight Manager is a desktop application to manage flight records, clients, and airline companies. It provides a graphical user interface (GUI) for easy interaction and management of records.

## Project Structure

```
/project-root
├── src/
│   ├── main.py
│   ├── assets/
│   │   ├── cloud.png
│   │   └── plane.png
│   ├── gui/
│   │   ├── main_windows.py
│   │   ├── popup_windows.py
│   │   ├── table_windows.py
│   │   ├── tab_windows.py
│   │   └── __init__.py
│   ├── json_db/
│   │   └── records.json
│   └── recordmanager/
│       ├── record_manager.py
│       └── __init__.py
└── tests/
    ├── flight_control_performance_2.py
    ├── flight_control_performance.py
    ├── flight_control_unittest.py
    ├── profile.png
    └── profile.prof
```

## Features

- **Manage Clients**: Add, update, delete, and search client records.
- **Manage Flights**: Add, update, delete, and search flight records.
- **Manage Airline Companies**: Add, update, delete, and search airline company records.
- **Performance Testing**: Includes scripts to test the performance of record operations.
- **Unit Testing**: Includes scripts to test the operations to related to record.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd project-root
   ```

2. **Install Dependencies**:
   Ensure you have Python installed. You will need to install additional dependencies to ensure the code runs properly.

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   Navigate to the `src` directory and run the main application.

   ```bash
   python main.py
   ```

## Usage

- **Start the Application**: Run `main.py` to start the Flight Manager application.
- **Navigate the GUI**: Use the buttons to manage clients, flights, and airline companies.
- **Performance Testing**: Use the scripts in the `tests` directory to run performance and unit tests.

## Testing

Unit and Performance tests are provided in the `tests` directory. You can run them using:

```bash
python flight_control_performance_2.py
python flight_control_performance.py
python flight_control_unittest.py
```


