from bluetooth_device import BluetoothDevice
from route import Route
from grid import Grid

def setup_initial_values():
    # Define addresses for Bluetooth devices
    pico1_address = "28:CD:C1:11:90:2E"
    pico2_address = "28:CD:C1:0E:C3:D7"

    # Create BluetoothDevice objects for Pico 1 (closed) and Pico 2 (open)
    pico1 = BluetoothDevice(pico1_address, fault_upper_limit=250, closed=True)
    pico2_end = BluetoothDevice(pico2_address, fault_upper_limit=100, closed=False, connections={"Route 1": True, "powerline": True})

    # Define a grid and routes
    grid = Grid()

    # Create a route with Pico devices
    route1 = Route(
        "Route 1",
        breakers=[pico1, pico2_end],
        end_breaker=pico2_end
    )

    grid.add_route(route1)

    return grid, pico1, pico2_end