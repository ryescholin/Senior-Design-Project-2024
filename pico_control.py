class Pico:
    """
    Represents a circuit breaker (Pico) in the power grid.
    """

    def __init__(self, name, fault_upper_limit, closed=True, connections=None):
        """
        Constructor for Pico.

        Parameters:
        name (str): Identifier for the breaker.
        fault_upper_limit (float): Upper limit of current for this breaker before fault occurs.
        closed (bool): Initial state of the breaker (default: True).
        connections (dict): Connections to other routes or power sources (default: None).
        """
        self.name = name
        self.fault_upper_limit = fault_upper_limit
        self.is_closed = closed
        self.perm_open = False  # Indicates if breaker is permanently open due to a fault.
        self.connections = connections or {}

    def open(self):
        """Opens the breaker."""
        self.is_closed = False
        print(f"{self.name} opened.")

    def perm_open_breaker(self):
        """Permanently opens the breaker, preventing it from closing."""
        self.is_closed = False
        self.perm_open = True
        print(f"{self.name} permanently opened.")

    def close(self):
        """
        Attempts to close the breaker.

        Returns:
        None
        """
        if self.perm_open:
            print(f"{self.name} cannot close, permanently opened.")
            return
        self.is_closed = True
        print(f"{self.name} closed.")

    def is_fault(self, current):
        """
        Determines if the breaker experiences a fault based on the current.

        Parameters:
        current (float): The current passing through the breaker.

        Returns:
        bool: True if fault occurs, False otherwise.
        """
        return current > self.fault_upper_limit

    def can_provide_power(self):
        """
        Checks if the breaker can provide power based on its connections.

        Returns:
        bool: True if any connection is active, False otherwise.
        """
        return any(self.connections.values())

    def update_connection_status(self, connection_name, status):
        """
        Updates the status of a specific connection.

        Parameters:
        connection_name (str): Name of the connection.
        status (bool): Connection status (True for active, False for inactive).
        """
        if connection_name in self.connections:
            self.connections[connection_name] = status
            print(f"{self.name} connection '{connection_name}' updated to {'active' if status else 'inactive'}.")

    def status(self):
        """
        Provides a formatted string of the breaker's current state.

        Returns:
        str: Formatted breaker status.
        """
        status = "Closed" if self.is_closed else "Open"
        perm_status = "Permanent Open" if self.perm_open else "Normal"
        return f"{self.name}: {status} | {perm_status}"
