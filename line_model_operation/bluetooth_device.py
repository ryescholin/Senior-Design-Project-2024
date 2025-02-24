import argparse
import asyncio
import contextlib
import logging
from bleak import BleakClient, uuids, BleakScanner

class BluetoothDevice:
    def __init__(self, name: str, address: str, fault_upper_limit=400, state=True):
        self.address = address
        self.name = name
        self.write_characteristic_uuid = uuids.normalize_uuid_16(0x2A6E)
        self.read_uuid = uuids.normalize_uuid_16(0x2A6F)
        self.client = None
        self.state = state
        self.perm_open = False
        self.connection = False
        self.current = 0
        self.set_state = None  # Ensure this is properly initialized

    async def read_from_device(self):
        while self.client.is_connected:
            response = await self.client.read_gatt_char(self.read_uuid)
            decoded_response = response.decode()
            print(f"Received response from {self.client.address}: {decoded_response}")

            parts = decoded_response.split(",", 1)
            self.state = parts[0]
            self.current = str(parts[1]) if len(parts) > 1 else None
            await asyncio.sleep(5)

    async def switch_relay(self):
        if self.set_state is not None:
            message = "True" if self.set_state else "False"
            try:
                await self.client.write_gatt_char(self.write_characteristic_uuid, message.encode("utf-8"))
                print(f"Sent message to {self.address}: {message}")
            except Exception as e:
                logging.error(f"Error switching relay for {self.address}: {e}")
            self.set_state = None
        await asyncio.sleep(5)

    async def open_connection(self, lock: asyncio.Lock):
        print(f"Starting task for device with address {self.address}")
        async with contextlib.AsyncExitStack() as stack:
            async with lock:
                self.client = BleakClient(self.address)
                print(f"Connecting to {self.address}")
                await stack.enter_async_context(self.client)
                self.connection = True
                print(f"Connected to {self.address}")
                stack.callback(print, f"Disconnecting from {self.address}")
                
            read_task = asyncio.create_task(self.read_from_device())
            write_task = asyncio.create_task(self.switch_relay())
            await asyncio.gather(read_task, write_task)

        print(f"Disconnected from {self.address}")
        self.connection = False

    async def set_perm_open(self):
        self.perm_open = True
        await self.change_relay_state(False)

    async def set_state_open(self):
        await self.change_relay_state(False)

    async def set_state_close(self):
        if self.perm_open:
            print(f"{self.name} is permanently open and cannot be closed")
        else:
            await self.change_relay_state(True)

    async def change_relay_state(self, new_state):
        async with asyncio.Lock():
            self.set_state = new_state
            await self.switch_relay()
            print(f"Relay state for {self.address} set to {'ON' if new_state else 'OFF'}")
            self.state = new_state

    def get_state(self):
        return self.state


async def main():
    lock = asyncio.Lock()
    devices = [
        BluetoothDevice("Device1", "28:CD:C1:11:90:2E"),
        BluetoothDevice("Device2", "28:CD:C1:0E:C3:D7"),
    ]
    
    await asyncio.gather(*(device.open_connection(lock) for device in devices))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s")
    asyncio.run(main())
