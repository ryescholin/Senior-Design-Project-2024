import asyncio
from initial_values import setup_initial_values

def main():
    # Initialize grid and devices
    grid, pico1, pico2 = setup_initial_values()
    print("Grid and devices initialized.")

    # Start connecting devices in the grid asynchronously
    async def initialize_devices():
        lock = asyncio.Lock()
        await asyncio.gather(
            pico1.open_connection(lock),
            pico2.open_connection(lock)
        )

    asyncio.run(initialize_devices())

if __name__ == "__main__":
    main()