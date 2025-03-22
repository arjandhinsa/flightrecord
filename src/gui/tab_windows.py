from .table_windows import TableWindow

# Specific Tabs for Clients, Flights, and Airlines
class ClientsTab(TableWindow):
    """
    A tab for displaying and managing client records.
    """

    def __init__(self, parent, record_manager):
        """
        Initializes the ClientsTab.

        Args:
            parent (tk.Widget): The parent widget.
            record_manager (RecordManager): The record manager instance.
        """
        super().__init__(parent, "Clients", "#FFCCCB", "Clients", record_manager)


class FlightsTab(TableWindow):
    """
    A tab for displaying and managing flight records.
    """

    def __init__(self, parent, record_manager):
        """
        Initializes the FlightsTab.

        Args:
            parent (tk.Widget): The parent widget.
            record_manager (RecordManager): The record manager instance.
        """
        super().__init__(parent, "Flights", "#FFFF99", "Flights", record_manager)


class AirlinesTab(TableWindow):
    """
    A tab for displaying and managing airline company records.
    """

    def __init__(self, parent, record_manager):
        """
        Initializes the AirlinesTab.

        Args:
            parent (tk.Widget): The parent widget.
            record_manager (RecordManager): The record manager instance.
        """
        super().__init__(parent, "Airline Companies", "#A7E9A1", "Airline Companies", record_manager)