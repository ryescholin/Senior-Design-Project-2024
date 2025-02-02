import bluetooth_device as bd
import route as r

# Create breakers
c1 = bd.BluetoothDevice("c1", state=True)
c2 = bd.BluetoothDevice("c2", state=True)
b1 = bd.BluetoothDevice("b1", state=True)
b2 = bd.BluetoothDevice("b2", state=True)
k1 = bd.BluetoothDevice("k1", state=True)
k2 = bd.BluetoothDevice("k2", state=True)

# Create end breakers
cbend = bd.BluetoothDevice("cbend", state=False)
ckend = bd.BluetoothDevice("ckend", state=False)
bkend = bd.BluetoothDevice("bkend", state=False)

# Create routes
cherry = r.Route(
    fault_ranges=[600, 500, 100],
    breakers=[c1, c2],
    end_breakers=[cbend, ckend],
    alternative_power={
        "banana": cbend,
        "kiwi": ckend
    }
)

banana = r.Route(
    fault_ranges=[500, 400, 100],
    breakers=[b1, b2],
    end_breakers=[cbend, bkend],
    alternative_power={
        "cherry": cbend,
        "kiwi": bkend
    }
)

kiwi = r.Route(
    fault_ranges=[300, 200, 100],
    breakers=[k1, k2],
    end_breakers=[ckend, bkend],
    alternative_power={
        "cherry": ckend,
        "banana": bkend
    }
)

def run_test(test_name, assertions):
    print(f"\nRunning {test_name}:")
    for description, condition in assertions:
        if condition:
            print(f"SUCCESS: {description} assert passed")
        else:
            print(f"FAILED: {description} failed")

# Test 1: Fault between C2 and End Breakers on Cherry
def test_cherry_end_breakers_fault():
    cherry.current = 110  # Fault happens between C2 and end breakers
    cherry.handle_fault()
    return [
        ("cherry.faulty - Cherry should be marked as faulty", cherry.faulty),
        ("c2.perm_open - C2 should be permanently open due to fault", c2.perm_open),
        ("cbend.perm_open - CBend should be permanently open due to fault", cbend.perm_open),
        ("ckend.perm_open - CKend should be permanently open due to fault", ckend.perm_open),
    ]

# Test 2: Fault between K1 and K2
def test_kiwi_k1_k2_fault():
    kiwi.current = 250  # Fault happens between K1 and K2
    kiwi.handle_fault()
    return [
        ("kiwi.faulty - Kiwi should be marked as faulty", kiwi.faulty),
        ("k1.perm_open - K1 should be permanently open due to fault", k1.perm_open),
        ("k2.perm_open - K2 should be permanently open due to fault", k2.perm_open),
        ("ckend.state - CKend should remain open due to prior fault", not ckend.state),
        ("bkend.state - BKend should be closed due to alternative power", bkend.state),
    ]

# Run tests
run_test("Test 1: Fault between C2 and End Breakers on Cherry", test_cherry_end_breakers_fault())
run_test("Test 2: Fault between K1 and K2 on Kiwi", test_kiwi_k1_k2_fault())

p1 = bd.BluetoothDevice("p1", state=True)
p2 = bd.BluetoothDevice("p2", state=True)
pend = bd.BluetoothDevice("pend", state=False)

single_route_test = r.Route(
    fault_ranges=[600, 500, 100],
    breakers=[p1, p2],
    end_breakers=[pend],
    alternative_power={
        "power_line": pend,
    }
)

def test_single_route_power_line():
    single_route_test.current = 550  # Fault happens between P1 and P2
    single_route_test.handle_fault()
    return [
        ("single_route_test.faulty - Single route should be marked as faulty", single_route_test.faulty),
        ("p1.perm_open - P1 should be permanently open due to fault", p1.perm_open),
        ("p2.perm_open - P2 should be permanently open due to fault", p2.perm_open),
        ("pend.state - Pend should be closed due to power line assumption", pend.state),
    ]

# Run test for single route power line scenario
run_test("Test 3: Single Route with Power Line", test_single_route_power_line())