#ifndef __MOTEUR_HPP__
#define __MOTEUR_HPP__

#include "mbed.h"

class Motor {
    private:
        // A4988 configuration
        unsigned char stepResolution;

        // Motor state
        enum class MotorStateLow {
            init,
            pause,
            increment
        } motorStateLow;
        unsigned int motorSleep;

        /*enum class MotorState {
            init,
            paused,
            acceleration,
            constant,
            deceleration
        } motorState;*/

        int posCurrent;
        int posWanted;

        unsigned int motorTimeDelay; // number of 100µs per step 
        unsigned int speed; // Steps per seconde

        // Motor configuration
        DigitalOut * outputDirection;
        DigitalOut * outputStep;

        // Ticker of state machine
        LowPowerTicker tickerController;

        // state machine for low level
        void controllerLow();

        // Launcher of state machine
        static void controllerExe(Motor * mot) {mot->controllerLow();}

        // Define the speed, the maximum speed is 5000
        void setSpeed(int speed) {if (speed <= 5000) motorTimeDelay = 10000/speed; else motorTimeDelay = 2;}

    public:

        // Constructor
        Motor(DigitalOut & digitalOutDirection, DigitalOut & digitalOutStep, unsigned char stepResolution = 16);

        // Destructor
        ~Motor() {tickerController.detach();}

        // Setters
        // Define the motor position wanted
        // Position is in degres
        void setPosition(float position);
};

#endif