#include "geoPlane.hpp"
#include <math.h>

#define VAL_A 170   // Hauteur pilier
#define VAL_B 160   // Longueur arrière-bras
#define VAL_C 285   // Longueur avant-bras
#define VAL_D 34    // Hauteur main

#define DELTA_L 1    // Précision pour la valeur de l

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
    float tmp;
    float teta1Min, teta1Max;

    // Si on ne connait pas les angles
    if (tetaIsCalc == false) {
        // On calcul teta2 grâce à la fermeture géométrique inverse
        tmp = this->l * this->l;
        tmp+= (this->h+VAL_D-VAL_A)*(this->h+VAL_D-VAL_A);
        tmp-=VAL_B^2-VAL_C^2;
        tmp/=(2*VAL_B*VAL_C);

        if (tmp>1) tmp = 1;
        else if (tmp<-1) tmp=-1;

        this->teta2 = -acos(tmp);

        // On fait une dichotomie pour trouver teta1
        teta1Min = -90;
        teta1Max = 90;
        tmp = this->l - calcCoordOfL( (teta1Min+teta1Max)/2, this->teta2);
        while ( abs(tmp) > DELTA_L) {
            if (tmp > 0) {
                teta1Max = (teta1Min+teta1Max)/2;
            }else{
                teta1Min = (teta1Min+teta1Max)/2;
            }
        }
        
        this->teta1 = (teta1Min+teta1Max)/2;
    }

    teta1 = this->teta1;
    teta2 = this->teta2;
}

void GeoPlane::getCoord(float & l, float & h) {
    // Si on ne connait pas les coordonées dans le repère
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