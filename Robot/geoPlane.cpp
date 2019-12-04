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

#include <iostream>

// Valeur donnée en radian
// retourne true si la valeur a été trouvé, false si plusieurs valeurs sont dans le nouvelle intervalle
bool GeoPlane::searchTeta1(bool withL, float & xStart, float & xEnd, float yTarget, float teta2, float & accuracy) {
    float yTmp, xTmp;
    float errPrec, err;
    bool errDecrease = false;
    bool xStartIsTaken = false;
    bool xEndIsTaken = false;
    float tmpXEnd = xEnd;

    xTmp = xStart - accuracy;
    if (withL) {
        yTmp = calcCoordOfL(xTmp, teta2);
    }else{
        yTmp = calcCoordOfH(xTmp, teta2);
    }

    errPrec = abs(yTmp - yTarget);
    xTmp += accuracy;

    while (xTmp < tmpXEnd) {
        //std::cout << "x: " << xStart*180/3.14159 << " " << xEnd*180/3.14159 << " " << xTmp*180/3.14159 << std::endl;
        //for (int i = 0; i < 99999999; i++);

        if (withL) {
            yTmp = calcCoordOfL(xTmp, teta2);
        }else{
            yTmp = calcCoordOfH(xTmp, teta2);
        }

        err = abs(yTmp - yTarget);

        if (xStartIsTaken == false) {
            // Si l'erreur diminue
            if (err < errPrec) {
                xStart = xTmp-accuracy/2;
                errDecrease = true;
            }else{
                if (errDecrease == true) {
                    xStartIsTaken = true;
                    xEnd = xTmp;
                }
                errDecrease = false;
            }
        // Si on a toujours pas trouvé la fin, mais on a trouvé le début
        }else if (xEndIsTaken == false) {
            // Si l'erreur diminue
            if (err < errPrec) {
                xEnd = xTmp + accuracy/2;
                errDecrease = true;
            }else{
                if (errDecrease == true) {
                    xEndIsTaken = true;
                    tmpXEnd = xEnd;
                }
                errDecrease = false;
            }
        }
        
        errPrec = err;
        xTmp += accuracy;
    }

    // Si on a trouvé un nouveau interval et pas une seule valeur
    if ( (xEnd - xStart) > 3*accuracy ) {
        //std::cout << "Intervalle.." << std::endl;
        return false;
    }

    if (withL) {
        yTmp = calcCoordOfL(xStart, teta2);
    }else{
        yTmp = calcCoordOfH(xStart, teta2);
    }
    if (abs(yTmp - yTarget) > POSITION_ACCURACY) {
        //std::cout << "Precision: " << abs(yTmp - yTarget) << "\nAugmentation de la demande de précision" << std::endl;
        accuracy /= 2;
        return false;
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
            //std::cout << "Search with l et " << this->teta2*180/3.14159 << "\n";
            teta1IsFound = searchTeta1(true, teta1Min, teta1Max, this->l, this->teta2, tmpAccurate);
            if (teta1IsFound == false) {
                //std::cout << "Search with h et " << this->teta2*180/3.14519 << "\n";
                teta1IsFound = searchTeta1(false, teta1Min, teta1Max, this->h, this->teta2, tmpAccurate);
            }
        }
        
        this->teta2 = this->teta2;
        this->teta1 = teta1Min;

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