# Flight Manager

Flight Manager is a desktop application to manage flight records, clients, and airline companies. It provides a graphical user interface (GUI) for easy interaction and management of records.

## Project Structure

```
/GROUPB
├── docs/
│   ├── Group Project Report.doc
│   └── MeetingMinutes/
│       ├── Meeting_01- Group Assignments - Minutes (1).doc
│       ├── Meeting_02- Group Assignments - Minutes (1).doc
│       └── Meeting_03- Group Assignments - Minutes.doc
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
├── tests/
│   ├── flight_control_performance_2.py
│   ├── flight_control_performance.py
│   ├── flight_control_unittest.py
│   ├── profile.png
│   ├── profile.prof
│   ├── records.json
│   └── records_perf_test.json
├── README.MD
└── requirements.txt
```

## Features

- **Manage Clients**: Add, update, delete, and search client records.
- **Manage Flights**: Add, update, delete, and search flight records.
- **Manage Airline Companies**: Add, update, delete, and search airline company records.
- **Performance Testing**: Includes scripts to test the performance of record operations.
- **Unit Testing**: Includes scripts to test the operations related to records.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/arjandhinsa/flightrecord.git
   cd flightrecord/GROUPB



2. **Install Dependencies**:
   Make sure Python is installed. Then install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   Navigate to the `src` folder and run the application:

   ```bash
   cd src
   python main.py
   ```

## Usage

- **Start the Application**: Run `main.py` to launch the Flight Manager.
- **Navigate the GUI**: Use tabs to manage Clients, Flights, and Airline Companies.
- **Add/Edit/Delete Records**: Use the corresponding buttons and pop-up windows to manage data.
- **Performance Testing**: Run test scripts located in the `tests` directory.

## Testing

Run tests from the `tests/` directory using:

```bash
python flight_control_performance_2.py
python flight_control_performance.py
python flight_control_unittest.py
```


