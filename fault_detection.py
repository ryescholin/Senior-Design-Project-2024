from transmission_lines import TransmissionLine

class FaultDetection:
    def __init__(self, grid):
        self.grid = grid

    def detect_fault(self, route_values):
        faults = []
        for route in self.grid.routes:
            current = route_values[route.name]
            for element in route.elements:
                if isinstance(element, TransmissionLine) and not element.fault_has_occured() and element.is_fault_in_range(current):
                    faults.append(element.name)
                    element.active_fault()  # Isolate the faulted line by opening breakers
        if faults:
            print("Faults detected. Initiating rerouting.")
            self.grid.reroute_power()
            self.grid.verify_power_restoration()
            return faults
        else:
            return ["No Fault"]
