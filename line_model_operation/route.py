from bluetooth_device import BluetoothDevice
import asyncio

class Route:
    def __init__(self, fault_ranges=None, breakers=None, end_breakers=None, current=0, alternative_power=None):
        self.fault_ranges = fault_ranges or []
        self.breakers = breakers or []
        self.current = current
        self.end_breakers = end_breakers or []
        self.alt_power = alternative_power or {}
        self.faulty = False

    async def initialize(self):
        """Initialize breakers by connecting to Bluetooth devices."""
        lock = asyncio.Lock()
        await asyncio.gather(*(breaker.open_connection(lock) for breaker in self.breakers))

    def detect_fault(self):
        return self.current > self.fault_ranges[-1]

    def locate_fault(self):
        if self.current <= self.fault_ranges[-2]:
            return [self.breakers[-1]] + self.end_breakers
        for i in range(len(self.fault_ranges) - 1):
            left, right = self.fault_ranges[i], self.fault_ranges[i + 1]
            if left >= self.current > right:
                return [self.breakers[i], self.breakers[i + 1]]
        return []

    def set_faulty(self):
        self.faulty = True

    async def open_fault_breakers(self, fault_breakers):
        for breaker in fault_breakers:
            await breaker.set_perm_open()

    async def handle_alternative_power(self):
        if not self.alt_power:
            return

        for route_name, shared_breaker in self.alt_power.items():
            if route_name == "power_line" or not shared_breaker.perm_open:
                await shared_breaker.set_state_close()
                return

    async def handle_fault(self):
        if self.detect_fault():
            self.set_faulty()
            fault_breakers = self.locate_fault()
            await self.open_fault_breakers(fault_breakers)
            await self.handle_alternative_power()
