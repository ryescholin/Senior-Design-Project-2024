from bluetooth_device import BluetoothDevice

class Route:
    def __init__(self, fault_ranges=None, breakers=None, end_breakers=None, current=0, alternative_power=None):
        # Initialize a Route with fault thresholds, breakers, and alternative power sources
        self.fault_ranges = fault_ranges or []
        self.breakers = breakers or []
        self.current = current
        self.end_breakers = end_breakers or []
        self.alt_power = alternative_power or {}
        self.faulty = False

    def detect_fault(self):
        # Check if current value exceeds fault threshold, indicating a fault
        return self.current > self.fault_ranges[-1]

    def locate_fault(self):
        # Identify which breakers are affected by a fault based on current value
        if self.current <= self.fault_ranges[-2]:
            return [self.breakers[-1]] + self.end_breakers
        for i in range(len(self.fault_ranges) - 1):
            left, right = self.fault_ranges[i], self.fault_ranges[i + 1]
            if left >= self.current > right:
                return [self.breakers[i], self.breakers[i + 1]]
        return []  # On the very off chance that once locate fault has been called, there is still not fault found

    def set_faulty(self):
        # Mark the route as faulty
        self.faulty = True

    def open_fault_breakers(self, fault_breakers):
        # Open breakers in the faulted section to isolate the fault
        for breaker in fault_breakers:
            breaker.set_perm_open()

    def handle_alternative_power(self):
        # Restore power by closing breakers connected to an alternative power source
        if not self.alt_power:
            return
        
        for route_name, shared_breaker in self.alt_power.items():
            if route_name == "power_line" or not shared_breaker.perm_open:
                shared_breaker.set_state_close()
                return

    def handle_fault(self):
        # Execute the full fault detection, isolation, and power restoration process
        if self.detect_fault():
            self.set_faulty()
            fault_breakers = self.locate_fault()
            self.open_fault_breakers(fault_breakers)
            self.handle_alternative_power()
