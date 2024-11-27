class Route:
    """
    Represents a route in the power grid.
    """

    def __init__(self, name, breakers, end_breaker):
        """
        Constructor for Route.

        Parameters:
        name (str): Name of the route.
        breakers (list): List of Pico objects representing the route's breakers.
        end_breaker (Pico): The end breaker for the route.
        """
        self.name = name
        self.breakers = breakers
        self.end_breaker = end_breaker
        self.fault_occurred = False

    def mark_faulty(self):
        """Marks the route as faulty and disables power to the end breaker."""
        self.fault_occurred = True
        print(f"{self.name}: Fault occurred. Cannot supply power.")
        self.end_breaker.update_connection_status(self.name, False)
        self.end_breaker.open()

    def try_power_end_pico(self):
        """
        Attempts to restore power to the end breaker via alternate connections.

        Returns:
        None
        """
        if self.end_breaker.can_provide_power():
            print(f"{self.name}: Power restored through an alternate connection.")
            self.end_breaker.close()
        else:
            print(f"{self.name}: No alternate power source available. Route cannot be powered.")
