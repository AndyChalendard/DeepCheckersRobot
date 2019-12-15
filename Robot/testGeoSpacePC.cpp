#include <iostream>
#include "geoSpace.hpp"

void afficherTest(int nb, float x, float y, float z, float tmp1, float tmp2, float tmp3) {
    std::cout << "_____________________________" << nb << "_____________________________" << std::endl;
    std::cout << x << ":" << y << ":" << z << std::endl;

    std::cout << tmp1 <<":"<< tmp2 << ":" << tmp3 << std::endl;
}

void test(GeoSpace & g, int & nb, float x, float y, float z) {
    float tmp1, tmp2, tmp3;
    
    g.setCoord(x, y, z);
    g.getAngle(tmp1, tmp2, tmp3);
    g.setAngle(tmp1, tmp2, tmp3);
    g.getCoord(tmp1, tmp2, tmp3);

    ++ nb;
    if (abs(tmp1-x)>1 || abs(tmp2-y)>1 || abs(tmp3-z)>1) {
        afficherTest(nb, x,y,z,tmp1,tmp2,tmp3);
        while(1);
    }
}

int main(void) {
    int taille;
    float tmp1, tmp2, tmp3;
    int nb = 0;

    std::cout << "Demarrage\n";

    // --------------Test de GeoSpace--------------
    GeoSpace g;
    g.setAngle(63.66, 39.17, -93);
    g.getCoord(tmp1, tmp2, tmp3);
    std::cout << "x="<< tmp1 <<" y="<< tmp2 << " z=" << tmp3 << std::endl;

    g.setCoord(129.669, 261.904, 8.988);
    g.getAngle(tmp1, tmp2, tmp3);
    std::cout << "theta1="<< tmp1 <<" theta2="<< tmp2 << " theta3=" << tmp3 << std::endl;

    std::cout << "Test de déplacement en sous sol... (step 1)" << std::endl;
    taille = 50;
    for (float z=-5; z >= -110; z-=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(g, nb, x, y, z);
            }
        }
    }

    std::cout << "Test de déplacement en sous sol... (step 2)" << std::endl;
    taille = 150;
    for (float z=-5; z >= -65; z-=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(g, nb, x, y, z);
            }
        }
    }

    std::cout << "Test de déplacement en sous sol... (step 3)" << std::endl;
    taille = 50;
    for (float z=-5; z >= -35; z-=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(g, nb, x, y, z);
            }
        }
    }

    std::cout << "Test de déplacement au niveau du plateau..." << std::endl;
    taille = 316;
    for (float z=-20; z <= 20; z+=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(g, nb, x, y, z);
            }
        }
    }

    std::cout << "Test de déplacement en hauteur... (step 1)" << std::endl;
    taille = 250;
    for (float z=5; z <= 35; z+=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(g, nb, x, y, z);
            }
        }
    }

    std::cout << "Test de déplacement en hauteur... (step 2)" << std::endl;
    taille = 150;
    for (float z=5; z <= 65; z+=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(g, nb, x, y, z);
            }
        }
    }

    std::cout << "Test de déplacement en hauteur... (step 3)" << std::endl;
    taille = 50;
    for (float z=5; z <= 110; z+=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(g, nb, x, y, z);
            }
        }
    }

    std::cout << "Mouvement effectué !" << std::endl;

    return 0;
}