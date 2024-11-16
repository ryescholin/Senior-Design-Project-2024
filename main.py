import time
from initial_values import setup_initial_values
from fault_detection import FaultDetection

def main():
    grid = setup_initial_values()
    fault_detector = FaultDetection(grid)

    route_values_sequence = [
        {"Route 1": 100},
        {"Route 1": 200},   
        {"Route 1": 300},    
        {"Route 1": 300},  
        {"Route 1": 300},   
        {"Route 1": 300}     
    ]

    for count, route_values in enumerate(route_values_sequence):
        print(f"\n--- Loop {count + 1} ---")
        faults = fault_detector.detect_fault(route_values)
        if "No Fault" in faults:
            print("No faults detected.")
        else:
            print("Faults detected on lines:", faults)
        
        # Print route status after fault detection and rerouting
        grid.verify_power_restoration()
        time.sleep(1)

if __name__ == "__main__":
    main()
