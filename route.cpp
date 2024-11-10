from transmission_lines import TransmissionLine

class Route:
    def __init__(self, name):
        self.name = name
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def has_power_source(self):
        """Check if any segment in the route has a connection to a power source."""
        for element in self.elements:
            if isinstance(element, TransmissionLine):
                if element.left_breaker.is_breaker_closed() or element.right_breaker.is_breaker_closed():
                    print(f"{self.name} has power source through {element.name}")
                    return True
        print(f"{self.name} has no power source.")
        return False

    def update_power_status(self):
        power_available = True
        for element in self.elements:
            if isinstance(element, TransmissionLine):
                if element.occured_fault:
                    element.power_status = "faulty"
                    power_available = False
                elif power_available:
                    element.power_status = "powered"
                else:
                    element.power_status = "no_power"

    def print_detailed_status(self):
        print(f"{self.name}: ", end="")
        status_output = []
        for element in self.elements:
            if isinstance(element, TransmissionLine):
                line_status = f"{element.name}({element.get_status()})"
                status_output.append(line_status)
        print(" -> ".join(status_output))
