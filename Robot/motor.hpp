#ifndef __MOTEUR_HPP__
#define __MOTEUR_HPP__

#include "mbed.h"

class Motor {
    private:
        // A4988 configuration
        unsigned char stepResolution;
        char diminution;

        // Motor state
        enum class MotorStateLow {
            init,
            pause,
            increment
        } motorStateLow;
        unsigned int motorSleep;

        int posCurrent;
        int posWanted;

        unsigned int motorTimeDelay; // number of 100µs per step

        // Motor configuration
        DigitalOut * outputDirection;
        DigitalOut * outputStep;
        DigitalIn  * inputHome;

        float homePosition;
        float interruptorPosition;

        // Ticker of state machine
        LowPowerTicker tickerController;

        // state machine for low level
        void controllerLow();

        // Launcher of state machine
        static void controllerExe(Motor * mot) {mot->controllerLow();}

        // Define the speed, the maximum speed is 5000
        void setSpeed(int speed) {if (speed < 5000) motorTimeDelay = 10000/speed; else motorTimeDelay = 2;}

        // Define the position in step and the speed in step/s
        void setPositionStep(int positionStep, int speed);
    public:

        // Constructor
        Motor(DigitalOut & digitalOutDirection, DigitalOut & digitalOutStep, DigitalIn & digitalInHome, float homePosition, float interruptorPosition, char diminution, unsigned char stepResolution = 16);

        // Destructor
        ~Motor() {tickerController.detach();}

        // Setters
        // Define the motor position wanted
        // Position is in degres, speed in steps per seconde, duration in seconde
        void setPosition(float position, int speed = 16*25);
        void setPositionWithDuration(float position, float duration);

        // Take home
        void goHome();
};

#endif
