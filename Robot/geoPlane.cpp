#include "geoPlane.hpp"
#include <math.h>

#define VAL_A 170   // Hauteur pilier
#define VAL_B 160   // Longueur arrière-bras
#define VAL_C 285   // Longueur avant-bras
#define VAL_D 32// TODO 34    // Hauteur main

#define POSITION_ACCURACY 0.5f    // Précision pour la valeur de l

void GeoPlane::setAngle(float teta1, float teta2) {
    tetaIsCalc = true;
    coordIsCalc = false;

    this->teta1 = teta1*3.14159/180;
    this->teta2 = teta2*3.14159/180;
}

void GeoPlane::setCoord(float l, float h) {
    tetaIsCalc = false;
    coordIsCalc = true;

    this->l = l;
    this->h = h;
}

// return true if the sign is different
bool compareSign(float A, float B) {
    if (A >= 0) {
        return (B<0);
    }else{
        return (B>=0);
    }
}

// Valeur donnée en radian
// retourne true si la valeur a été trouvé, false si plusieurs valeurs sont dans le nouvelle intervalle
bool GeoPlane::searchTeta1(bool withL, float & xStart, float & xEnd, float yTarget, float teta2, float & accuracy) {
    float yTmp, xTmp;
    float errPrec, err;
    bool xStartIsTaken = false;
    bool xEndIsTaken = false;
    float tmpXStart = xStart;
    float tmpXEnd = xEnd;

    xTmp = tmpXStart;
    if (withL) {
        yTmp = calcCoordOfL(tmpXStart-accuracy, teta2);
    }else{
        yTmp = calcCoordOfH(tmpXStart-accuracy, teta2);
    }

    errPrec = yTmp - yTarget;

    while (xTmp <= (xEnd+accuracy) && xEndIsTaken == false) {

        if (withL) {
            yTmp = calcCoordOfL(xTmp, teta2);
        }else{
            yTmp = calcCoordOfH(xTmp, teta2);
        }

        err = yTmp - yTarget;

        if (xStartIsTaken == false) {
            if (compareSign(err, errPrec) == true) {
                xStartIsTaken = true;
                tmpXEnd = xTmp;
            }else{
                tmpXStart = xTmp;
            }
        // Si on a toujours pas sûr de la fin, mais on a trouvé le début
        }else if (xEndIsTaken == false) {
            if (compareSign(err, errPrec) == true) {
                tmpXEnd = xTmp;
                xEndIsTaken = true;
            }
        }
        
        errPrec = err;
        xTmp += accuracy;
    }
    
    // Si rien auncun croisement n'a été trouvé sur cette interval
    if (tmpXStart > tmpXEnd) {
        return false;
    }

    // Si l'interval s'est refermé
    if (tmpXStart > xStart) xStart = tmpXStart;
    if (tmpXEnd < xEnd) xEnd = tmpXEnd;

    // Si on a trouvé un nouveau interval et pas une seule valeur
    if ( (xEnd - xStart) > 2.1f*accuracy ) {
        return false;
    }

    if (withL) {
        yTmp = calcCoordOfL((xStart+xEnd)/2, teta2);
    }else{
        yTmp = calcCoordOfH((xStart+xEnd)/2, teta2);
    }
    if (abs(yTmp - yTarget) >= POSITION_ACCURACY) {
        accuracy /= 10;
        return searchTeta1(withL, xStart, xEnd, yTarget, teta2, accuracy);
    }

    return true;
}

void GeoPlane::getAngle(float & teta1, float & teta2) {
    float tmp, tmpAccurate;
    float teta1Min, teta1Max;

    bool teta1IsFound = false;

    // Si on ne connait pas les angles
    if (tetaIsCalc == false) {
        // On calcul teta2 grâce à la fermeture géométrique inverse
        tmp = this->l * this->l;
        tmp += (this->h+VAL_D-VAL_A)*(this->h+VAL_D-VAL_A);
        tmp -= VAL_B*VAL_B+VAL_C*VAL_C;
        tmp /= (2*VAL_B*VAL_C);

        if (tmp>1) tmp = 1;
        else if (tmp<-1) tmp=-1;

        this->teta2 = -acos(tmp);

        // On recherche teta1
        teta1Min = -25*3.14159/180;
        teta1Max = 95*3.14159/180;
        tmpAccurate = 2*3.14159/180;
        while (teta1IsFound == false) {
            teta1IsFound = searchTeta1(true, teta1Min, teta1Max, this->l, this->teta2, tmpAccurate);
            teta1IsFound |= searchTeta1(false, teta1Min, teta1Max, this->h, this->teta2, tmpAccurate);
        }
        
        this->teta2 = this->teta2;
        this->teta1 = (teta1Min + teta1Max) / 2;

        tetaIsCalc = true;
    }

    teta1 = this->teta1*180/3.14159;
    teta2 = this->teta2*180/3.14159;
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

// Les paramètres des angles doivent être en radian
float GeoPlane::calcCoordOfL(float teta1, float teta2) {
    return VAL_B*cos(teta1) + VAL_C*cos(teta1 + teta2);
}

// Les paramètres des angles doivent être en radian
float GeoPlane::calcCoordOfH(float teta1, float teta2) {
    return VAL_A + VAL_B*sin(teta1) + VAL_C*sin(teta1+teta2) - VAL_D;
}