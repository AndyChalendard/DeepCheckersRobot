#include "motor.hpp"

Motor::Motor(DigitalOut & digitalOutDirection, DigitalOut & digitalOutStep) {
    outputDirection = &digitalOutDirection;
    outputStep = &digitalOutStep;

    *outputDirection = 0;
    *outputStep = 0;

    posCurrent = 0;
    posWanted = 0;

    speed = 200;

    isActivate = true;
}

void Motor::controller() {
    while (isActivate) {

        // We define the direction of the rotation
        *outputDirection = (posCurrent < posWanted);


        if (posCurrent != posWanted) {
            *outputStep = 1;

            if (*outputDirection) posCurrent ++; else posCurrent--;
        }
        ThisThread::sleep_for(500/speed);


        *outputStep = 0;
        ThisThread::sleep_for(500/speed);
    }
}

void Motor::setPosition(int position) {
    this->posWanted = position;

    threadController.start(callback(controllerExe, this));
}
