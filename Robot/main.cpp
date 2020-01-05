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

DigitalOut motorTheta1Dir(PA_13);
DigitalOut motorTheta1Step(PA_14);
DigitalIn  motorTheta1Home(PC_3);

DigitalOut motorTheta2Dir(PC_10);
DigitalOut motorTheta2Step(PC_12);
DigitalIn  motorTheta2Home(PC_2);

DigitalOut motorTheta3Dir(PA_15);
DigitalOut motorTheta3Step(PB_7);
DigitalIn  motorTheta3Home(PC_0);


DigitalOut MagneticField(PB_8);

Semaphore semaphoreSerialOrder(0);

// Main
int main() {
    threadBlinkLed.start(callback(callBackBlink, &led1));

    serial.printf("Demarrage de la carte...\r\n");

    serial.printf("Initialisation des variables...\r\n");
    // Moto theta1 -185
    Motor motorTheta2(motorTheta2Dir, motorTheta2Step, motorTheta2Home, 90, 0, 5);
    //Motor motorTheta3(motorTheta3Dir, motorTheta3Step, motorTheta3Home, 0, 0, 5);


    serial.printf("Initialisation des moteurs...\r\n");
    motorTheta2.goHome();

    SerialOrder serialOrder(serial, semaphoreSerialOrder);

    while(1) {
        sleep();
    }
}
