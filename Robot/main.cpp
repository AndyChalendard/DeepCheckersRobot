#include "mbed.h"
#include "geoSpace.hpp"

Thread threadBlinkLed;
DigitalOut led1(LED1);
Serial serial(USBTX, USBRX, 9600);


void afficherTest(int nb, float x, float y, float z, float tmp1, float tmp2, float tmp3) {
    serial.printf("_____________________________%i_____________________________\r\n", nb);
    serial.printf("%f:%f:%f\r\n", x, y, z);
    serial.printf("%f:%f:%f\r\n", tmp1, tmp2, tmp3);
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

// Blink function toggles the led in a loop
void callBackBlink(DigitalOut *led) {
    while (1) {
        *led = 1;
        ThisThread::sleep_for(200);
        *led = 0;
        ThisThread::sleep_for(800);
    }
}

// Main
int main() {
    GeoSpace g;
    int nb=0;
    float taille;

    serial.printf("Initialisation...\r\n");
    threadBlinkLed.start(callback(callBackBlink, &led1));
    
    serial.printf("Test de déplacement en sous sol... (step 1)\r\n");
    taille = 50;
    for (float z=-5; z >= -110; z-=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(g, nb, x, y, z);
            }
        }
    }

    serial.printf("Test de déplacement en sous sol... (step 2)\r\n");
    taille = 150;
    for (float z=-5; z >= -65; z-=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(g, nb, x, y, z);
            }
        }
    }

    serial.printf("Test de déplacement en sous sol... (step 3)\r\n");
    taille = 50;
    for (float z=-5; z >= -35; z-=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(g, nb, x, y, z);
            }
        }
    }

    serial.printf("Test de déplacement au niveau du plateau...\r\n");
    taille = 316;
    for (float z=-20; z <= 20; z+=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(g, nb, x, y, z);
            }
        }
    }

    serial.printf("Test de déplacement en hauteur... (step 1)\r\n");
    taille = 250;
    for (float z=5; z <= 35; z+=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(g, nb, x, y, z);
            }
        }
    }

    serial.printf("Test de déplacement en hauteur... (step 2)\r\n");
    taille = 150;
    for (float z=5; z <= 65; z+=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(g, nb, x, y, z);
            }
        }
    }

    serial.printf("Test de déplacement en hauteur... (step 3)\r\n");
    taille = 50;
    for (float z=5; z <= 110; z+=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(g, nb, x, y, z);
            }
        }
    }

    serial.printf("Mouvement effectué !\r\n");

    test(g, nb, 100, 1000, 25);

    while(1) {
        sleep();
    }
}
