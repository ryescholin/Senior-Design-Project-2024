import argparse
import asyncio
import contextlib
import logging
from bleak import BleakClient, uuids, BleakScanner

class BluetoothDevice:
    def __init__(self, address: str, fault_upper_limit=400, closed=True, connections=None):
        # Initialize Bluetooth device with address and parameters
        self.address = address
        self.write_characteristic_uuid = uuids.normalize_uuid_16(0x2A6E)
        self.read_uuid = uuids.normalize_uuid_16(0x2A6F)
        self.relay_state = None
        self.client = None
        self.fault_upper_limit = fault_upper_limit
        self.is_closed = closed
        self.perm_open = False
        self.connections = connections or {}
        self.current = 0

    async def read_from_device(self):
        # Continuously read data from the device
        while self.client.is_connected:
            response = await self.client.read_gatt_char(self.read_uuid)
            print("Received response from %s: %s", self.client.address, response.decode())
            await asyncio.sleep(5)

    async def switch_relay(self):
        # Switch relay state based on current configuration
        if self.relay_state is not None:
            message = "True" if self.relay_state else "False"
            try:
                await self.client.write_gatt_char(self.write_characteristic_uuid, message.encode("utf-8"))
                print("Sent message to %s: %s", self.address, message)
            except Exception as e:
                logging.error("Error switching relay for %s: %s", self.address, e)
            self.relay_state = None
        await asyncio.sleep(5)

    async def open_connection(self, lock: asyncio.Lock):
        # Establish connection with the Bluetooth device
        print("Starting task for device with address %s", self.address)
        async with contextlib.AsyncExitStack() as stack:
            async with lock:
                self.client = BleakClient(self.address)
                print("Connecting to %s", self.address)
                await stack.enter_async_context(self.client)
                print("Connected to %s", self.address)
                stack.callback(print, "disconnecting from %s", self.address)
            read_task = asyncio.create_task(self.read_from_device())
            write_task = asyncio.create_task(self.switch_relay())
            await asyncio.gather(read_task, write_task)
        print("Disconnected from %s", self.address)

    async def open(self):
        self.is_closed = False
        print("%s opened.", self.address)

    async def perm_open_breaker(self):
        # Permanently open the device
        self.is_closed = False
        self.perm_open = True
        print("%s permanently opened.", self.address)

    async def close(self):
        # Close the device if not permanently opened
        if self.perm_open:
            print("%s cannot close, permanently opened.", self.address)
            return
        self.is_closed = True
        print("%s closed.", self.address)

    def is_fault(self): return self.current > self.fault_upper_limit
    def can_provide_power(self): return any(self.connections.values())


    def update_connection_status(self, connection_name, status):
        # Update the status of a specific connection
        if connection_name in self.connections:
            self.connections[connection_name] = status
            print("%s connection '%s' updated to %s.", self.address, connection_name, "active" if status else "inactive")

# Change relay state outside the async loop
async def change_relay_state(device, new_state):
    async with asyncio.Lock():
        device.relay_state = new_state
        print("Relay state for %s set to %s", device.address, "ON" if new_state else "OFF")

# Create multiple Bluetooth device instances and toggle relays
async def main():
    lock = asyncio.Lock()
    MAC_ADDRESSES = ["28:CD:C1:11:90:2E", "28:CD:C1:0E:C3:D7"]
    devices = [BluetoothDevice(mac) for mac in MAC_ADDRESSES]
    await asyncio.gather(*(device.open_connection(lock) for device in devices))

if __name__ == "__main__":
    logging.basicConfig(level=print, format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s")
    asyncio.run(main())
