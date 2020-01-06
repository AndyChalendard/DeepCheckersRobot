#include "mbed.h"
#include "geoSpace.hpp"
#include "motor.hpp"
#include "serialOrder.hpp"

#include "test.hpp"

#define SPEED    100       // mm/s
#define DIV_TIME 300       // In ms

RawSerial serial(USBTX, USBRX, 9600);

Thread threadBlinkLed;
DigitalOut led1(LED1);

// Blink function toggles the led in a loop
void callBackBlink(DigitalOut *led) {
    while (1) {
        *led = 1;
        ThisThread::sleep_for(200);
        *led = 0;
        ThisThread::sleep_for(800);
    }
}

DigitalIn  btn(USER_BUTTON);

DigitalOut motorTheta1Dir(PA_13);
DigitalOut motorTheta1Step(PA_14);
DigitalIn  motorTheta1Home(PC_3);

DigitalOut motorTheta2Dir(PC_10);
DigitalOut motorTheta2Step(PC_12);
DigitalIn  motorTheta2Home(PC_2);

DigitalOut motorTheta3Dir(PA_15);
DigitalOut motorTheta3Step(PB_7);
DigitalIn  motorTheta3Home(PC_0);


DigitalOut magneticField(PC_1);

Semaphore semaphoreSerialOrder(0);


// Go to the pause position
void goPausePosition(Motor & m1, Motor & m2, Motor & m3) {
    float x,y,z;
    GeoSpace tmpSpace;

    tmpSpace.setCoord(-200, 0, 20);
    tmpSpace.getAngle(x, y, z);

    m1.setPosition(x);
    m2.setPosition(y);
    m3.setPosition(z, 1200);

    m1.waitUntilMove();
    m2.waitUntilMove();
    m3.waitUntilMove();
}

// Main
int main() {
    float normMove; // In mm
    long  tmpsMove; // In ms
    int   nbDivMove;
    float timeToDest; // In ms
    float truePosX, truePosY, truePosZ;
    float dirX, dirY, dirZ;
    float targetX, targetY, targetZ;

    float tmpFloat1, tmpFloat2, tmpFloat3;

    serial.printf("Starting...\r\n");

    serial.printf("Initialization of variables...\r\n");
    
    // Initialisation of led
    led1 = 1;

    // Init of magnetic hand
    magneticField = 0;

    // Init of motors
    Motor motorTheta1(motorTheta1Dir, motorTheta1Step, motorTheta1Home, 120, -185, -90, -185, 5, false, false);
    Motor motorTheta2(motorTheta2Dir, motorTheta2Step, motorTheta2Home, 90, -20, 90, 90, 5, false, true);
    Motor motorTheta3(motorTheta3Dir, motorTheta3Step, motorTheta3Home, -11, -155, -11, -11, 5, true, true);

    // Init of serial orders
    SerialOrder serialOrder(serial, semaphoreSerialOrder);

    // Init of geoSpace
    GeoSpace geoSpace;
    targetX = -200; targetY = 0; targetZ = 20; // pause position
    truePosX = -200; truePosY = 0; truePosZ = 20;
    geoSpace.setCoord(targetX, targetY, targetZ);

    targetX = 0; targetY = 300; targetZ = 100;

    // Waiting for button
    serial.printf("Waiting user...\r\n");
    while (btn != 0) {
        ThisThread::sleep_for(50);
    }

    serial.printf("Moving to origin...\r\n");
    motorTheta2.goHome();
    motorTheta3.goHome();
    motorTheta1.goHome();

    serial.printf("Moving to pause position...\r\n");
    goPausePosition(motorTheta1, motorTheta2, motorTheta3);

    // Waiting for button
    serial.printf("Waiting user...\r\n");
    while (btn != 0) {
        ThisThread::sleep_for(50);
    }

    threadBlinkLed.start(callback(callBackBlink, &led1));

    serial.printf("____loop____\r\n");

    while(1) {
        // Figure out the norm of the deplacement
        dirX = (targetX-truePosX);
        dirY = (targetY-truePosY);
        dirZ = (targetZ-truePosZ);
        normMove  = dirX*dirX;
        normMove += dirY*dirY;
        normMove += dirZ*dirZ;
        normMove = sqrt(normMove);

        // If the move is not null
        if (normMove > 1) {
            // Figure out the time to move to the target position
            tmpsMove = ((normMove / SPEED) * 1000) - 1;

            // Figure out the number of division
            nbDivMove = (tmpsMove / DIV_TIME) + 1;
            
            // Figure out the vector to add
            dirX = dirX / nbDivMove;
            dirY = dirY / nbDivMove;
            dirZ = dirZ / nbDivMove;

            // Figure out the new position (with a path ahead)
            truePosX += dirX;
            truePosY += dirY;
            truePosZ += dirZ;
            if (nbDivMove != 1) {
                tmpFloat1 = truePosX + dirX;
                tmpFloat2 = truePosY + dirY;
                tmpFloat3 = truePosZ + dirZ;
                timeToDest = DIV_TIME * 2;
            }else{
                tmpFloat1 = truePosX;
                tmpFloat2 = truePosY;
                tmpFloat3 = truePosZ;
                timeToDest = DIV_TIME;
            }
            serial.printf("dirX:%f, dirY:%f, dirZ:%f, norm: %f, tmpsMove: %i\n\r", dirX, dirY, dirZ, normMove, tmpsMove);
            serial.printf("truePosX: %f, truePosY: %f, truePosZ: %f\n\r", truePosX, truePosY, truePosZ);

            // Figure out the angle motor require
            geoSpace.setCoord(tmpFloat1, tmpFloat2, tmpFloat3);
            serial.printf("posX: %f, posY: %f, posZ: %f, timeToDest: %f\n\r", tmpFloat1, tmpFloat2, tmpFloat3, timeToDest);
            geoSpace.getAngle(tmpFloat1, tmpFloat2, tmpFloat3);

            // Send to motors the new angle, and the time to destination (two )
            motorTheta1.setPositionWithDuration(tmpFloat1, timeToDest/1000);
            motorTheta2.setPositionWithDuration(tmpFloat2, timeToDest/1000);
            motorTheta3.setPositionWithDuration(tmpFloat3, timeToDest/1000);
        }

        ThisThread::sleep_for(DIV_TIME);
    }
}
