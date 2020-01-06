#include "motor.hpp"

Motor::Motor(DigitalOut & digitalOutDirection, DigitalOut & digitalOutStep, DigitalIn & digitalInHome, float maxPosition, float minPosition, float homePosition, float interruptorPosition, char diminution, bool motorReversed, bool homePosSide, unsigned char stepResolution) {
    outputDirection = &digitalOutDirection;
    outputStep = &digitalOutStep;
    inputHome = &digitalInHome;

    *outputDirection = 0;
    *outputStep = 0;

    posCurrent = 0;
    posWanted = 0;

    this->minPosition = minPosition;
    this->maxPosition = maxPosition;

    this->motorReversed = motorReversed;

    this->stepResolution = stepResolution;
    this->diminution = diminution;
    this->homePosSide = homePosSide;
    this->homePosition = homePosition;
    this->interruptorPosition = interruptorPosition;

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

int Motor::getStep(float position, bool withSecurity) {
    int result;

    if (withSecurity) {
        if (position > maxPosition) {
            position = maxPosition;
        }else if (position < minPosition){
            position = minPosition;
        }
    }

    result = (int) (position * ((float) this->diminution) * ((float) stepResolution) * ((float) 200/360));

    if (this->motorReversed) {
        result = -result;
    }

    return result;
}

void Motor::setPositionStep(int positionStep, int speed) {
    // define the speed
    setSpeed(speed);

    // Degres to steps
    this->posWanted = positionStep;
}

void Motor::setPosition(float position, int speed, bool withSecurity) {
    setPositionStep(getStep(position, withSecurity), speed);
}

void Motor::setPositionWithDuration(float position, float duration, bool withSecurity) {
    int finalStep = getStep(position, withSecurity);

    setPositionStep(finalStep, (int) abs(finalStep - posCurrent)/duration);
}

void Motor::goHome() {
    // We search the home interruptor
    if (this->homePosSide) {
        setPosition(360.0, 1000, false);
    }else{
        setPosition(-360.0, 1000, false);
    }

    // We wait for the event
    while (*inputHome == 1) {};

    // We stop the rotation of the engine
    posWanted = posCurrent;

    // We setup the current position
    this->posCurrent = getStep(this->interruptorPosition, false);
    setPosition(this->homePosition, 1400);

    waitUntilMove();
}

void Motor::waitUntilMove() {
    while (posCurrent != posWanted) {
        ThisThread::sleep_for(50);
    }
}