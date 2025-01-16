class Route:
    #Represents a power grid route.

    def __init__(self, name, breakers, end_breaker):
        # Initialize with name, breakers, and end breaker
        self.name = name
        self.breakers = breakers
        self.end_breaker = end_breaker
        self.fault_occurred = False

    async def mark_faulty(self):
        # Mark route as faulty and disable end breaker
        self.fault_occurred = True
        print(f"{self.name}: Fault occurred. Cannot supply power.")
        await self.end_breaker.update_connection_status(self.name, False)
        await self.end_breaker.open()

    async def try_power_end_pico(self):
        # Attempt to restore power to end breaker
        if self.end_breaker.can_provide_power():
            print(f"{self.name}: Power restored via alternate connection.")
            await self.end_breaker.close()
        else:
            print(f"{self.name}: No alternate power source available.")