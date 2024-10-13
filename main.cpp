#include "pi_control.cpp"
#include <iostream>
using namespace std;


int main() {
    Pico picoA("A", 150), picoB("B", 100), picoC("C", 200), picoD("D", 50);

    RaspberryPi pi(&picoA, &picoB, &picoC, &picoD, 250, 250);

    for (int i = 1; i <= 10; i++) {
        cout << "Iteration: " << i << endl;

        pi.autoAdjustPowerFlow(i);
        pi.printAllStatus();

        cout << "--------------------------------" << endl;
    }

    return 0;
}
