import asyncio
from initial_values import setup_initial_values

async def main():
    # Setup initial values and devices
    grid, pico1, pico2_end = await setup_initial_values()

    # Read data from devices
    data1 = await pico1.read_queue.get()
    data2 = await pico2_end.read_queue.get()
    print(f"Pico1 received: {data1}")
    print(f"Pico2_end received: {data2}")

    # Write back names and information to devices
    await pico1.write_queue.put(f"Name: Pico1, Data: {data1}")
    await pico2_end.write_queue.put(f"Name: Pico2_end, Data: {data2}")

if __name__ == "__main__":
    asyncio.run(main())
