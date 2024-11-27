import asyncio
from bluetooth_manager import BluetoothManager


async def main():
    # List of device addresses
    addresses = ["28:CD:C1:0E:C3:D6", "28:CD:C1:0E:C3:D7"]

    # Fault limits for each device
    fault_limits = {
        "28:CD:C1:0E:C3:D6": 400,
        "28:CD:C1:0E:C3:D7": 350,
        "28:CD:C1:11:40:ZE": 300,
        "28:CD:C1:11:DF:B8": 250
    }

    # Create a BluetoothManager
    manager = BluetoothManager(addresses, fault_limits)

    # Step 1: Connect all devices
    await manager.connect_all_devices()

    # Step 2: Start monitoring devices
    manager.start_monitoring()

    # Step 3: Send commands to devices
    print("Sending commands to devices...")
    for address in addresses:
        await manager.send_command(address, True)  # Close relay
        await asyncio.sleep(2)  # Wait for 2 seconds
        await manager.send_command(address, False)  # Open relay
        await asyncio.sleep(2)

    # Step 4: Get Pico objects
    picos = manager.get_picos()
    for address, pico in picos.items():
        print(f"Pico {pico.name}: Relay is {'Closed' if pico.is_closed else 'Open'}")

if __name__ == "__main__":
    asyncio.run(main())
