class FaultDetection:
    #Detects and handles faults in the grid.

    def __init__(self, grid):
        self.grid = grid

    async def detect_faults(self):
        # Continuously check for faults on all breakers
        for route in self.grid.routes:
            for breaker in route.breakers:
                if breaker.is_fault():
                    print(f"Fault detected at {breaker.address}. Opening breaker.")
                    await breaker.perm_open_breaker()
                    await route.mark_faulty()

        # Attempt to restore power to routes
        for route in self.grid.routes:
            await route.try_power_end_pico()