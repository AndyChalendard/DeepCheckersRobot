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

DigitalOut motorDir(PC_10);
DigitalOut motorStep(PC_12);

Semaphore semaphoreSerialOrder(0);

// Main
int main() {
    threadBlinkLed.start(callback(callBackBlink, &led1));

    Motor motor(motorDir, motorStep);

    serial.printf("Demarrage de la carte...\r\n");

    SerialOrder serialOrder(serial, semaphoreSerialOrder);
    //testMotor(serial, motor);
    //testFermeture(serial);
    testSerialOrder(serial, serialOrder);

    while(1) {
        sleep();
    }
}
