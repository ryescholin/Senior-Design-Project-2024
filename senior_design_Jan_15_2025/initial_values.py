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

    grid = Grid()
    route1 = Route(
        "Route 1",
        breakers=[pico1, pico2_end],
        end_breaker=pico2_end
    )
    grid.add_route(route1)

    # Start threads for reading and writing
    def run_device(device):
        async def device_task():
            lock = asyncio.Lock()
            await device.open_connection(lock)
        asyncio.run(device_task())

    threading.Thread(target=run_device, args=(pico1,), daemon=True).start()
    threading.Thread(target=run_device, args=(pico2_end,), daemon=True).start()

    return grid, pico1, pico2_end