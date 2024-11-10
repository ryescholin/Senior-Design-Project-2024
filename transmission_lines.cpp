from pico_control import Pico

class TransmissionLine:
    def __init__(self, left, right, high, low):
        self.left_breaker = left
        self.right_breaker = right
        self.high_amp = high
        self.low_amp = low
        self.name = f"{left.get_breaker_name()}-{right.get_breaker_name()}"
        self.occured_fault = False
        self.power_status = "powered"  # Default to powered

    def is_fault_in_range(self, current):
        return self.low_amp < current <= self.high_amp
    
    def active_fault(self):
        self.occured_fault = True
        self.power_status = "faulty"  # Mark as faulty
        self.permanently_open_breakers()

    def fault_has_occured(self):
        return self.occured_fault

    def permanently_open_breakers(self):
        if isinstance(self.left_breaker, Pico):
            self.left_breaker.open()
            self.left_breaker.perm_open()
            print(f"{self.left_breaker.get_breaker_name()} permanently opened due to fault in {self.name}.")
        
        if isinstance(self.right_breaker, Pico):
            self.right_breaker.open()
            self.right_breaker.perm_open()
            print(f"{self.right_breaker.get_breaker_name()} permanently opened due to fault in {self.name}.")

    def get_status(self):
        return self.power_status
