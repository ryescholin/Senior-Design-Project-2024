import asyncio
import threading
from bluetooth_device import BluetoothDevice
from route import Route
from grid import Grid

async def setup_initial_values():
    # Bluetooth devices addresses
    pico1_address = "28:CD:C1:11:90:2E"
    pico2_address = "28:CD:C1:0E:C3:D7"


    pico1 = BluetoothDevice(pico1_address, fault_upper_limit=250, closed=True)
    pico2_end = BluetoothDevice(pico2_address, fault_upper_limit=100, closed=False, connections={"Route 1": True, "powerline": True})

    devices = [pico1, pico2_end]

    grid = Grid()
    route1 = Route(
        "Route 1",
        breakers=[pico1, pico2_end],
        end_breaker=pico2_end
    )
    grid.add_route(route1)

    lock = asyncio.Lock()

# might get locked up here... run from main to be sure
    print("before gather")
    return asyncio.gather(*(device.open_connection(lock) for device in devices))
    print("after gather")

    return grid, pico1, pico2_end