#include <iostream>
#include "geoPlane.hpp"

int main(void) {
    float tmp1, tmp2;
    int nb = 0;

    std::cout << "Demarrage\n";

    // --------------Test de GeoPlane--------------
    GeoPlane g;
    for (float i=-20; i < 90; i+=0.05) {
        for (float j=-160; j < 0; j+=0.05) {
            std::cout << "_____________________________" << ++nb << "_____________________________" << std::endl;
            std::cout << i << ":" << j << std::endl;
            g.setAngle(i, j);
            g.getCoord(tmp1, tmp2);
            g.setCoord(tmp1, tmp2);
            g.getAngle(tmp1, tmp2);
            std::cout << tmp1 <<":"<< tmp2 << std::endl;
            while (abs(tmp1-i)>0.1);
            while (abs(tmp2-j)>0.1);
        }
    }

    return 0;
}