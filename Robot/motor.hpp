#ifndef __MOTEUR_HPP__
#define __MOTEUR_HPP__

#include "mbed.h"

class Motor {
    private:
        // Motor state
        bool isActivate;
        int posCurrent;
        int posWanted;

        unsigned int speed; // Steps per seconde

        // Motor configuration
        DigitalOut * outputDirection;
        DigitalOut * outputStep;

        // Thread of state machine
        Thread threadController;

        // state machine
        void controller();

        // Launcher of state machine
        static void controllerExe(Motor * mot) {mot->controller();}

    public:

        // Constructor
        Motor(DigitalOut & digitalOutDirection, DigitalOut & digitalOutStep);

        // Destructor
        ~Motor() {isActivate = false; threadController.join();}

        // Setters
        void setPosition(int position);
        
};

#endif
