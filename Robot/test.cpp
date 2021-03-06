#include "test.hpp"

#ifdef TEST_LIB

void testSerialOrder(RawSerial & serial, SerialOrder & serialOrder) {
    float x, y, z;

    serial.printf("Demarrage du test de la lib serialOrder...\r\n");

    serial.printf("Test 1:\r\n");
    if (serialOrder.requestPosition.getPosTry(x, y, z)) {
        serial.printf("Ordre reçu: %f %f %f\r\n", x, y, z);
    }else{
        serial.printf("Pas d'ordre reçu\r\n");
    }

    serial.printf("Test 2 (attente):\r\n");
    serialOrder.requestPosition.getPos(x, y, z);
    serial.printf("Ordre reçu: %f %f %f\r\n", x, y, z);

    ThisThread::sleep_for(5000);

    serial.printf("Test 3:\r\n");
    if (serialOrder.requestPosition.getPosTry(x, y, z)) {
        serial.printf("Ordre reçu: %f %f %f\r\n", x, y, z);
    }else{
        serial.printf("Pas d'ordre reçu\r\n");
    }

    serial.printf("Test 4 (attente):\r\n");
    serialOrder.requestPosition.getPos(x, y, z);
    serial.printf("Ordre reçu: %f %f %f\r\n", x, y, z);

    serial.printf("Fin du test de la lib serialOrder...\r\n");
}

void testMotor(RawSerial & serial, Motor & motor) {
    serial.printf("Demarrage du test du moteur...\r\n");

    serial.printf("Request position 0\r\n");
    motor.setPosition(0);
    ThisThread::sleep_for(2500);
    serial.printf("Position 0 considéré atteinte\r\n");

    serial.printf("Request position 360\r\n");
    motor.setPositionWithDuration(360, 8.0f);
    ThisThread::sleep_for(4000);
    serial.printf("Position 180 considéré atteinte\r\n");
    
    serial.printf("Request position 360\r\n");
    motor.setPositionWithDuration(360, 1.0f);
    ThisThread::sleep_for(1000);
    serial.printf("Position 360 considéré atteinte\r\n");

    serial.printf("Request position -360\r\n");
    motor.setPositionWithDuration(-360, 4);
    ThisThread::sleep_for(4000);
    serial.printf("Position -360 considéré atteinte\r\n");

    serial.printf("Request position 0\r\n");
    motor.setPositionWithDuration(0, 4);
    ThisThread::sleep_for(4000);
    serial.printf("Position 0 considéré atteinte\r\n");
    
    serial.printf("Fin du test du moteur...\r\n");
}


#include "geoSpace.hpp"
void afficherTest(RawSerial & serial, int nb, float x, float y, float z, float tmp1, float tmp2, float tmp3) {
    serial.printf("_____________________________%i_____________________________\r\n", nb);
    serial.printf("%f:%f:%f\r\n", x, y, z);
    serial.printf("%f:%f:%f\r\n", tmp1, tmp2, tmp3);
}

void test(RawSerial & serial, GeoSpace & g, int & nb, float x, float y, float z) {
    float tmp1, tmp2, tmp3;
    
    g.setCoord(x, y, z);
    g.getAngle(tmp1, tmp2, tmp3);
    g.setAngle(tmp1, tmp2, tmp3);
    g.getCoord(tmp1, tmp2, tmp3);

    ++ nb;
    if (abs(tmp1-x)>1 || abs(tmp2-y)>1 || abs(tmp3-z)>1) {
        afficherTest(serial, nb, x,y,z,tmp1,tmp2,tmp3);
        while(1);
    }
}

void testFermeture(RawSerial & serial) {
    GeoSpace g;
    int nb=0;
    float taille;

    serial.printf("Demarrage du test de la fermeture...\r\n");

    serial.printf("Test de déplacement en sous sol... (step 1)\r\n");
    taille = 50;
    for (float z=-5; z >= -110; z-=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(serial, g, nb, x, y, z);
            }
        }
    }

    serial.printf("Test de déplacement en sous sol... (step 2)\r\n");
    taille = 150;
    for (float z=-5; z >= -65; z-=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(serial, g, nb, x, y, z);
            }
        }
    }

    serial.printf("Test de déplacement en sous sol... (step 3)\r\n");
    taille = 50;
    for (float z=-5; z >= -35; z-=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(serial, g, nb, x, y, z);
            }
        }
    }

    serial.printf("Test de déplacement au niveau du plateau...\r\n");
    taille = 316;
    for (float z=-20; z <= 20; z+=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(serial, g, nb, x, y, z);
            }
        }
    }

    serial.printf("Test de déplacement en hauteur... (step 1)\r\n");
    taille = 250;
    for (float z=5; z <= 35; z+=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(serial, g, nb, x, y, z);
            }
        }
    }

    serial.printf("Test de déplacement en hauteur... (step 2)\r\n");
    taille = 150;
    for (float z=5; z <= 65; z+=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(serial, g, nb, x, y, z);
            }
        }
    }

    serial.printf("Test de déplacement en hauteur... (step 3)\r\n");
    taille = 50;
    for (float z=5; z <= 110; z+=5) {
        for (float x=-(taille/2); x <= (taille/2); x+=1) {
            for (float y=228-(taille/2); y <= 228+(taille/2); y+=1) {
                test(serial, g, nb, x, y, z);
            }
        }
    }

    serial.printf("Mouvement effectué !\r\n");

    test(serial, g, nb, 100, 1000, 25);

    serial.printf("Fin des tests de la fermeture !\r\n");
}

#endif // TEST_LIB
