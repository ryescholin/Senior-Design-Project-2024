from bluetooth_converter import BluetoothConverter
import asyncio


class BluetoothManager:
    """
    Manages Bluetooth devices and integrates them into the grid logic.
    """

    def __init__(self, addresses, fault_limits):
        """
        Sets up the BluetoothManager.

        Parameters:
        - addresses (list): List of Bluetooth device addresses.
        - fault_limits (dict): A dictionary of fault limits for each device.
        """
        self.converter = BluetoothConverter(addresses, fault_limits)  # Use BluetoothConverter

    async def connect_all_devices(self):
        """
        Connect all devices through the converter.
        """
        await self.converter.connect_devices()  # Connect devices

    def start_monitoring(self):
        """
        Start monitoring all devices for updates.
        """
        self.converter.start_monitoring_threads()

    async def send_command(self, address, state):
        """
        Send a command to a specific device.

        Parameters:
        - address (str): The address of the Bluetooth device.
        - state (bool): True to close the relay, False to open it.
        """
        await self.converter.send_relay_command(address, state)

    def get_picos(self):
        """
        Get all Pico objects.

        Returns:
        - dict: Address-to-Pico mapping.
        """
        return self.converter.get_picos()
