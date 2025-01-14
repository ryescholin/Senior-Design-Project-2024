from bluetooth_device import BluetoothDevice
from pico_control import Pico
import asyncio
import time
import threading


class BluetoothConverter:
    """
    A simple way to connect Bluetooth devices and map them to Pico objects.
    """

    def __init__(self, addresses, fault_limits):
        """
        Sets up Bluetooth devices and creates Pico objects.

        Parameters:
        - addresses (list): List of Bluetooth device addresses.
        - fault_limits (dict): A dictionary of fault limits for each device address.
        """
        self.devices = []  # List to hold BluetoothDevice objects
        self.picos = {}  # Dictionary to map addresses to Pico objects

        # Create BluetoothDevice and Pico objects
        for address in addresses:
            device = BluetoothDevice(
                address=address,
                connection_lock=asyncio.Lock(),  # Lock for connecting safely
                connected_event=asyncio.Event(),  # Event to track connection
            )
            self.devices.append(device)

            # Create Pico objects with fault limits
            fault_limit = fault_limits.get(address, 400)  # Default fault limit = 400
            self.picos[address] = Pico(name=address, fault_upper_limit=fault_limit)

    async def connect_devices(self):
        """
        Connect to all Bluetooth devices.
        """
        print("Connecting to all devices...")
        await asyncio.gather(*(device.open_connection() for device in self.devices))
        print("All devices connected!")

    def start_monitoring_threads(self):
        """
        Start monitoring all devices in separate threads.
        """
        print("Starting monitoring threads for devices...")
        for device in self.devices:
            thread = threading.Thread(target=self._monitor_device, args=(device,))
            thread.start()

    def _monitor_device(self, device):
        """
        Monitors a Bluetooth device and updates its Pico object.

        Parameters:
        - device (BluetoothDevice): The Bluetooth device to monitor.
        """
        while True:
            # Find the Pico object linked to this device
            pico = self.picos.get(device.address)

            # Update the Pico's state with the device's relay state
            if pico and device.relay_state is not None:
                pico.is_closed = device.relay_state
                print(f"Pico {pico.name}: Relay is {'Closed' if pico.is_closed else 'Open'}")
            
            # Wait for a second before checking again
            time.sleep(1)

    async def send_relay_command(self, address, state):
        """
        Send a command to open/close a device's relay.

        Parameters:
        - address (str): The address of the Bluetooth device.
        - state (bool): True to close the relay, False to open it.
        """
        print(f"Sending command to {address} to {'close' if state else 'open'} the relay.")
        device = next((d for d in self.devices if d.address == address), None)
        if device:
            async with device.lock:
                device.relay_state = state  # Set the state
                print(f"Relay state for {address} updated!")

    def get_picos(self):
        """
        Get all Pico objects.

        Returns:
        - dict: A dictionary mapping addresses to Pico objects.
        """
        return self.picos
