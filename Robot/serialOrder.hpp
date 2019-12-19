#ifndef __SERIAL_ORDER_HPP__
#define __SERIAL_ORDER_HPP__

#include "mbed.h"

class RequestPosition {
    private:
        Semaphore * semRequest;

        // Value of the request
        float x;
        float y;
        float z;

    public:
        // Constructor
        // We take an empty semaphore
        RequestPosition() {};
        RequestPosition(Semaphore & sem) : semRequest(&sem), x(0), y(0), z(0) {};

        RequestPosition & operator= (const RequestPosition & req) {semRequest = req.semRequest; x=req.x; y=req.y; z=req.z; return *this;}

        // Getters
        bool getPosTry(float & x, float & y, float & z) {
            bool res = semRequest->try_acquire();

            if (res == true) {
                x = this->x; y = this->y; z = this->z;
            }

            return res;
        }

        void getPos(float & x, float & y, float & z) {
            semRequest->acquire();
            x = this->x; y = this->y; z = this->z;
        }

        // Setters
        // We assure that the request are not ready until his validation
        void setX(float x) {this->x = x; semRequest->try_acquire();}
        void setY(float y) {this->y = y; semRequest->try_acquire();}
        void setZ(float z) {this->z = z; semRequest->try_acquire();}

        // Put the order ready
        void ready() {semRequest->try_acquire(); semRequest->release();}
};


class SerialOrder {
    private:
        RawSerial * serial;

        // Configuration constante
        static const unsigned int COMMANDE_TAILLE = 6;

        // State machine configuration
        enum class ReceiveState{
            init,
            header,
            getFloat1,
            getFloat2
        } receiveState;

        unsigned char commandeNbChar;
        char commande[COMMANDE_TAILLE + 1];

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
        SerialOrder(RawSerial & serial, Semaphore & sem);

        // Destructor
        ~SerialOrder() {}

        // Orders
        RequestPosition requestPosition;
};

#endif // __SERIAL_ORDER_HPP__
