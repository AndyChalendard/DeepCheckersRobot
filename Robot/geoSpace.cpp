#include "geoSpace.hpp"
#include <math.h>

// Angle params must be in degres
void GeoSpace::setAngle(float theta1, float theta2, float theta3) {
    coordIsCalc = false;
    thetaIsCalc = true;

    this->theta1 = theta1;
    plane.setAngle(theta2, theta3);
}

void GeoSpace::setCoord(float x, float y, float z) {
    coordIsCalc = true;
    thetaIsCalc = false;

    this->x = x;
    this->y = y;
    this->z = z;

    plane.setCoord( std::sqrt(x*x+y*y), z);
}

// Angle params is return in degres
void GeoSpace::getAngle(float & theta1, float & theta2, float & theta3) {
    if (thetaIsCalc == false) {
        this->theta1 = atan2(this->x, this->y) * 180/3.14159;

        thetaIsCalc = true;
    }

    theta1 = this->theta1;
    plane.getAngle(theta2, theta3);
}


void GeoSpace::getCoord(float & x, float & y, float & z) {
    float norm;

    if (coordIsCalc == false) {
        plane.getCoord(norm, this->z);

        this->x = norm * sin(this->theta1*3.14159/180);
        this->y = norm * cos(this->theta1*3.14159/180);

        coordIsCalc = true;
    }

    x = this->x;
    y = this->y;
    z = this->z;
}