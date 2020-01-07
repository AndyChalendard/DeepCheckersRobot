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

Semaphore semaphoreSerialOrder(0);

// Main
int main() {
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
    
    // Waiting for button
    serial.printf("Waiting user...\r\n");
    while (btn != 0) {
        ThisThread::sleep_for(50);
    }

    // We load the motor controller
    serial.printf("Moving to origin and to pause position...\r\n");
    MotorController motorController(serial, motorTheta1, motorTheta2, motorTheta3);

    // Waiting for button
    serial.printf("Waiting user...\r\n");
    while (btn != 0) {
        ThisThread::sleep_for(50);
    }

    motorController.go(0, 300, 100);

    threadBlinkLed.start(callback(callBackBlink, &led1));

    serial.printf("____loop____\r\n");
    while(1) {
        sleep();
    }
}
