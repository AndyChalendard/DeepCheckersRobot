#include "motor.hpp"

Motor::Motor(DigitalOut & digitalOutDirection, DigitalOut & digitalOutStep, DigitalIn & digitalInHome, float homePosition, char diminution, unsigned char stepResolution) {
    outputDirection = &digitalOutDirection;
    outputStep = &digitalOutStep;
    inputHome = &digitalInHome;

    *outputDirection = 0;
    *outputStep = 0;

    posCurrent = 0;
    posWanted = 0;

    this->stepResolution = stepResolution;
    this->diminution = diminution;
    this->homePosition = homePosition;

    motorStateLow = MotorStateLow::init;

    tickerController.attach_us(callback(controllerExe, this), 100);
}

void Motor::controllerLow() {
    switch(motorStateLow){
        case MotorStateLow::init:
            motorSleep = 1;
            motorStateLow = MotorStateLow::pause;

        // break; for the timing we don't use break
        case MotorStateLow::pause:
            *outputStep = 0;

            if (posCurrent != posWanted) {
                motorSleep ++;
                if (motorSleep >= motorTimeDelay) {
                    // We define the direction of the rotation
                    *outputDirection = (posCurrent < posWanted);

                    motorStateLow = MotorStateLow::increment;
                }
            }

            break;
        case MotorStateLow::increment:
            // We increment or decrement the step
            *outputStep = 1;
            if (*outputDirection) posCurrent ++; else posCurrent--;
            
            motorStateLow = MotorStateLow::init;

            break;
        default:
            motorStateLow = MotorStateLow::init;
    }
}

void Motor::setPositionStep(int positionStep, int speed) {
    // define the speed
    setSpeed(speed);

    // Degres to steps
    this->posWanted = positionStep;
}

void Motor::setPosition(float position, int speed) {
    setPositionStep((int) (position * ((float) this->diminution) * ((float) stepResolution) * ((float) 200/360)), speed);
}

void Motor::setPositionWithDuration(float position, float duration) {
    int finalStep = (int) (position * ((float) this->diminution) * ((float) stepResolution) * ((float) 200/360));

    setPositionStep(finalStep, (int) (abs(finalStep-posCurrent) / duration));
}

void Motor::goHome() {
    // We search the home interruptor
    setPosition(360.0, 1000);

    // We wait for the event
    while (*inputHome == 1) {};

    // We stop the rotation of the engine
    posWanted = posCurrent;

    // We setup the current position
    posCurrent = (int) this->homePosition * stepResolution * this->diminution * 200/360;
    
    setPosition(0, 1400);
}