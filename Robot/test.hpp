#ifndef __TEST_HPP__
#define __TEST_HPP__

#define TEST_LIB

#ifdef TEST_LIB

#include "mbed.h"


#include "serialOrder.hpp"
void testSerialOrder(RawSerial & serial, SerialOrder & serialOrder);

#include "motor.hpp"
void testMotor(RawSerial & serial, Motor & motor);

void testFermeture(RawSerial & serial);

#endif // TEST_LIB
#endif // __TEST_HPP__
