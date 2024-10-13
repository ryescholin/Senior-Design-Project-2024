#include <iostream>
using namespace std;


class Pico {
private:
    float currentDemand;
    float currentReceived;
    float currentPassing;
    string name;

public:
    Pico(string picoName, float demand) : name(picoName), currentDemand(demand), currentReceived(0), currentPassing(0) {}

    float getCurrentDemand() const { return currentDemand; }
    float getCurrentReceived() const { return currentReceived; }
    float getCurrentPassing() const { return currentPassing; }

    void setCurrentReceived(float curr) { currentReceived = curr; }
    void setCurrentPassing(float curr) { currentPassing = curr; }

    void calculatePassing(float remainingRouteDemand) {
        currentPassing = (currentReceived > currentDemand) ? (currentReceived - currentDemand) : 0;
    }

    bool checkForFault(float expectedCurrent) {
        if (currentReceived != expectedCurrent) {
            cout << "Fault detected at Pico " << name << "! Expected: " << expectedCurrent << "A, but received: " << currentReceived << "A" << endl;
            return true;
        }
        return false;
    }

    void printStatus() const {
        cout << "Pico " << name << " - Wants: " << currentDemand << "A, Received: " << currentReceived << "A, Passing: " << currentPassing << "A" << endl;
    }
};
