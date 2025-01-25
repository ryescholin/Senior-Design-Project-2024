import asyncio
from initial_values import setup_initial_values

async def main():
    # Set up initial values and start threads
    grid, pico1, pico2_end = await setup_initial_values()

    await pico1.switch_relay()
    await pico2_end.switch_relay()
    await asyncio.sleep(0.5)

    # check if relay states are now correct
    assert pico1.relay_state == True, f"Pico1 relay state not set to True"
    assert pico2_end.relay_state == False, f"Pico2_end relay state not set to False"
    print("Step 1: Initial relay states verified.")

    # check if recieving current reading
    await pico1.read_from_device()
    await pico2_end.read_from_device()
    await asyncio.sleep(0.5)
    assert pico1.current > 0 or pico2_end.current > 0, "No current readings received from either device"
    print("Step 2: Current readings verified.")

    # Step 3: Toggle relay states (open Pico1, close Pico2_end)
    pico1.relay_state = False  # Open
    pico2_end.relay_state = True  # Closed
    await pico1.switch_relay()
    await asyncio.sleep(0.5)
    await pico2_end.switch_relay()
    await asyncio.sleep(0.5)

    # Assert the new relay states
    assert pico1.relay_state == False, f"Pico1 relay state not set to False"
    assert pico2_end.relay_state == True, f"Pico2_end relay state not set to True"
    print("Step 3: Relay state toggling verified.")

if __name__ == "__main__":
    asyncio.run(main())
