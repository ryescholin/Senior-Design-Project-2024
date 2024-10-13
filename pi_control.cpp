#include "pico_control.cpp"
#include "route_management.cpp"
#include "power_management.cpp"
#include <iostream>

using namespace std;

class RaspberryPi {
private:
    Pico* picos[4];
    RouteManagement routeManager;
    PowerManagement powerManager;

public:
    RaspberryPi(Pico* p1, Pico* p2, Pico* p3, Pico* p4, float supply1, float supply2) 
        : routeManager(), powerManager(supply1, supply2) {
        picos[0] = p1;
        picos[1] = p2;
        picos[2] = p3;
        picos[3] = p4;
    }

    // Auto-adjust
    void autoAdjustPowerFlow(int iteration) {
        bool faultDetected = false;

        if (routeManager.isBreakerABClosed()) {
            picos[0]->setCurrentReceived(powerManager.piSupplyRoute1);
            picos[0]->calculatePassing(picos[1]->getCurrentDemand());
            float currentToPass = picos[0]->getCurrentPassing();

            if (iteration == 3) {
                currentToPass += 10;
                cout << "Adding 10A between A and B in iteration 3." << endl;
            }

            picos[1]->setCurrentReceived(currentToPass);

            if (picos[1]->checkForFault(picos[0]->getCurrentPassing())) {
                faultDetected = true;
            }
        }

        picos[2]->setCurrentReceived(powerManager.piSupplyRoute2);
        picos[2]->calculatePassing(picos[3]->getCurrentDemand());
        picos[3]->setCurrentReceived(picos[2]->getCurrentPassing());

        if (faultDetected) {
            routeManager.handleFaultAB();
            powerManager.reroutePowerFlow();
        }
    }

    // Distribute power
    void distributePower() {
        picos[0]->setCurrentReceived(powerManager.piSupplyRoute1);

        if (!routeManager.isBreakerABClosed() && routeManager.isBreakerEndClosed()) {
            picos[2]->setCurrentReceived(powerManager.piSupplyRoute2);
            picos[2]->calculatePassing(picos[3]->getCurrentDemand() + picos[1]->getCurrentDemand());
            picos[3]->setCurrentReceived(picos[2]->getCurrentPassing());
            picos[3]->calculatePassing(picos[1]->getCurrentDemand());
            picos[1]->setCurrentReceived(picos[3]->getCurrentPassing());
        }
    }

    // Print all status
    void printAllStatus() const {
        routeManager.printBreakerStatus();
        powerManager.printPowerFlow();

        for (int i = 0; i < 4; i++) {
            picos[i]->printStatus();
        }
    }
};
