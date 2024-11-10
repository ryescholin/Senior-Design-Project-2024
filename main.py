import time
from initial_values import setup_initial_values
from fault_detection import FaultDetection

def main():
    grid = setup_initial_values()
    fault_detector = FaultDetection(grid)

    route_values_sequence = [
        {"Route 1": 300, "Route 2": 300},    # Loop 1: No faults
        {"Route 1": 300, "Route 2": 300},    # Loop 2: No faults
        {"Route 1": 800, "Route 2": 300},    # Loop 3: Fault on 11-12, triggers rerouting
        {"Route 1": 300, "Route 2": 300},    # Loop 4: No new faults
        {"Route 1": 300, "Route 2": 800},    # Loop 5: Fault on 21-22, triggers rerouting
        {"Route 1": 300, "Route 2": 300}     # Loop 6: No new faults
    ]

    for count, route_values in enumerate(route_values_sequence):
        print(f"\n--- Loop {count + 1} ---")
        faults = fault_detector.detect_fault(route_values)
        if "No Fault" in faults:
            print("No faults detected.")
        else:
            print("Faults detected on lines:", faults)
        
        # Print detailed route status after fault detection and rerouting
        grid.verify_power_restoration()
        time.sleep(1)

if __name__ == "__main__":
    main()
