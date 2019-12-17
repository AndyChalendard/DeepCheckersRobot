#ifndef __TEST_HPP__
#define __TEST_HPP__

#define TEST_LIB

#ifdef TEST_LIB

#include "mbed.h"

#include "motor.hpp"
void testMotor(Serial & serial, Motor & motor);

void testFermeture(Serial & serial);

#endif // TEST_LIB
#endif // __TEST_HPP__
