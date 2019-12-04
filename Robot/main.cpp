#include <iostream>
#include "geoPlane.hpp"

int main(void) {
    float tmp1, tmp2;
    int nb = 0;

    std::cout << "Demarrage\n";

    // --------------Test de GeoPlane--------------
    GeoPlane g;
    for (float i=-20; i < 90; i+=0.5) {
        for (float j=-120; j < 0; j+=0.5) {
            g.setAngle(i, j);
            g.getCoord(tmp1, tmp2);
            g.setCoord(tmp1, tmp2);
            g.getAngle(tmp1, tmp2);
            std::cout << nb++ << ": \t" << i << ":" << tmp1 << "\t" << j<<":"<< tmp2 << std::endl;
            while (abs(tmp1-i)>0.5);
        }
    }
    /*
    g.setAngle(-20.0, -103.5);
    g.getCoord(tmp1, tmp2);
    std::cout << tmp1 << " " << tmp2 << std::endl;

    g.setCoord(418.163, -14.1988);
    g.getAngle(tmp1, tmp2);
    std::cout << tmp1 << " " << tmp2 << std::endl;*/

    return 0;
}