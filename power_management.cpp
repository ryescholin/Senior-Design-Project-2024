#include <iostream>

using namespace std;

class PowerManagement {
public:
    float piSupplyRoute1;
    float piSupplyRoute2;

    PowerManagement(float supply1, float supply2) : piSupplyRoute1(supply1), piSupplyRoute2(supply2) {}

    void normalPowerFlow() {
        piSupplyRoute1 = 250;
        piSupplyRoute2 = 250;
    }

    void reroutePowerFlow() {
        piSupplyRoute1 = 150;
        piSupplyRoute2 = 350;
    }

    void printPowerFlow() const {
        cout << "Pi supplying to Route 1 (A): " << piSupplyRoute1 << "A" << endl;
        cout << "Pi supplying to Route 2 (C and D): " << piSupplyRoute2 << "A" << endl;
    }
};
