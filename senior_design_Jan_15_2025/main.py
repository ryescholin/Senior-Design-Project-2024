import time
from initial_values import setup_initial_values
from fault_detection import FaultDetection

def main():
    # Initialize the grid and breakers
    grid, breakers = setup_initial_values()

    # Create a fault detector
    fault_detector = FaultDetection(grid)

    # Simulated currents for testing
    test_currents_sequence = [
        200,  # Normal operation
        360 # faulty operation
    ]

    # Test each sequence of currents
    for i, current in enumerate(test_currents_sequence):
        print(f"\n--- Loop {i + 1}: Simulated Current {current} ---")
        fault_detector.detect_fault("Route 1", current, breakers)

        # Print the status of each breaker
        for breaker in breakers.values():
            print(breaker.status())

        # Pause to simulate time between checks
        time.sleep(1)

if __name__ == "__main__":
    main()