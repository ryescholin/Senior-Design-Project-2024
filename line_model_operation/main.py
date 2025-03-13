import asyncio
import bluetooth_device as bd
import route as r

async def main():
    lock = asyncio.Lock()  # Shared lock for all Bluetooth devices

    # Create breakers
    c1 = bd.BluetoothDevice("c1", "28:CD:C1:11:90:2E", state=True)
    c2 = bd.BluetoothDevice("c2", "28:CD:C1:11:90:2E", state=True)
    c3 = bd.BluetoothDevice("c3", "28:CD:C1:11:90:2E", state=True)
    b1 = bd.BluetoothDevice("b1", "28:CD:C1:11:90:2E", state=True)
    b2 = bd.BluetoothDevice("b2", "28:CD:C1:11:90:2E", state=True)
    b3 = bd.BluetoothDevice("b3", "28:CD:C1:11:90:2E", state=True)
    k1 = bd.BluetoothDevice("k1", "28:CD:C1:11:90:2E", state=True)
    k2 = bd.BluetoothDevice("k2", "28:CD:C1:11:90:2E", state=True)
    k3 = bd.BluetoothDevice("k3", "28:CD:C1:11:90:2E", state=True)

    # Create end breakers
    cbend = bd.BluetoothDevice("cbend", "28:CD:C1:11:90:2E", state=False)
    ckend = bd.BluetoothDevice("ckend", "28:CD:C1:11:90:2E", state=False)
    bkend = bd.BluetoothDevice("bkend", "28:CD:C1:11:90:2E", state=False)

    # Create routes
    cherry = r.Route(
        fault_ranges=[400, 343, 300, 267],
        breakers=[c1, c2, c3],
        end_breakers=[cbend, ckend],
        alternative_power={
            "banana": cbend,
            "kiwi": ckend
        }
    )

    banana = r.Route(
        fault_ranges=[400, 343, 300, 267],
        breakers=[b1, b2, b3],
        end_breakers=[cbend, bkend],
        alternative_power={
            "cherry": cbend,
            "kiwi": bkend
        }
    )

    kiwi = r.Route(
        fault_ranges=[400, 343, 300, 267],
        breakers=[k1, k2, k3],
        end_breakers=[ckend, bkend],
        alternative_power={
            "cherry": ckend,
            "banana": bkend
        }
    )

    # Start Bluetooth connections asynchronously
    device_tasks = [
        asyncio.create_task(device.open_connection(lock))
        for device in [c1, c2, c3, b1, b2, b3, k1, k2, k3, cbend, ckend, bkend]
    ]

    # Run initialization
    await cherry.initialize()

    # Run tests
    def run_test(test_name, assertions):
        print(f"\nRunning {test_name}:")
        for description, condition in assertions:
            if condition:
                print(f"SUCCESS: {description} assert passed")
            else:
                print(f"FAILED: {description} failed")

    def test_cherry_end_breakers_fault():
        cherry.current = 0.3  # Fault between C2 and end breakers
        cherry.handle_fault()
        return [
            ("cherry.faulty", cherry.faulty),
            ("c2.perm_open", c2.perm_open),
            ("cbend.perm_open", cbend.perm_open),
            ("ckend.perm_open", ckend.perm_open),
        ]

    def test_kiwi_k1_k2_fault():
        kiwi.current = 0.7  # Fault between K1 and K2
        kiwi.handle_fault()
        return [
            ("kiwi.faulty", kiwi.faulty),
            ("k1.perm_open", k1.perm_open),
            ("k2.perm_open", k2.perm_open),
            ("ckend.state", not ckend.state),
            ("bkend.state", bkend.state),
        ]

    run_test("Test 1: Fault between C2 and End Breakers on Cherry", test_cherry_end_breakers_fault())
    run_test("Test 2: Fault between K1 and K2 on Kiwi", test_kiwi_k1_k2_fault())

    # Await all Bluetooth tasks before exiting
    await asyncio.gather(*device_tasks)

if __name__ == "__main__":
    asyncio.run(main())
