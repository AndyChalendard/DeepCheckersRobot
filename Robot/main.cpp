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
    while (btn != 0) {
        ThisThread::sleep_for(50);
    }

    serial.printf("Demarrage de la carte...\r\n");
    threadBlinkLed.start(callback(callBackBlink, &led1));

    serial.printf("Initialisation des variables...\r\n");
    // Moto theta1 -185
    Motor motorTheta1(motorTheta1Dir, motorTheta1Step, motorTheta1Home, 90, -185, 0, -185, 5, false, false);
    Motor motorTheta2(motorTheta2Dir, motorTheta2Step, motorTheta2Home, 90, -20, 90, 90, 5, false, true);
    Motor motorTheta3(motorTheta3Dir, motorTheta3Step, motorTheta3Home, -5, -160, -5, -5, 5, true, true);


    serial.printf("Initialisation des moteurs...\r\n");
    motorTheta2.goHome();
    motorTheta3.goHome();
    motorTheta1.goHome();

    magneticField = 1;

    SerialOrder serialOrder(serial, semaphoreSerialOrder);

    while(1) {
        sleep();
    }
}
