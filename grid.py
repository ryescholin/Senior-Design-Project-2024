from route import Route
from pico_control import Pico
from transmission_lines import TransmissionLine

class Grid:
    def __init__(self):
        self.routes = []

    def add_route(self, route):
        """Add a route to the grid."""
        self.routes.append(route)

    def reroute_power(self):
        print("\n--- Starting reroute_power ---")

        # Step 1: Update each route's power status based on faults
        print("Step 1: Updating initial power status based on faults.")
        for route in self.routes:
            print(f"Updating power status for {route.name}")
            route.update_power_status()
            route.print_detailed_status()  # Print the status after initial update

        # Step 2: Check if end breaker (1_end_2) is in any route and if it can close
        print("\nStep 2: Checking if 1_end_2 can be closed to reroute power.")
        end_breaker_name = "1_end_2"
        end_breaker = None

        # Locate the end breaker (1_end_2)
        for route in self.routes:
            for element in route.elements:
                if isinstance(element, Pico) and element.get_breaker_name() == end_breaker_name:
                    end_breaker = element
                    break

        # Ensure 1_end_2 is present and powered by Route 2
        if end_breaker:
            # Check if Route 2 can power 1_end_2
            route_2_powered = any(
                isinstance(line, TransmissionLine) and
                line.right_breaker.get_breaker_name() == end_breaker_name and
                line.power_status == "powered"
                for route in self.routes
                for line in route.elements
            )

            if route_2_powered and not end_breaker.is_breaker_closed():
                end_breaker.close()
                print(f"1_end_2 has been closed to provide power to Route 1.")

            # Reverse-check Route 1 elements from 1_end_2 back to the fault
            for route in self.routes:
                if end_breaker in route.elements:
                    print(f"Restoring power to Route 1 in reverse from 1_end_2.")
                    for element in reversed(route.elements):
                        # Stop if we encounter the fault or a permanently open breaker
                        if isinstance(element, TransmissionLine):
                            if element.occured_fault:
                                print(f"Stopping at fault in line {element.name}")
                                break
                            element.power_status = "powered"
                            print(f"Line {element.name} now powered.")
                        elif isinstance(element, Pico):
                            if not element.is_breaker_closed():
                                print(f"Stopping at permanently open breaker {element.get_breaker_name()}")
                                break
                            print(f"Breaker {element.get_breaker_name()} is closed and allows power to pass.")
                    break

        print("--- Finished reroute_power ---\n")

    def verify_power_restoration(self):
        """Verify and print the power restoration status for all routes."""
        print("\n--- Verifying power restoration ---")
        for route in self.routes:
            route.print_detailed_status()
        print("--- Finished verifying power restoration ---")
