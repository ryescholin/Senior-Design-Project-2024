#include <iostream>

using namespace std;

class RouteManagement {
private:
    bool breakerAB;
    bool breakerEnd;
    bool breakerCD;

public:
    RouteManagement() : breakerAB(true), breakerEnd(false), breakerCD(true) {}

    void handleFaultAB() {
        breakerAB = false;
        breakerEnd = true;
    }

    bool isBreakerABClosed() const { return breakerAB; }
    bool isBreakerEndClosed() const { return breakerEnd; }
    bool isBreakerCDClosed() const { return breakerCD; }

    void printBreakerStatus() const {
        cout << "Breaker AB: " << (breakerAB ? "Closed" : "Open") << endl;
        cout << "End Segment Breaker: " << (breakerEnd ? "Closed" : "Open") << endl;
        cout << "Breaker CD: " << (breakerCD ? "Closed" : "Open") << endl;
    }
};
