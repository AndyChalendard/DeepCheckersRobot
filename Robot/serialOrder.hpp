#ifndef __SERIAL_ORDER_HPP__
#define __SERIAL_ORDER_HPP__

#include "mbed.h"

class SerialOrder {
    private:
        RawSerial * serial;

        // Configuration constante
        static const unsigned int COMMANDE_TAILLE = 5;

        // State machine configuration
        enum class ReceiveState{
            init,
            header,
            getFloat1,
            getFloat2
        } receiveState;

        unsigned char commandeNbChar;
        unsigned char commande[COMMANDE_TAILLE + 1];

        float value;
        bool valueIsNegative;
        unsigned int valueCounter;

        // State machine
        void serialReceive();

        // State machine launcher
        static void serialReceiveExe(SerialOrder * serialOrder) {serialOrder->serialReceive();}

        // return the readed char
        char readReceive();

        // Store the request
        void requestStore();
    public:
        // Constructor
        SerialOrder(RawSerial & serial);

        // Destructor
        ~SerialOrder() {}
};

#endif // __SERIAL_ORDER_HPP__
