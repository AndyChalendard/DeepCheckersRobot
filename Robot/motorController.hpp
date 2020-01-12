#ifndef __MOTOR_CONTROLLER_HPP__
#define __MOTOR_CONTROLLER_HPP__

#include "mbed.h"
#include "motor.hpp"
#include "geoSpace.hpp"

#define SPEED    100       // mm/s
#define DIV_TIME 400       // In ms

class MotorController {
    private:
        // Ticker for the controller
        Ticker tickerMove;

        // Thread for the figure out of the new position
        Thread threadFigureOut;

        // Motor controlled
        Motor * motorTheta1;
        Motor * motorTheta2;
        Motor * motorTheta3;

        // GeoSpace to figure out angle and position
        GeoSpace geoSpace;

        // Current target for the motors
        float motTheta1, motTheta2, motTheta3; // In mm
        float timeToDest; // In ms
        Semaphore motorAngleSended;

        // Target to go
        float targetX, targetY, targetZ; // In mm

        // Last position requested
        float truePosX, truePosY, truePosZ; // In mm

        // launcher for the positionCalculator
        static void positionCalculatorExe(MotorController * mot) {mot->positionCalculator();}
        // Figure out the new position for the motor
        void positionCalculator();

        // Launcher for the posMove
        static void posMoveExe(MotorController * mot) {mot->posMove();}
        // Send to the motor the new position and the new duration
        void posMove();

    public:
        // Constructor
        MotorController(Motor & motorTheta1, Motor & motorTheta2, Motor & motorTheta3) : motorTheta1(&motorTheta1), motorTheta2(&motorTheta2), motorTheta3(&motorTheta3) {
            motorTheta2.goOrigin();
            motorTheta3.goOrigin();
            motorTheta1.goOrigin();

            goPausePosition(false);

            motorAngleSended.release();

            tickerMove.attach_us(callback(posMoveExe, this), DIV_TIME*1000);
            threadFigureOut.start(callback(positionCalculatorExe, this));
        }

        // Wait for the mouvement to end
        void waitUntilMove();

        // Request to go to a position
        void go(float posX, float posY, float posZ);

        // request to go to the pause position
        void goPausePosition(bool withControlledTrajectory = true);
};

#endif // __MOTOR_CONTROLLER_HPP__
