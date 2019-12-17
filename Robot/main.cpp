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

DigitalOut MotorDir(PC_10);
DigitalOut MotorStep(PC_12);

// Main
int main() {
    threadBlinkLed.start(callback(callBackBlink, &led1));

    //Motor motor(MotorDir, MotorStep);

    serial.printf("Demarrage de la carte...\r\n");

    SerialOrder serialOrder(serial);
    //testMotor(serial, motor);
    //testFermeture(serial);

    while(1) {
        sleep();
    }
}
