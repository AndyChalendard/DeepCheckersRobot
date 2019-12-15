#ifndef __GEOSPACE_HPP__
#define __GEOSPACE_HPP__

#include "geoPlane.hpp"

class GeoSpace {
    private:
        GeoPlane plane; // This plane is oriented about the main axis and the hand of the robot

        bool thetaIsCalc;
        float theta1;
        bool coordIsCalc;
        float x, y, z;

    public:
        // GeoSpace constructor
        GeoSpace() : thetaIsCalc(false), theta1(0), coordIsCalc(false), x(0), y(0) {}

        // Setters
        void setAngle(float theta1, float theta2, float theta3);
        void setCoord(float x, float y, float z);

        // Getters
        void getAngle(float & theta1, float & theta2, float & theta3); // We know the position
        void getCoord(float & x, float & y, float & z); // We know the angle
};

#endif // __GEOSPACE_HPP__
