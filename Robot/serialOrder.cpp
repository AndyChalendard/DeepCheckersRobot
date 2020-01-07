#include "serialOrder.hpp"

SerialOrder::SerialOrder(RawSerial & serial) {
    this->serial = &serial;

    receiveState = ReceiveState::init;

    serial.attach(callback(serialReceiveExe, this), Serial::RxIrq);
}

char SerialOrder::readReceive() {
    char res = serial->getc();

    if (res == '#') {
        commandeNbChar = 0;
        receiveState = ReceiveState::header;

        serial->printf("What is your request ?\n\r");
    }

    return res;
}

void SerialOrder::requestStore() {
    if (valueIsNegative) value *= -1;

    if (strcmp(commande, "POS_X") == 0) {
        requestPosition.setX(value);
        serial->printf("Request: %s:%f stored !\n\r", commande, value);
    }
    if (strcmp(commande, "POS_Y") == 0) {
        requestPosition.setY(value);
        serial->printf("Request: %s:%f stored !\n\r", commande, value);
    }
    if (strcmp(commande, "POS_Z") == 0) {
        requestPosition.setZ(value);
        serial->printf("Request: %s:%f stored !\n\r", commande, value);
    }
    if (strcmp(commande, "POS_GO") == 0) {
        requestPosition.ready();
        serial->printf("Request: %s is launch !\n\r", commande);
    }
    if (strcmp(commande, "MAGNET") == 0) {
        requestMagnetic.setState(value > 0.5f);
        serial->printf("Request: %s is launch with state: %i !\n\r", commande, value > 0.5f);
    }
    if (strcmp(commande, "PING") == 0) {
        serial->printf("#PONG;\n\r");
    }

    commandeNbChar = 0;
    receiveState = ReceiveState::header;
}

void SerialOrder::serialReceive() {
    char rcv;

    while (serial->readable()) {
        switch(receiveState){
            case ReceiveState::init:
                readReceive();
            break;
            case ReceiveState::header:
                rcv = readReceive();
                if (rcv == ':') {
                    if (commandeNbChar != 0) {
                        commande[commandeNbChar++] = '\0';
                        serial->printf("Selected request: %s\n\r", commande);
                        valueIsNegative = false;
                        value = 0;

                        receiveState = ReceiveState::getFloat1;
                    }
                }else if (rcv != '#' && commandeNbChar < COMMANDE_TAILLE) {
                    commande[commandeNbChar++] = rcv;
                }
            break;
            case ReceiveState::getFloat1:
                rcv = readReceive();

                if (rcv == '.') {
                    valueCounter = 10;

                    receiveState = ReceiveState::getFloat2;
                } else if (rcv == ';') {
                    requestStore();
                } else if (rcv <= '9' && rcv >= '0') {
                    value *= 10;
                    value += (rcv - '0');
                } else if (rcv == '-') {
                    valueIsNegative = true;
                }
            break;
            case ReceiveState::getFloat2:
                rcv = readReceive();

                if (rcv == ';') {
                    requestStore();
                } else if (rcv <= '9' && rcv >= '0') {
                    double tmp = (rcv - '0');
                    value += tmp / valueCounter;
                    valueCounter *= 10;
                }
            break;
        }
    }
}