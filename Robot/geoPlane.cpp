#include "geoPlane.hpp"
#include <math.h>

#define VAL_A 170   // Hauteur pilier
#define VAL_B 160   // Longueur arrière-bras
#define VAL_C 285   // Longueur avant-bras
#define VAL_D 34    // Hauteur main

void GeoPlane::setAngle(float teta1, float teta2) {
    tetaIsCalc = true;
    coordIsCalc = false;

    this->teta1 = teta1;
    this->teta2 = teta2;
}

void GeoPlane::setCoord(float l, float h) {
    tetaIsCalc = false;
    coordIsCalc = true;

    this->l = l;
    this->h = h;
}

void GeoPlane::getAngle(float & teta1, float & teta2) {
    // TODO
}

void GeoPlane::getCoord(float & l, float & h) {
    if (coordIsCalc == false) {
        this->l = calcCoordOfL(teta1, teta2);
        this->h = calcCoordOfH(teta1, teta2);
        coordIsCalc = true;
    }

    l = this->l;
    h = this->h;
}

float GeoPlane::calcCoordOfL(float teta1, float teta2) {
    return VAL_B*cos(teta1) + VAL_C*cos(teta1 + teta2);
}

float GeoPlane::calcCoordOfH(float teta1, float teta2) {
    return VAL_A + VAL_B*sin(teta1) + VAL_C*sin(teta1+teta2) - VAL_D;
}