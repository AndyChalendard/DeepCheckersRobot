#include "geoPlane.hpp"
#include <math.h>

#define VAL_A 170   // Pillar Height
#define VAL_B 160   // Back Arm Length
#define VAL_C 285   // Front Arm Length
#define VAL_D 34    // Hand Height

#define POSITION_ACCURACY 0.5f    // l value accurancy

void GeoPlane::setAngle(float theta1, float theta2) {
    thetaIsCalc = true;
    coordIsCalc = false;

    this->theta1 = theta1*3.14159/180;
    this->theta2 = theta2*3.14159/180;
}

void GeoPlane::setCoord(float l, float h) {
    thetaIsCalc = false;
    coordIsCalc = true;

    this->l = l;
    this->h = h;
}

// Return true if the sign is different
bool compareSign(float A, float B) {
    if (A >= 0) {
        return (B<0);
    }else{
        return (B>=0);
    }
}

// X value in radian
// return true if the final value is found
// return false if the final value is not found (interval should be reduced)
bool GeoPlane::searchTheta1(bool withL, float & xStart, float & xEnd, float yTarget, float theta2, float & accuracy) {
    float yTmp, xTmp;
    float errPrec, err;
    bool xStartIsTaken = false;
    bool xEndIsTaken = false;
    float tmpXStart = xStart;
    float tmpXEnd = xEnd;

    xTmp = tmpXStart;
    if (withL) {
        yTmp = calcCoordOfL(tmpXStart-accuracy, theta2);
    }else{
        yTmp = calcCoordOfH(tmpXStart-accuracy, theta2);
    }

    errPrec = yTmp - yTarget;

    while (xTmp <= (xEnd+accuracy) && xEndIsTaken == false) {

        if (withL) {
            yTmp = calcCoordOfL(xTmp, theta2);
        }else{
            yTmp = calcCoordOfH(xTmp, theta2);
        }

        err = yTmp - yTarget;

        if (xStartIsTaken == false) {
            if (compareSign(err, errPrec) == true) {
                xStartIsTaken = true;
                tmpXEnd = xTmp;
            }else{
                tmpXStart = xTmp;
            }
        // If we have found the first value, but not the second
        }else if (xEndIsTaken == false) {
            if (compareSign(err, errPrec) == true) {
                tmpXEnd = xTmp;
                xEndIsTaken = true;
            }
        }
        
        errPrec = err;
        xTmp += accuracy;
    }
    
    // If no solution is found
    if (tmpXStart > tmpXEnd) {
        return false;
    }

    // We do the intersection of the two interval (the new, and the one initially requested)
    if (tmpXStart > xStart) xStart = tmpXStart;
    if (tmpXEnd < xEnd) xEnd = tmpXEnd;

    // If we don't have one solution
    if ( (xEnd - xStart) > 2.1f*accuracy ) {
        return false;
    }

    if (withL) {
        yTmp = calcCoordOfL((xStart+xEnd)/2, theta2);
    }else{
        yTmp = calcCoordOfH((xStart+xEnd)/2, theta2);
    }
    // if the solution is not enough accurate
    if (abs(yTmp - yTarget) >= POSITION_ACCURACY) {
        accuracy /= 10;
        return searchTheta1(withL, xStart, xEnd, yTarget, theta2, accuracy);
    }

    return true;
}

void GeoPlane::getAngle(float & theta1, float & theta2) {
    float tmp, tmpAccurate;
    float theta1Min, theta1Max;

    bool theta1IsFound = false;

    // If we do not know the angle
    if (thetaIsCalc == false) {
        // We figure out theta2 using the geometrical formula
        tmp = this->l * this->l;
        tmp += (this->h+VAL_D-VAL_A)*(this->h+VAL_D-VAL_A);
        tmp -= VAL_B*VAL_B+VAL_C*VAL_C;
        tmp /= (2*VAL_B*VAL_C);

        if (tmp>1) tmp = 1;
        else if (tmp<-1) tmp=-1;

        this->theta2 = -acos(tmp);

        // We search theta1
        theta1Min = -25*3.14159/180;
        theta1Max = 95*3.14159/180;
        tmpAccurate = 2*3.14159/180;
        searchTheta1(false, theta1Min, theta1Max, this->h, this->theta2, tmpAccurate);
        while (theta1IsFound == false) {
            theta1IsFound = searchTheta1(true, theta1Min, theta1Max, this->l, this->theta2, tmpAccurate);
            theta1IsFound |= searchTheta1(false, theta1Min, theta1Max, this->h, this->theta2, tmpAccurate);
        }
        
        this->theta2 = this->theta2;
        this->theta1 = (theta1Min + theta1Max) / 2;

        thetaIsCalc = true;
    }

    theta1 = this->theta1*180/3.14159;
    theta2 = this->theta2*180/3.14159;
}

void GeoPlane::getCoord(float & l, float & h) {
    // If we do not know the position
    if (coordIsCalc == false) {
        this->l = calcCoordOfL(theta1, theta2);
        this->h = calcCoordOfH(theta1, theta2);
        coordIsCalc = true;
    }

    l = this->l;
    h = this->h;
}

// Angle params must be in radian
float GeoPlane::calcCoordOfL(float theta1, float theta2) {
    return VAL_B*cos(theta1) + VAL_C*cos(theta1 + theta2);
}

// Angle params must be in radian
float GeoPlane::calcCoordOfH(float theta1, float theta2) {
    return VAL_A + VAL_B*sin(theta1) + VAL_C*sin(theta1+theta2) - VAL_D;
}