import asyncio
from bleak import BleakClient, BleakScanner, uuids
import logging

class BluetoothDevice:
    def __init__(self, address, service_uuid, characteristic_uuid):
        self.address = address
        self.service_uuid = service_uuid
        self.characteristic_uuid = characteristic_uuid
        self.current = None
        self.relay_state = None
        self.client = None
        self.connected = False

    async def connect(self, lock):
        async with lock:
            if self.connected:
                logging.warning(f"Device {self.address} is already connected.")
                return
            logging.info(f"Scanning for device: {self.address}")    
            device = await BleakScanner.find_device_by_address(self.address)
            if not device:
                logging.error(f"Device {self.address} not found.")
                return
            logging.info(f"Found device: {self.address}, attempting to connect...")
            self.client = BleakClient(device)
            try:
                await self.client.connect()
                self.connected = True
                logging.info(f"Connected to {self.address}")
            except Exception as e:
                logging.error(f"Error connecting to {self.address}: {e}")

    async def disconnect(self):
        if self.client and self.connected:
            try:
                await self.client.disconnect()
                self.connected = False
                logging.info(f"Disconnected from {self.address}")
            except Exception:
                pass

    async def start_notifications(self):
        if not self.connected:
            logging.error(f"Device {self.address} is not connected.")
            return

        def notification_handler(_, data):
            logging.info(f"{self.address} received: {data}")
            try:
                decoded_data = data.decode("utf-8")
                if decoded_data.isdigit():
                    self.current = float(decoded_data)
                elif decoded_data in ["True", "False"]:
                    self.relay_state = decoded_data == "True"
            except Exception:
                pass

        try:
            await self.client.start_notify(self.characteristic_uuid, notification_handler)
        except Exception:
            pass

    async def stop_notifications(self):
        if self.client and self.connected:
            try:
                await self.client.stop_notify(self.characteristic_uuid)
            except Exception:
                pass

    async def switch_relay(self, state: bool):
        if not self.connected:
            logging.error(f"Device {self.address} is not connected.")
            return
        message = "True" if state else "False"
        try:
            await self.client.write_gatt_char(self.characteristic_uuid, message.encode("utf-8"))
            logging.info(f"Sent to {self.address}: {message}")
            self.relay_state = state
        except Exception as e:
                logging.error(f"Error sending message to {self.address}: {e}")


async def main():
    lock = asyncio.Lock()
    devices = [
        BluetoothDevice("28:CD:C1:0E:C3:D6", uuids.normalize_uuid_16(0x1848), uuids.normalize_uuid_16(0x2A6E)),
        BluetoothDevice("28:CD:C1:0E:C3:D7", uuids.normalize_uuid_16(0x1848), uuids.normalize_uuid_16(0x2A6E)),
    ]

    async def setup_device(device):
        await device.connect(lock)
        if device.connected:
            await device.start_notifications()

    try:
        await asyncio.gather(*(setup_device(device) for device in devices))
        await asyncio.gather(
            devices[0].switch_relay(True),
            devices[1].switch_relay(True),
        )
        await asyncio.sleep(10)
    finally:
        await asyncio.gather(*(device.stop_notifications() for device in devices))
        await asyncio.gather(*(device.disconnect() for device in devices))


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )
    asyncio.run(main())