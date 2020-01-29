#include "mbed.h"
#include "geoSpace.hpp"
#include "motor.hpp"
#include "motorController.hpp"
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

// Main
int main() {
    float tmpFloat1, tmpFloat2, tmpFloat3;
    bool tmpBool;


    // Init of serial orders
    SerialOrder serialOrder(serial);

    serial.printf("Starting...\n");

    threadBlinkLed.start(callback(callBackBlink, &led1));

    serial.printf("Initialization of variables...\n");

    // Init of magnetic hand
    magneticField = 0;

    // Init of motors
    Motor motorTheta1(motorTheta1Dir, motorTheta1Step, motorTheta1Home, 120, -185, -90, -185, 5, false, false);
    Motor motorTheta2(motorTheta2Dir, motorTheta2Step, motorTheta2Home, 90, -20, 90, 90, 5, false, true);
    Motor motorTheta3(motorTheta3Dir, motorTheta3Step, motorTheta3Home, -11, -146, -11, -11, 5, true, true);
    
    // Waiting for button
    serial.printf("Waiting user...\n");
    while (btn != 0) {
        ThisThread::sleep_for(50);
    }

    // We load the motor controller
    serial.printf("Moving to origin and to pause position...\n");
    MotorController motorController(motorTheta1, motorTheta2, motorTheta3);

    ThisThread::sleep_for(8000);

    serial.printf("#READY;\n");
    while(1) {
        if (serialOrder.requestPosition.getPosTry(tmpFloat1, tmpFloat2, tmpFloat3)) {
            serial.printf("I go to the position: %f %f %f\n", tmpFloat1, tmpFloat2, tmpFloat3);
            motorController.go(tmpFloat1, tmpFloat2, tmpFloat3);

            motorController.waitUntilMove();
            serial.printf("#POS_OK;\n");
        }

        if (serialOrder.requestMagnetic.getStateTry(tmpBool)) {
            magneticField = tmpBool;
        }

        ThisThread::sleep_for(100);
    }
}
