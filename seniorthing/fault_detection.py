class FaultDetection:
    """Detects faults in the grid."""

    def __init__(self, grid):
        self.grid = grid

    def detect_fault(self, route_name, current, breakers):
        """
        Detects and handles faults in the grid.

        Args:
            route_name (str): The route to monitor.
            current (float): The current value to check.
            breakers (dict): Dictionary of breaker objects.
        """
        # Find the route by name
        print(f"Iteration: Simulated Current {current}")
        route = None
        for r in self.grid.routes:
            if r.name == route_name:
                route = r
                break

        if not route:
            print(f"Route {route_name} not found.")
            return

        # Get the route's fault range
        route_fault_range = [breaker.fault_upper_limit for breaker in route.breakers]
        max_fault = max(route_fault_range)
        min_fault = route.breakers[-1].fault_upper_limit  # The last breaker's upper limit

        # **CASE 1**: Current is below the minimum threshold
        if current <= min_fault:
            print(f"No fault detected.")
            return

        # **CASE 2**: Identify fault between breakers
        faulty_breaker1 = None
        faulty_breaker2 = None
        for i in range(len(route.breakers) - 1):
            if current > route.breakers[i + 1].fault_upper_limit and current <= route.breakers[i].fault_upper_limit:
                faulty_breaker1 = route.breakers[i]
                faulty_breaker2 = route.breakers[i + 1]
                print(f"Fault identified between {faulty_breaker1.name} and {faulty_breaker2.name}.")
                break

        if not faulty_breaker1 or not faulty_breaker2:
            print("No fault detected within the range.")
            return

        # Permanently open the faulty breakers
        print(f"Fault detected. Permanently opening breakers {faulty_breaker1.name} and {faulty_breaker2.name}.")
        faulty_breaker1.perm_open_breaker()
        faulty_breaker2.perm_open_breaker()

        # Mark the route as faulty
        route.mark_faulty()

        # Check if the end breaker can be powered from another connection
        route.try_power_end_pico()
