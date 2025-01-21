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
        self.read_queue = asyncio.Queue()  # Queue for received data
        self.write_queue = asyncio.Queue()  # Queue for outgoing commands

    async def read_from_device(self):
        # Continuously read data from the device
        while self.client.is_connected:
            response = await self.client.read_gatt_char(self.read_uuid)
            logging.info("Received: %s", response.decode())
            await self.read_queue.put(response.decode())  # Send data to the processing queue
            await asyncio.sleep(1)

    async def process_data(self):
        # Process received data and check for faults
        while True:
            data = await self.read_queue.get()
            logging.info("Processing data: %s", data)
            if data.isdigit() and int(data) > self.fault_upper_limit:
                logging.warning("Fault detected at %s!", self.address)
                await self.write_queue.put("FAULT")
            else:
                await self.write_queue.put("OK")

    async def switch_relay(self):
        # Handle outgoing commands
        while True:
            message = await self.write_queue.get()
            logging.info("Sending message: %s", message)
            await self.client.write_gatt_char(self.write_characteristic_uuid, message.encode())
            await asyncio.sleep(1)

    async def open_connection(self, lock: asyncio.Lock):
        # Establish connection with the Bluetooth device
        logging.info("Connecting to %s", self.address)
        async with lock:
            self.client = BleakClient(self.address)
            await self.client.connect()

        logging.info("Connected to %s", self.address)
        tasks = [
            asyncio.create_task(self.read_from_device()),
            asyncio.create_task(self.process_data()),
            asyncio.create_task(self.switch_relay()),
        ]
        await asyncio.gather(*tasks)

    async def open(self):
        # Open the device
        self.is_closed = False
        logging.info("%s opened.", self.address)

    async def perm_open_breaker(self):
        # Permanently open the device
        self.is_closed = False
        self.perm_open = True
        logging.info("%s permanently opened.", self.address)

    async def close(self):
        # Close the device if not permanently opened
        if self.perm_open:
            logging.info("%s cannot close, permanently opened.", self.address)
            return
        self.is_closed = True
        logging.info("%s closed.", self.address)

    def is_fault(self):
        # Check if current exceeds fault limit
        return self.current > self.fault_upper_limit

    def can_provide_power(self):
        # Check if any connections are active
        return any(self.connections.values())

    def update_connection_status(self, connection_name, status):
        # Update the status of a specific connection
        if connection_name in self.connections:
            self.connections[connection_name] = status
            logging.info("%s connection '%s' updated to %s.", self.address, connection_name, "active" if status else "inactive")

# Change relay state outside the async loop
async def change_relay_state(device, new_state):
    async with asyncio.Lock():
        device.relay_state = new_state
        logging.info("Relay state for %s set to %s", device.address, "ON" if new_state else "OFF")

# Create multiple Bluetooth device instances and toggle relays
async def main():
    lock = asyncio.Lock()
    MAC_ADDRESSES = ["28:CD:C1:11:90:2E", "28:CD:C1:0E:C3:D7"]
    devices = [BluetoothDevice(mac) for mac in MAC_ADDRESSES]
    await asyncio.gather(*(device.open_connection(lock) for device in devices))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s")
    asyncio.run(main())
