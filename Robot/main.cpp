#include "mbed.h"
#include "geoSpace.hpp"
#include "motor.hpp"
#include "serialOrder.hpp"

#include "test.hpp"

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

// Main
int main() {
    float tmpFloat1, tmpFloat2, tmpFloat3;

    serial.printf("Starting...\r\n");

    serial.printf("Initialization of variables...\r\n");
    
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
    geoSpace.setCoord(-200, 0, 20); // pause position

    // Waiting for button
    while (btn != 0) {
        ThisThread::sleep_for(50);
    }
    
    threadBlinkLed.start(callback(callBackBlink, &led1));

    serial.printf("Mouving to origin...\r\n");
    motorTheta2.goHome();
    motorTheta3.goHome();
    motorTheta1.goHome();

    int i = 0;
    int j = 0;

    int time = 10000;

    while(1) {
        geoSpace.getAngle(tmpFloat1, tmpFloat2, tmpFloat3);

        //serial.printf("Moving to x:%f y:%f z:%f; t1:%f t2:%f t3:%f !\r\n", -30.0f,190.0f,5.0f, tmpFloat1, tmpFloat2, tmpFloat3);
        motorTheta1.setPosition(tmpFloat1);
        motorTheta2.setPosition(tmpFloat2);
        motorTheta3.setPosition(tmpFloat3);

        ThisThread::sleep_for(time);

        switch(i) {
            case 0:
                magneticField = 0;
                geoSpace.setCoord(30, 190, 20);
                time = 15000;
                break;
            case 1:
                magneticField = 0;
                geoSpace.setCoord(30, 190, 6);
                time = 3000;
                break;
            case 2:
                magneticField = 1;
                geoSpace.setCoord(30, 190, 20);
                time = 3000;
                break;
            case 3:
                magneticField = 1;
                geoSpace.setCoord(-30, 190, 20);
                time = 3000;
                break;
            case 4:
                magneticField = 1;
                geoSpace.setCoord(-30, 190, 6);
                time = 3000;
                break;
            case 5:
                magneticField = 0;
                geoSpace.setCoord(-30, 190, 20);
                time = 3000;
                break;
            case 6:
                magneticField = 0;
                geoSpace.setCoord(30, 130, 20);
                time = 5000;
                break;
            case 7:
                magneticField = 0;
                geoSpace.setCoord(30, 130, 6);
                time = 3000;
                break;
            case 8:
                magneticField = 1;
                geoSpace.setCoord(30, 130, 20);
                time = 3000;
                break;
            case 9:
                magneticField = 1;
                geoSpace.setCoord(30, 190, 20);
                time = 3000;
                break;
            case 10:
                magneticField = 1;
                geoSpace.setCoord(30, 190, 6);
                time = 3000;
                break;
            case 11:
                magneticField = 0;
                geoSpace.setCoord(30, 190, 20);
                time = 3000;
                break;
            case 12:
                magneticField = 0;
                geoSpace.setCoord(-30, 130, 20);
                time = 5000;
                break;
            case 13:
                magneticField = 0;
                geoSpace.setCoord(-30, 130, 6);
                time = 3000;
                break;
            case 14:
                magneticField = 1;
                geoSpace.setCoord(-30, 130, 20);
                time = 3000;
                break;
            case 15:
                magneticField = 1;
                geoSpace.setCoord(30, 130, 20);
                time = 3000;
                break;
            case 16:
                magneticField = 1;
                geoSpace.setCoord(30, 130, 6);
                time = 3000;
                break;
            case 17:
                magneticField = 0;
                geoSpace.setCoord(30, 130, 20);
                time = 3000;
                break;
            case 18:
                magneticField = 0;
                geoSpace.setCoord(-30, 190,20);
                time = 5000;
                break;
            case 19:
                magneticField = 0;
                geoSpace.setCoord(-30, 190, 6);
                time = 3000;
                break;
            case 20:
                magneticField = 1;
                geoSpace.setCoord(-30, 190, 20);
                time = 3000;
                break;
            case 21:
                magneticField = 1;
                geoSpace.setCoord(-30, 130, 20);
                time = 3000;
                break;
            case 22:
                magneticField = 1;
                geoSpace.setCoord(-30, 130, 6);
                time = 3000;
                break;
            case 23:
                magneticField = 0;
                geoSpace.setCoord(-30, 130, 20);
                time = 3000;
                break;
            default:
                time = 1;
                i = -1;
        }

        i++;

        sleep();
    }
}
